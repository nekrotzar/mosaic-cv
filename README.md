# mosaic-cv

This script generates photo mosaics with **Python3** using the **OpenCV** library to handle images.
The script requires a target image and different images to be processed as the block units in the mosaic.


## Usage

Run the following command:
```sh
python mosaic.py <target> <images> <block_size>
```

* `target`: the target image directory.
* `images`: the image directory to be used. A recursive search is used to find all the supported files.
To add other image formats, edit the code to add the format prefix to the global variable [IMAGE_FILE_FORMATS](https://github.com/nekrotzar/mosaic-cv/blob/master/mosaic.py#L9).
* `block_size`: the size of a mosaic square block (in pixels).

## Example
Using a custom dataset of images placed in /data/images:
```sh
python mosaic.py data/cat.jpg data/images 20
```

![Mosaic](data/cat.jpg "original")  |  ![Oricinal](data/out/mosaic-20-2320x3480.png "mosaic")
:-------------------------:|:-------------------------:
Original image (data/cat.jpg)             |  Mosaic output (data/out/mosaic-20-2320x3480)

The quality of the ouput is heavily dependent on the size and variety of your dataset.
