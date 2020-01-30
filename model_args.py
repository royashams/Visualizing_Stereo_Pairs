import os
import argparse
import numpy as np
import cv2

cwd = os.getcwd()
# string $disparity_path = "/Users/royashams/Documents/Visualizing_Stereo_Pairs/Blurred/middlebury_veronica.jpg";
# string $colour_path = "/Users/royashams/Documents/Visualizing_Stereo_Pairs/image_pairs/veronica_left.jpg";
# float $disparity_height = 0.2;
# float $img_width = 3.84;
# float $img_height = 5.89;

# print(cwd)
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("colour_image")
    # Technique refers to the usage of outputting anaglyph images or the disparity for a 3D model.
    parser.add_argument("disparity_image")
    parser.add_argument("disparity_height")
    args = parser.parse_args()

    colour_image = args.colour_image
    disparity_image = args.disparity_image
    disparity_height = args.disparity_height

    # Get current paths for each image
    colour_path = cwd + "/image_pairs/" + colour_image
    disparity_path = cwd + "/Blurred/" + disparity_image

    # Read images and get their dimensions
    colour_image = cv2.imread(colour_path)
    disparity_image = cv2.imread(disparity_path)

    width = colour_image.shape[1] / 100.0
    height = colour_image.shape[0] / 100.0

    # Now that we have all of our variable values, convert them to strings and print
    mel_disparity = 'string $disparity_path = "{}";'.format(disparity_path)
    mel_colour = 'string $colour_path = "{}";'.format(colour_path)
    mel_disparity_height = 'float $disparity_height = {};'.format(disparity_height)
    mel_width = 'float $img_width = {};'.format(width)
    mel_height = 'float $img_height = {};'.format(height)

    print(mel_colour)
    print(mel_disparity)
    print(mel_disparity_height)
    print(mel_width)
    print(mel_height)

    # print(width)
    # print(height)


    # print(colour_path)
    # print(disparity_path)
    # print(disparity_height)




