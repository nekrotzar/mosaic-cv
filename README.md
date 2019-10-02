# mosaic-cv

This script generates photo mosaics using Python3 and the library OpenCV to handle images.
The script requires a target image and different images to be processed as the block units in the mosaic.


## Usage

Run the following command:
> python mosaic.py <target> <images> <block_size>

* `target`: the target image directory.
* `images`: the image directory to be used. A recursive search is used to find all the suported files.
To add other image formats, edit the code to add the format prefix to the global variable [IMAGE_FILE_FORMATS](https://github.com/nekrotzar/mosaic-cv/blob/master/mosaic.py#L9).
* `block_size`: the size of a mosaic square block (in pixels).

## Example
Using a custom dataset of images placed in /data/images:
> python mosaic.py data/cat.jpg data/images 20

Original(data/cat.jpg)             |  Mosaic(data/out/mosaic-20-2320x3480)
:-------------------------:|:-------------------------:
![](data/cat.jpg)  |  ![](data/out/mosaic-20-2320x3480.png)
