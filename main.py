# Main file for running both parts of the CSC420 Final Project for Visualizing Stereo Pairs.
import matplotlib.pyplot as plt
import cv2
import numpy as np
import random
import math
import argparse
import subprocess

# Converts colours of the rectified image to new image channels based on formulas from paper. 
# image_name is the name of the image (eg. veronica), and rectified specifies if this is 
# simple parallel compositing or using the rectified images. 
def AnaglyphColoring(image_name, img, other_img, rectified=False):
    # Separate image into channels
    R = img.copy()
    R[:,:,1] = 0
    R[:,:,2] = 0
    
    G = img.copy()
    G[:,:,0] = 0
    G[:,:,2] = 0

    B = img.copy()
    B[:,:,0] = 0
    B[:,:,1] = 0

    result_img = img.copy()
    result_img[:, :, 2] = 0

    # Now with the other image, just get the R colour channel
    other_img_R = other_img.copy()
    other_img_R[:, :, 0] = 0
    other_img_R[:, :, 1] = 0
    other_img_R = other_img_R

    result_img = other_img_R + result_img
    if rectified == True:
        cv2.imwrite("Anaglyphs/" + image_name + "_anaglyph_rectified" + ".jpg", result_img)
    else:
        cv2.imwrite("Anaglyphs/" + image_name + "_anaglyph.jpg", result_img)
    return result_img

