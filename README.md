# UOLO: UOLO: A Multitask U-Net YOLO Hybrid Model for Railway Scene Understanding.

This is the repository which implements UOLO, a YOLO-U-Net hybrid for joint object detection and semantic segmentation.

The implementation is heavily based on [YoloV5](https://github.com/ultralytics/yolov5). UOLO is basicly an extension of YoloV5 which also performs semantic segmentation. 

This repository also contains a "geometric" preprocessing tailored for the rail-domain, especially for the RailSem19 dataset. The code which obtains this extra input can be found 
in the preprocessing folder. 

This run this code add  'masks' and 'preprocessing' folders to at the same level with the 'images' and 'labels' folders used in the vanilla YoloV5.

There is still work to be done to conducted in order to further facilitate the use of this repository, which will be done as soon as posible :)

