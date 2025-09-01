**Project Sheek\
**

**1. Stage-1**

A complete end to end dockerized solution which includes implementation
of the following: -

\(a\) Data pipeline

\(b\) Reading data-files in formats defined in datasets section.

\(c\) Pre-processing as required.

\(d\) ML/DL inferencing model for ship detection in EO and SAR images

\(e\) Algorithms for correlation between ship detections and AIS data

\(f\) Algorithms for path interpolation- For sparse AIS points
interpolating the intermediate points.

\(g\) Output in formats defined in evaluation section.

![](media/image1.png){width="6.268055555555556in"
height="1.0694444444444444in"}

**2. Stage-2**

The solution would broadly have to focus on the following (including
Planetscope data): -

\(a\) Ship Detection

\(b\) Classification of vessels as per pre-defined classes

\(c\) Correlation with AIS

\(d\) Path interpolation

\(e\) Path prediction

**3. Stage-3**

Exact details will be updated prior to beginning of this stage. The
solution would broadly have to focus on the following on internal
datasets : -

\(a\) Ship Detection

\(b\) Classification of vessels as per pre-defined classes

\(c\) Correlation with AIS and other spatio-temporal datasets

\(d\) Path interpolation

\(e\) Path prediction within 2 knots of speed and 5 deg of course

\(f\) Use historical data for providing more insights

**Roadmap**\
\
**Stage-1**

1.  **Data Collection and Organization**

**Objectives:**

-   Efficiently gather all required datasets

-   Organize data logically for smooth processing and modeling

-   Prepare data for preprocessing steps

**Download Satellite Imagery**

Access Sentinel-1 SAR images (TIFF format) from Copernicus or specified
open-source repositories.

Download Sentinel-2 EO images (JP2 format) for the prescribed locations
and dates.

Ensure coverage matches AIS and other auxiliary data timeframes.

**Acquire AIS Data**

Download AIS CSV files from Marine Cadastre \|\| provided mock/sample
datasets.

Data completeness, correct columns (latitude, longitude, MMSI,
timestamp, speed, course).

**Gather Land Masking Data**

Obtain coastline vector shapefiles or data from natural earth datasets
or other sources referenced.

Download any cloud masking masks or auxiliary files.

**Organize Data Storage**

Create a clear folder structure separating:

-Raw satellite images (SAR and EO)

-AIS CSV files

-Land masking and auxiliary data

-Processed and intermediate outputs

**Metadata Management**

Maintain metadata files or logs that link image files to their
timestamps, geographic tiles, and AIS data segments.

Record dataset versions and source URLs for reproducibility.

**Initial Data Inspection**

Visual inspection of some images to verify no corruption.

Check AIS data for anomalies such as missing timestamps or invalid
positions.

2.  **Data Preprocessing**

**Objectives:**

-   Prepare raw satellite satellite imagery and AIS data for input to
    models

-   Improve image quality and relevance with masking and normalization

-   Clean and align AIS data for correlation and interpolation

**Cloud Masking for EO Images**

Use spectral band combinations or cloud masks provided with Sentinel-2
data to filter out cloudy or hazy pixels.

Apply pixel-wise masks to exclude these pixels from further processing.

Consider using established cloud masking algorithms or Sentinel-2 Level
2A products if available.

**Land Masking**

Use coastline vector shapefiles to create a land mask polygon for each
image.

Mask out any detected objects or pixels that fall on land or within a
certain buffer zone near coastlines.

Ensure detection focus remains only on open-sea regions as required.

**Image Standardization**

Convert all images to a consistent coordinate reference system (e.g.,
WGS84).

Resample or crop images to fixed sizes if needed for model input (e.g.,
640x640 pixels).

Normalize spectral bands or pixel intensities across datasets for
consistent input ranges.

**AIS Data Cleaning and Synchronization**

Remove AIS records with missing or invalid coordinates, timestamps, or
MMSI.

Correct any obvious anomalies in position or speed.

Align AIS data temporally and spatially with corresponding satellite
image capture times and coverage.

Potentially interpolate missing AIS data points for better matches
later.

**Data Augmentation**

Apply augmentations such as rotations, flips, brightness adjustment on
satellite patches for robust model training.

Maintain synchronization of augmented AIS labels where applicable.

**Data Storage and Logging**

Store preprocessed images and masked AIS data in organized directories.

Log preprocessing parameters and versions for reproducibility.

3.  **Vessel Detection Model Development**

**Objectives:**

-   Build and train accurate models to detect vessels in satellite
    images (EO and SAR)

-   Ensure models generalize well across environmental conditions

**Model Selection**

Choose a suitable detection architecture such as YOLOv11, Faster R-CNN,
or EfficientDet.

Consider trade-offs between speed, accuracy, and deployment constraints
(offline, dockerized).

**Dataset Preparation for Training**