# A4 Code with slight modifications. 
# Code taken from: https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_feature2d/py_matcher/py_matcher.html
def MatchImages(img1, img2, output_filename, image_name):
    # Using ORB descriptors instead of SIFT
    # Initiate ORB detector
    orb = cv2.ORB_create()
    # find the keypoints and descriptors with ORB
    kp1, des1 = orb.detectAndCompute(img1,None)
    kp2, des2 = orb.detectAndCompute(img2,None)

    # create BFMatcher object
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    # Match descriptors.
    matches = bf.match(des1,des2)
    # Sort them in the order of their distance.
    matches = sorted(matches, key = lambda x:x.distance)

    chosen_matches = []
    # Sometimes, choosing all matches vs. the best 16 matches in the algorithm yields different results 
    # on a case-by-case basis. 
    # For the "foot" and "fountain" images, choosing all of the matches is better.
    # For the "nike" and "veronica" images, choosing the best 16 is better. 
    if image_name == "foot" or "fountain":
        chosen_matches = matches
    else:
        chosen_matches = matches[:16]

    #   # OPTIONAL 
    #   # Weed out the bad matches
    #   angle_list = []
    #   pruned_matches = []

    #   for match in matches:
    #     x1 = kp1[match.queryIdx].pt[0]
    #     y1 = kp1[match.queryIdx].pt[1]
    #     x2 = kp2[match.queryIdx].pt[0]
    #     y2 = kp2[match.queryIdx].pt[1]
    #     # degrees = math.degrees(math.atan2(y2-y1, x2-x1))
    #     dist = np.linalg.norm(np.array([x1, y1]) - np.array([x2, y2]))
    #     if dist < 30:
    #         angle_list.append(dist)
    #         pruned_matches.append(match)

    # Draw matches
    out_img = cv2.drawMatches(img1,kp1,img2,kp2, chosen_matches ,None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    # OPTIONAL: If you want to use my pruning algorithm that I attempted to write, uncomment the line below
    # out_img = cv2.drawMatches(img1,kp1,img2,kp2, pruned_matches ,None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    cv2.imwrite(output_filename, out_img)
    return (out_img, chosen_matches, kp1, kp2, des1, des2)
    # OPTIONAL: If you want to use my pruning algorithm that I attempted to write, uncomment the line below
    # return (out_img, pruned_matches, kp1, kp2, des1, des2)


def RectifyImage(img1, img2, left_points, right_points, F_matrix):
  # Get extrinsic and intrinsic parameters
  (ex, h1, h2) = cv2.stereoRectifyUncalibrated(left_points, right_points, F_matrix, img1.shape[:2])
  # Get combination transform and warp the image
  comb_trans = np.linalg.inv(h1).dot(h2)
  im_warp = cv2.warpPerspective(img1, comb_trans, (img2.shape[1], img1.shape[0]))
  return im_warp

def OutputRectified(img1, img2, image_name):
    left_points = []
    right_points = []
    matched = MatchImages(img1, img2, "Matched/" + image_name + "_match.jpg", image_name)
    kp1 = matched[2]
    kp2 = matched[3]
    for match in matched[1]:
        p1 = kp1[match.queryIdx].pt
        p2 = kp2[match.trainIdx].pt
        left_points.append(p1)
        right_points.append(p2)

    left_points = np.array(left_points)
    right_points = np.array(right_points)

    fundamental_mat_leftright = cv2.findFundamentalMat(left_points, right_points)[0]
    fundamental_mat_rightleft = cv2.findFundamentalMat(right_points, left_points)[0]

    rectified_first = RectifyImage(img1, img2, left_points, right_points, fundamental_mat_leftright)
    rectified_second = RectifyImage(img2, img1, right_points, left_points, fundamental_mat_rightleft)
    plt.imshow(rectified_first)
    cv2.imwrite("Rectified/" + image_name + "_rectified_first.jpg", rectified_first)
    cv2.imwrite("Rectified/" + image_name + "_rectified_second.jpg", rectified_second)

    return (rectified_first, rectified_second)

# Run the Middlebury Stereo Evaluation SDK
def RunMiddlebury(img1, img2, image_name):
    # In case there are no png files yet in the appropriate directory, write them
    cv2.imwrite("MiddEval3/alg-ELAS/" + image_name + "_left.png", img1)
    cv2.imwrite("MiddEval3/alg-ELAS/" + image_name + "_right.png", img2)
    
    # I wrote a shell script that will take these two images and run the Middlebury evaluation.
    subprocess.call(["./middlebury.sh", image_name + "_right.png", image_name + "_left.png", image_name])
    # Now that the png file is generated, read this black and white image and return.
    binary_disp = cv2.imread("MiddleburyDisparity/" + image_name +  "_binary_disp.png")
    return binary_disp

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # Image name refers to the prefix of the image pair. images are named like:
    # veronica, foot, nike, etc. they are attached to the suffix
    # veronica_left, foot_right, etc. 
    # this program *assumes* there is already a left and right image pair for the given image name.
    # inside of the folder image_pairs/
    parser.add_argument("image_name")
    # Technique refers to the usage of outputting anaglyph images or the disparity for a 3D model.
    parser.add_argument("technique")
    args = parser.parse_args()
    print("Image Name : " + args.image_name)
    image_name = args.image_name
    technique = args.technique

    if technique == "1":
        print("Running Anaglyphs...")
        first_image = cv2.imread("image_pairs/" + image_name + "_left.jpg")
        second_image = cv2.imread("image_pairs/" + image_name + "_right.jpg")
        # Run this normally on the original two images
        original_anaglyph = AnaglyphColoring(image_name, first_image, second_image, False)
        # Now get rectified images
        rectified_pair = OutputRectified(first_image, second_image, image_name)
        rectified_anaglyph = AnaglyphColoring(image_name, rectified_pair[0], rectified_pair[1], True)
        plt.imshow(original_anaglyph)
        plt.show()
        plt.imshow(rectified_anaglyph)
        plt.show()

    elif technique == "2":
        print("Running Disparity Map Generation...")
        first_image = cv2.imread("image_pairs/" + image_name + "_left.jpg", cv2.CV_8UC1)
        second_image = cv2.imread("image_pairs/" + image_name + "_right.jpg", cv2.CV_8UC1)
        disp_choice = raw_input("Press A to run Middlebury or B to run StereoBM: \n")
        kernel = int(raw_input("\nChoose an odd number as the kernel size for Gaussian Blur\n"))
        if disp_choice == "A":
            print("Running Middlebury using Gaussian Blur kernel of " + str(kernel))
            # Run the Middlebury script
            middlebury_disp = RunMiddlebury(first_image, second_image, image_name)
            plt.imshow(middlebury_disp)
            plt.show()
            # Apply a Gaussian kernel over this image
            middlebury_blur = cv2.GaussianBlur(middlebury_disp,(kernel,kernel),0)
            cv2.imwrite("Blurred/middlebury_" + image_name + ".jpg",middlebury_blur)
            plt.imshow(middlebury_blur)
            plt.show()
            print("Done! Check the output in /Blurred or /MiddleburyDisparity")

        elif disp_choice == "B":
            print("Running StereoBM using Gaussian Blur kernel of " + str(kernel))
            stereo = cv2.StereoBM_create(numDisparities=16, blockSize=7)
            stereoBM_disp = stereo.compute(second_image, first_image)
            cv2.imwrite("StereoBM_Disparity/_" + image_name + "_disp.png", stereoBM_disp)
            plt.imshow(stereoBM_disp, 'gray')
            plt.show()
            # Apply a Gaussian kernel over this image
            stereoBM_blur = cv2.GaussianBlur(stereoBM_disp,(kernel,kernel),0)
            cv2.imwrite("Blurred/stereoBM_" + image_name + ".jpg", stereoBM_blur)
            plt.imshow(stereoBM_blur, 'gray')
            plt.show()
            print("Done! Check the output in /Blurred or /StereoBM_Disparity")
    else:
        print("Error: Please choose 1 for Anaglyphs or 2 for Disparity Map Generation.")
    
    
