import os
import time 
import argparse

import cv2 as cv
import numpy as np
import progress.bar

IMAGE_FILE_FORMATS = ['.JPG', '.jpg', '.png']

def average_color(data):
    '''Get the average color.

    Args:
        data (np.ndarray): a array of arrays of length 3 containing an RGB colors.
        block_size (int): the size of a mosaic block

    Returns:
        np.ndarray: arrays of length 3 containing the average color
    '''
    average_row_color = np.average(data, axis=0)
    average_color = np.average(average_row_color, axis=0)

    return average_color

def find_best_match(block, target_value, data):
    '''Get best fit from dataset.

    Args:
        block (numpy.ndarray): a block from the target image.
        target_value (numpy.ndarray): the target metric value. In this instance, we use an RGB color array.
        data (list): the blocks processed from the dataset.

    Returns:
        numpy.ndarray: a block that best matches the color
    '''
    min_distance = np.Infinity
    best_match = None

    for candidate in data:
        color = average_color(candidate)
        distance = np.linalg.norm(target_value - color)

        if distance < min_distance:
            min_distance = distance
            best_match = candidate

    return best_match

def analyse_dataset(files_path, block_size):
    '''Analyze a directory and store images 

    Args:
        files_path (str): dataset path
        block_size (int): size of the mosaic block (in pixels)

    Returns:
        list: a list containing the images found on files_path
    '''
    data = []
    start = time.time()
    
    print("Analysing dataset...")
    for (root, _, filenames) in os.walk(files_path):       
        for filename in filenames:
            if filename[-4:] in IMAGE_FILE_FORMATS:
                path = os.path.join(root, filename)
                proc = process_image(path, block_size)
                data.append(proc)

    print('Processed {0} images in {1:.2f}s'.format(len(data), time.time() - start))
    return data

def process_image(path, size):
    '''Crop and resize image according to the block size.

    Args:
        path (str): target image directory
        size (int): size of the mosaic block (in pixels)

    Returns:
        np.ndarray: an array containing bgr color values
    '''
    image = cv.imread(path)
    height, width = image.shape[0], image.shape[1]

    # Crop image in order to avoid distortion
    min_dim = np.min((height, width))
    w_crop = int((width-min_dim) / 2)
    h_crop = int((height-min_dim) / 2)
    crop = image[h_crop:height-h_crop, w_crop:width-w_crop]

    # Resize cropped image to target block size
    final = cv.resize(crop, (size, size))
    return final

def generate_mosaic(target_path, data_path, block_size=50, target_scale=1):
    '''Generate photomosaic.

    Args:
        target_path (str): target image directory
        data_path (str): dataset images directory
        block_size (int, optional): size of the mosaic block (in pixels). Defaults to 20.
        target_scale (int, optional): the scale of the output image. Defaults to 1.
    '''
    start = time.time()
    image_data = analyse_dataset(data_path, block_size=block_size)

    # Read target image
    target = cv.imread(target_path)
    target = cv.resize(target, None, fx=target_scale, fy=target_scale, interpolation=cv.INTER_AREA)
    height, width = target.shape[:2]

    # Crop image to fit an integer number of mosaic blocks per row and column
    w_crop = int((width % block_size))
    h_crop = int((height % block_size))

    if w_crop or h_crop:
        w_adjust = 1 if (w_crop % 2) else 0
        h_adjust = 1 if (h_crop % 2) else 0
        min_h, min_w = int(h_crop/2), int(w_crop/2)
        target = target[min_h:height-(min_h + h_adjust), min_w: width-(min_w + w_adjust)]

    # Create blank image with target dimensions
    output = np.zeros(target.shape, dtype=np.uint8)
    (height, width) = output.shape[:2]

    row_size = int(height / block_size)
    col_size = int(width / block_size)
    n_blocks = row_size * col_size
    print("\tNumber of mosaic blocks: {0} rows x {1} cols = {2}".format(row_size, col_size, n_blocks))    

    try:
        pbar = progress.bar.IncrementalBar('Building mosaic', max=n_blocks)
        for r in range(row_size):
            for c in range(col_size):
                h_pos = (block_size * r)
                w_pos = (block_size * c)

                block = target[h_pos:h_pos+block_size, w_pos:w_pos+block_size]

                # Use average color as metric for block similarity
                metric_value = average_color(block)
                block = find_best_match(block, metric_value, image_data)
                
                # Fill output with average color
                output[h_pos:h_pos+block_size, w_pos:w_pos+block_size] = block
                pbar.next()
        pbar.finish()
    except KeyboardInterrupt:
        pbar.finish()
        cv.imwrite('mosaic.png', output)
        message = '[ERROR] Mosaic construction interrupted!'
    else:
        message = '[INFO] Mosaic construction complete'
    
    print(message + 'Elapsed time: {0:.2f}'.format(time.time()-start))
    cv.imwrite('data/out/mosaic-{0}-{1}x{2}.png'.format(block_size, width, height), output)

def main():
    parser = argparse.ArgumentParser(description="Generate a mosaic from an image")
    parser.add_argument("target", help="The target image path")
    parser.add_argument("images", help="The image directory to be used")
    parser.add_argument("block_size", help="The height/width of a mosaic block in pixels")
    args = parser.parse_args()

    generate_mosaic(args.target, args.images, block_size=int(args.block_size), target_scale=1)

if __name__ == "__main__":
    main()