Prepare labeled training datasets with vessel bounding boxes for both
Sentinel-1 SAR and Sentinel-2 EO images.

Convert annotations into the required format compatible with the chosen
model (e.g., YOLO format).

Split data into training, validation, and test sets.

**Training Setup**

Define hyperparameters (learning rate, batch size, epochs).

Implement data augmentation: rotations, flips, brightness/noise
adjustments to improve robustness.

Train models separately on EO and SAR images or explore multi-sensor
fusion approaches.

**Model Evaluation**

Evaluate on validation sets using metrics like Average Precision (AP)
and recall.

Analyze false positives and false negatives to guide model tuning.

Ensure bounding boxes for detections are non-overlapping as required.

**Model Optimization**

Fine-tune hyperparameters based on evaluation.

Implement post-processing techniques: Non-Maximum Suppression (NMS) with
strict IoU thresholds.

Compress or prune models if necessary for faster offline inference.

**Model Export and Integration**

Save trained model weights and configurations.

Prepare inference scripts compatible with dockerized deployment.

Test inference on sample images to verify outputs.

4.  **Dimension & Heading Estimation**

**Objectives:**

-   Accurately estimate vessel length, width, and heading angle from
    detected bounding boxes in satellite images

-   Provide metadata needed for further correlation and classification

**Calculate Vessel Dimensions**

Use bounding box pixel dimensions and satellite image spatial resolution
to compute vessel length and width in meters.

For rotated boxes or polygons, compute the oriented bounding box to find
length (longer side) and width (shorter side).

**Heading (Orientation) Estimation**

Extract vessel heading from the orientation of the bounding box or
polygon.

Analyze pixel intensity gradients or shape symmetry if available to
refine heading direction.

Convert heading to degrees relative to true north or satellite image
orientation referencing geographic metadata.

**Validation and Calibration**

Validate estimated dimensions and heading on annotated samples or via
AIS vessel dimension data when available.

Adjust algorithms to compensate for sensor distortions or image
projection effects.

**Integration into Pipeline**

Integrate dimension and heading estimation as a post-processing step
after vessel detection.

Ensure consistent formatting of output parameters matching submission
expectations.

5.  **Vessel Classification**

**Objectives:**

-   Categorize each detected vessel into pre-defined classes (e.g.,
    commercial, vessel of interest, other)

-   Enhance maritime domain awareness through vessel type recognition

**Feature Extraction**

Extract image patches or bounding box regions around detected vessels
from EO and SAR images.

Compute relevant features such as spectral signatures (EO), radar
backscatter patterns (SAR), shape, and texture.

**Model Selection and Training**

Choose a suitable classification model (e.g., CNN, transfer learning
with ResNet, EfficientNet).

Use labeled dataset to train the classifier on extracted features or
image patches.

Employ data augmentation to improve robustness (rotations, brightness,
noise).

**Evaluation and Tuning**

Validate classification accuracy on a separate validation set.

Tune hyperparameters and experiment with architectures to reduce
misclassification.

**Integration**

Integrate classifier into the post-detection pipeline.

Ensure output includes classification results formatted as required in
submission specifications.

6.  **AIS Correlation Algorithm Development**

**Objectives**:

-   Correlate detected vessels from satellite imagery with AIS data to
    identify each vessel

-   Handle spatial and temporal matching challenges to improve
    correlation accuracy

**Data Preparation**

Ensure AIS data (MMSI, timestamp, latitude, longitude, speed, course) is
cleaned and correctly formatted.

Extract detection centroids (latitude and longitude) from vessel
bounding polygons.

**Spatial Matching**

Define a geographical proximity threshold (e.g., within a few hundred
meters) to consider matches between detected vessels and AIS positions.

Use geodetic distance calculations to measure proximity.

**Temporal Matching**

Consider temporal proximity by comparing image capture timestamps and
AIS record timestamps.

Allow a reasonable time window to accommodate AIS data sparsity and
satellite image acquisition time.

**Matching Strategy**

Apply a scoring or ranking system combining spatial and temporal
distances.

Handle many-to-one and one-to-many matches by selecting the best-scoring
pair or applying heuristics.

**Output Generation**

Create CSV with columns: image name, timestamp, vessel_latitude,
vessel_longitude, MMSI.

Ensure proper formatting and consistency with challenge requirements.

**Validation and Refinement**

Validate correlation accuracy on available annotated data or known
matches.

Adjust thresholds and algorithms based on validation results.

7.  **Path Interpolation Modeling**

**Objectives:**

-   Interpolate missing vessel positions and paths from sparse AIS data
    points

-   Provide continuous vessel tracks for analysis and prediction

**Data Preparation**

Organize AIS trajectory data by vessel (MMSI) and timestamp.

Identify gaps or missing points in vessel trajectories within the AIS
data.

**Interpolation Methods**

Implement interpolation techniques suitable for vessel movement:

