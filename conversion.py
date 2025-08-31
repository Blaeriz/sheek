import os
import random
import shutil

# Current dataset
img_dir = "data/train/images"
lbl_dir = "data/train/labels"

# Output split dataset
output_dir = "data/split"
train_img_out = os.path.join(output_dir, "train/images")
train_lbl_out = os.path.join(output_dir, "train/labels")
val_img_out = os.path.join(output_dir, "val/images")
val_lbl_out = os.path.join(output_dir, "val/labels")

# Make output dirs
for d in [train_img_out, train_lbl_out, val_img_out, val_lbl_out]:
    os.makedirs(d, exist_ok=True)

# List all images
images = [f for f in os.listdir(img_dir) if f.endswith(".jpg")]
random.shuffle(images)

# Split (80% train, 20% val)
split_idx = int(0.8 * len(images))
train_files = images[:split_idx]
val_files = images[split_idx:]

def copy_files(files, img_out, lbl_out):
    for f in files:
        img_path = os.path.join(img_dir, f)
        lbl_path = os.path.join(lbl_dir, f.replace(".jpg", ".txt"))
        
        if os.path.exists(lbl_path):  # only copy if label exists
            shutil.copy(img_path, img_out)
            shutil.copy(lbl_path, lbl_out)

# Copy into train/val
copy_files(train_files, train_img_out, train_lbl_out)
copy_files(val_files, val_img_out, val_lbl_out)

print(f"✅ Done! Train: {len(train_files)} images, Val: {len(val_files)} images")
