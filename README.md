
# UOLO: A Multitask U-Net YOLO Hybrid Model for Railway Scene Understanding.

Official repository for our proposed approach UOLO which attempts to improve Railway Scene Understading through a Multi-Task method which combined [YOLOv5](https://github.com/ultralytics/yolov5) and [U-Net](https://arxiv.org/pdf/1505.04597). 


![UOLO Overview](https://github.com/manole-alexandru/yolov5-uolo/blob/uolo-vanilla/uolo_overview.png?raw=true)

The implementation is heavily based on [YOLOv5](https://github.com/ultralytics/yolov5), as seen by the fact that this repo is a fork of the YOLOv5 repo. In simple terms, UOLO an extension of YoloV5 which also performs semantic segmentation. 

This repository also contains a "geometric" preprocessing tailored for the rail-domain, especially for the RailSem19 dataset. The code which obtains this extra input can be found 
in the preprocessing folder.

We plan to further extend this work and make the code more robust in order to facilitate the use of this repository.
## Usage

The approach was focused on the [RailSem19](https://www.wilddash.cc/railsem19) dataset. A starting notebook which contains all necesary code can be found in this repo, in the [UOLO_Notebook file](https://github.com/manole-alexandru/yolov5-uolo/blob/uolo-vanilla/UOLO_Notebook.ipynb).

There the RailSem19 dataset is transformed to the YOLO format. Furthermore, the segmentation masks and preprocessing channels are obtained. To best understand the use of this repo we also recommand checking the original repository: https://github.com/ultralytics/yolov5.

The notebook can also be used to conduct experiments on other datasets (through small modifications), as long as the chosen dataset respects the following structure:

![UOLO Overview](https://github.com/manole-alexandru/yolov5-uolo/blob/uolo-vanilla/dataset_structure.png?raw=true)

The additions from the YOLOv5 structure are the masks and preprocessed folders. Both contain grayscale images with only black (0, 0, 0) and white (255, 255, 255) pixels. These images have to corespond to the ones from the images folder. Training UOLO without the proposed geometric preprocessing is also possible by setting the geometric preprocessing variable to false in the provided notebook:

```python 
USE_GEOMETRIC_PREPROCESSING = False
```

In this case, the preprocessed images and folders are not required. The two approaches (with & without preprocessing) are kept on the two branches of the repository: uolo-vanilla and uolo-extra-geometric-input. Besides this variable, multiple aspects of a experiment can be configured in the first cell of the starter notebook

```python 
USE_GEOMETRIC_PREPROCESSING = False
SEGMENTATION_OBJECTIVE = 'rail' # 'track'

EPOCHS = 1
BATCH_SIZE = 16
IMAGE_SIZE = 640

SEED = random.randint(0, 1000)

# Dataset 

WITH_CACHING = False # May cause issues if caching = True

TRAIN_SPLIT = 0.7
VALIDATION_SPLIT = 0.2
TEST_SPLIT = 0.1

# "none" - No filters - 0| "no_switches" - Filter images with no switches - 5736 | "only_unknown" - Filter images with only unknown switches - 6246
# "unknown_switches" - Filter images with at least one unknown image - 7260 | "unkown_switches_keep_no"
FILTER_SWITCHES = "no_switches"

KEEP_UNKNOWN = False # Keep annotations of unknown switches

# Dataset preprocessing

BOX_ENLARGE_CONSTANT = 150
BOX_ENLARGE_PERCENT_HEIGHT = 1.25
BOX_ENLARGE_PERCENT_WIDTH = 1.25

THRESHOLD_FOR_ENLARGE = 1920 * 1080 # 1920 * 1080 -> enlarge all BBoxes

PRECISION = 6
```

Some variables are self-explinatory (TRAIN, VALIDATION, TEST split). The rest will be explanined here:
- **SEGMENTATION_OBJECTIVE** - This RailSem19 specific fields determined wheter the segmentation objective will encapsulate the rails or both the rail and the track
- **FILTER_SWITCHES** - This allows granularity in the choice of images which will be kept in the dataset (all images, images with at least a switch, images with no unknown switches, etc.)
- **KEEP_UNKNOWN** - Wheter or not to keep unknown switches in the dataset
- **BOX_ENLARGE** - These variables enlarge the bounding boxes from the original dataset. Constant adds a absolut value to the height and width of the original bounding boxes, while the percent variables add a relative amount by multiplyng the height and width with the chosen number.
- **THRESHOLD_FOR_ENLARGE** - Bounding boxes with a size larger than this number will not have their dimensions increased by either the constant or relative enlargement.
- **PRECISION** - The amount of digits after the decimal point, which are used in describing the coordinates of the bounding boxes
## Contributing

Contributions are always welcome!



## Authors
- [Alexandru Manole](https://github.com/manole-alexandru) - alexandru.manole@ubbcluj.ro (Contact)
- [Laura Dioșan](https://www.cs.ubbcluj.ro/~lauras/) - laura.diosan@ubbcluj.ro


