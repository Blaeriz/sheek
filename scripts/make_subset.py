#!/usr/bin/env python3
"""
make_subset.py

Create a random subset of images and their corresponding label files.

Default behavior:
- Source images: data/train/images
- Source labels: data/train/labels (checked; script will try a few candidate locations)
- Destination: data/train/subset/images and data/train/subset/labels
- Default subset size: 5000

Usage:
  python scripts/make_subset.py --n 5000

The script is defensive: if fewer images are available it will copy all of them; it warns when a label file is missing.
"""
import argparse
import os
import random
import shutil
import sys


def find_labels_dir(src_root):
    # Try some sensible defaults for where labels may be stored
    candidates = [
        os.path.join(src_root, 'labels'),                      # data/train/labels
        os.path.join(os.path.dirname(src_root), 'labels'),     # data/labels
        os.path.join('data', 'labels'),                        # data/labels
        os.path.join('data', 'labels', os.path.basename(src_root)),
    ]
    for c in candidates:
        if os.path.isdir(c):
            return c
    return None


def list_images(images_dir, exts=None):
    if exts is None:
        exts = {'.jpg', '.jpeg', '.png', '.tif', '.tiff'}
    files = [f for f in os.listdir(images_dir) if os.path.splitext(f)[1].lower() in exts]
    files.sort()
    return files


def copy_subset(src_images_dir, src_labels_dir, dest_root, chosen_files):
    dest_images = os.path.join(dest_root, 'images')
    dest_labels = os.path.join(dest_root, 'labels')
    os.makedirs(dest_images, exist_ok=True)
    os.makedirs(dest_labels, exist_ok=True)

    missing_labels = 0
    for fname in chosen_files:
        src_img = os.path.join(src_images_dir, fname)
        dst_img = os.path.join(dest_images, fname)
        shutil.copy2(src_img, dst_img)

        label_name = os.path.splitext(fname)[0] + '.txt'
        # prefer labels in src_labels_dir
        src_lbl = os.path.join(src_labels_dir, label_name) if src_labels_dir else None
        if src_lbl and os.path.isfile(src_lbl):
            shutil.copy2(src_lbl, os.path.join(dest_labels, label_name))
        else:
            # warn and create empty label to keep file counts consistent (optional)
            missing_labels += 1
    return missing_labels


def main():
    p = argparse.ArgumentParser(description='Create a random subset of images+labels')
    p.add_argument('--src-root', default=None,
                   help='source root containing images/ and labels/ (e.g. data/train). Can be provided multiple times or as a comma-separated list')
    p.add_argument('--n', type=int, default=5000, help='number of images to sample per src-root (default: 5000)')
    p.add_argument('--dest-subdir', default='subset', help='destination subdir under each src-root (default: subset)')
    p.add_argument('--seed', type=int, default=42, help='random seed')
    p.add_argument('--all', action='store_true', help='process both data/train and data/val')
    args = p.parse_args()

    random.seed(args.seed)

    # Determine list of roots to process
    roots = []
    if args.all:
        roots = [os.path.join('data', 'train'), os.path.join('data', 'val')]
    elif args.src_root:
        # support comma-separated list
        roots = [r.strip() for r in args.src_root.split(',') if r.strip()]
    else:
        roots = [os.path.join('data', 'train')]

    for root in roots:
        src_images = os.path.join(root, 'images')
        if not os.path.isdir(src_images):
            print(f'ERROR: images directory not found: {src_images}', file=sys.stderr)
            continue

        src_labels = find_labels_dir(root)
        if not src_labels:
            print(f'WARNING: labels directory not found for {root}. Labels will not be copied.', file=sys.stderr)
        else:
            print(f'[{root}] Using labels from: {src_labels}')

        all_images = list_images(src_images)
        total = len(all_images)
        if total == 0:
            print(f'No images found in {src_images}. Skipping.', file=sys.stderr)
            continue

        n = min(args.n, total)
        chosen = random.sample(all_images, n) if n < total else all_images

        dest_root = os.path.join(root, args.dest_subdir)
        print(f'[{root}] Copying {len(chosen)} images from {src_images} to {dest_root}/images')
        missing_labels = copy_subset(src_images, src_labels, dest_root, chosen)

        print(f'[{root}] Done.')
        print(f'[{root}] Total images available: {total}')
        print(f'[{root}] Images copied: {len(chosen)}')
        if src_labels:
            print(f'[{root}] Labels missing for {missing_labels} images (those labels were not found in {src_labels})')


if __name__ == '__main__':
    main()