Linear interpolation for short gaps

Spline interpolation for smoother paths

Kalman filtering or moving average for noisy data smoothing

Explore machine learning or sequence models (e.g., RNNs, LSTMs) for more
advanced interpolation.

**Incorporate Speed and Course**

Use AIS speed and course information to constrain interpolated paths.

Limit interpolation results to physically plausible speeds and course
changes.

**Output Formatting**

Generate CSV output with columns: timestamp, path_id, point_id,
latitude, longitude, speed, course.

Maintain chronological order and unique identification for each path and
point.

**Validation**

Validate interpolated tracks against known trajectories or ground truth
data where available.

Measure accuracy with RMSE or other distance metrics.

**Integration**

Integrate interpolation module with AIS correlation and vessel detection
pipeline.

8.  **Output Formatting & Result Export**

**Objectives:**

-   Format all model outputs and processed data into the required
    submission formats

-   Ensure compatibility with evaluation tools and visualization
    software (QGIS)

**Detection Output Formatting**

Convert vessel detections to geoJSON format with bounding polygons.

Ensure polygons are well-defined with coordinates in latitude and
longitude.

Verify no overlap among bounding boxes as per challenge rules.

**Shapefile Export**

Generate QGIS-compatible shapefiles from detection results.

Create one shapefile per satellite image containing all vessel
detections in that frame.

**AIS Correlation CSV**

Prepare CSV files correlating image detections with AIS data.

Columns to include image name, timestamp, vessel latitude, vessel
longitude, MMSI.

Validate CSV structure and data integrity.

**Path Interpolation CSV**

Format interpolated tracks CSV with required columns: timestamp, path
ID, point ID, latitude, longitude, speed, course.

Maintain order and ensure no missing or duplicated rows.

**File Naming and Metadata**

Adhere strictly to file naming conventions:

\[YYYY_MM_DD\]\_\[STARTUP_NAME\]\_\[FILE_TYPE\]

Include metadata in each file where required, such as version, detection
thresholds.

**Quality Assurance**

Use scripts to validate geoJSON polygons and shapefile formats.

Validate CSV file columns and sample data consistency.

Perform mock imports into QGIS or other GIS tools to confirm
correctness.

9.  **Dockerization & Offline Solution Readiness**

**Objectives:**

-   Package the entire processing pipeline into a portable, reproducible
    Docker container

-   Ensure offline functionality matching challenge hardware and
    software requirements

**Define Environment Setup**

List all software dependencies: Python version, ML/DL frameworks
(PyTorch, TensorFlow), geospatial libraries (GDAL, Shapely), and
utilities.

Define system requirements: OS base image (e.g., Ubuntu 24.04 LTS),
required drivers (CUDA for GPU), and resource limits.

**Dockerfile Creation**

Write Dockerfile specifying base image, environment variables, and
installation steps.

Include all code, scripts, model weights, and configuration files inside
the container.

Ensure proper paths and permissions for volume mounts and data access.

**Automate Pipeline Execution**

Create entrypoint or execution scripts that can run the entire pipeline
end-to-end from raw data ingestion to output generation.

Parameterize inputs and outputs for flexibility.

**Offline Capability Testing**

Test container on a system with no internet connectivity to verify
offline readiness.

Ensure all required models and data are bundled or accessible offline.

**Performance and Resource Optimization**

Optimize container size by cleaning temporary files and using
slimmed-down base images.

Profile CPU/GPU/RAM usage to ensure compliance with competition hardware
limits.

**Documentation**

Document container usage instructions, command-line parameters, and any
configuration needs.

Keep logs for debugging and performance monitoring during container
execution.

10. **Testing, Validation, and Iteration**

**Objectives:**

-   Test the end-to-end pipeline for accuracy, robustness, and
    compliance

-   Validate output correctness, format adherence, and metric
    performance

-   Iterate to fix issues and optimize the solution before submission

**Unit Testing of Components**

Test individual modules such as preprocessing, detection,
classification, correlation, and interpolation independently.

Verify expected outputs and error handling for each.

**End-to-End Pipeline Testing**

Run the complete pipeline on mock and sample datasets provided by the
challenge.

Confirm successful pipeline execution without crashes or dependency
issues.

**Output Validation**

Check all output files (geoJSON, shapefiles, CSV) for correct formatting
and naming as per challenge specifications.

Ensure no overlapping bounding boxes in detection outputs.

**Accuracy and Metric Evaluation**

Calculate detection Average Precision (AP), AIS correlation F1 score,
and interpolation RMSE internally.

Compare results against reference data or previous benchmarks.

**Performance Optimization**

Optimize latency and resource usage to meet constraints.

Refine models and algorithms based on test results and error analysis.

**Final Simulation**

Simulate final submission workflows including docker container execution
and output packaging.

Prepare final submission packages and documentation for upload.
