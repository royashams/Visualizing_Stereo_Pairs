import matplotlib.pyplot as plt
import cv2
import numpy as np
import random
import math

veronica_path = "st_veronica.jpg"
nike_path = "nike.jpg"
fountain_path = "fountain_path.jpg"

veronica_img = cv2.imread(veronica_path)
# veronica_img = cv2.cvtColor(veronica_img, cv2.COLOR_BGR2RGB)
veronica_left = cv2.imread("image_pairs/veronica_left.jpg")
# veronica_left = cv2.cvtColor(veronica_left, cv2.COLOR_BGR2RGB)
veronica_right = cv2.imread("image_pairs/veronica_right.jpg")
# veronica_right = cv2.cvtColor(veronica_right, cv2.COLOR_BGR2RGB)
# plt.imshow(veronica_img)
# plt.show()

print(veronica_left.shape)
print(veronica_right.shape)

# Converts colours of the rectified image to new image channels based on formulas from paper. 
def RectifiedToAnaglyph(img, other_img):
    # B = img[:,:, 0] is cool tho

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

    # TODO: MESS IT UP INTENTIONALLY
    # R = img.copy()
    # R[:,:,0] = 0
    # R[:,:,1] = 0
    
    # G = img.copy()
    # G[:,:,0] = 0
    # G[:,:,2] = 0

    # B = img.copy()
    # B[:,:,1] = 0
    # B[:,:,2] = 0



    # Now get intensity, hue, and saturation based on the minimal R, G, or B?
    #TODO: MINIMAL R G OR B

    # I = (R + G + B )/ 3
    # saturation = (B / I)
    # hue = (R - B) / (G - B)
    # # Am i supposed to find new saturation? ok whateer lets pretend there's new saturation
    # # Make sure your saturation is a good colo0ur - i think some weird colour clipping is happening if too high :/
    # new_saturation = saturation + 255
    # # I think the new_B might have some issues
    # new_B = I * (1 - new_saturation)
    # # new_R_top = (G + B - 2.0 * R) + 3.0 * I (R - B)
    # new_R_top = new_B * (G + B - 2.0 * R) + 3.0 * I * (R - B)
    # new_R_bottom = (R + G - 2.0 * B)
    # new_R = new_R_top / new_R_bottom

    # new_G_top = new_B * (R + B - 2.0 * G) + 3.0 * I *(G - B)
    # new_G_bottom =  (R + G - 2.0 * B)
    # new_G = new_G_top / new_G_bottom

    # result_img = np.zeros(img.shape)
    # # result_img[:, :, 0] = new_R[:, :, 0]
    # # result_img[:, :, 1] = new_B[:, :, 1]
    # # result_img[:, :, 2] = new_G[:, :, 2]
    # result_img = new_R + new_G + new_B
    # result_img = result_img

    result_img = img.copy()
    result_img[:, :, 2] = 0

    # Now with the other image, just get the R colour channel
    other_img_R = other_img.copy()
    other_img_R[:, :, 0] = 0
    other_img_R[:, :, 1] = 0
    other_img_R = other_img_R


    result_img = other_img_R + result_img
    cv2.imwrite("result_img.jpg", result_img)
    print(result_img)
    plt.imshow(result_img, vmin = 0, vmax = 1)
    plt.show()

    # OK So what this function does is basically separate into CYM - C is when blue is minimum.

def angle_between(p1, p2):
    ang1 = np.arctan2(*p1[::-1])
    ang2 = np.arctan2(*p2[::-1])
    return np.rad2deg((ang1 - ang2) % (2 * np.pi))

# RECYCLED A4 CODE
# Code taken from: https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_feature2d/py_matcher/py_matcher.html
def match_images(img1, img2, output_filename):
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

  eight_matches = matches[:16]
  angle_list = []
  pruned_matches = []
  # Weed out the bad matches
#   myradians = math.atan2(targetY-gunY, targetX-gunX)

  for match in matches:
    x1 = kp1[match.queryIdx].pt[0]
    y1 = kp1[match.queryIdx].pt[1]
    x2 = kp2[match.queryIdx].pt[0]
    y2 = kp2[match.queryIdx].pt[1]
    degrees = math.degrees(math.atan2(y2-y1, x2-x1))
    # print("AAAAAAA")
    # x_diff = abs(x1 - x2)
    # y_diff = abs(y2 - y1)
    # print(abs(x1 - x2), abs(y1 -y2))
    # print("yeet hay")
    # print(abs(abs(x1 - x2) - abs(y1 -y2)))
    dist = np.linalg.norm(np.array([x1, y1]) - np.array([x2, y2]))
    # if dist < 40 and abs(degrees) < 60:
    # if dist < 40:
    if dist < 30:
        angle_list.append(dist)
        pruned_matches.append(match)
        # print("degrees and dist")
        # print(degrees)
        # print(dist)

    # degrees = angle_between((x1, y1), (x2, y2))
    # if abs(degrees) > 300:
    #     angle_list.append(degrees)
    #     pruned_matches.append(match)

    # radian_list.append(myradians)
    # temp_img = cv2.drawMatches(img1,kp1,img2,kp2, match,None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    # plt.imshow(temp_img)
    # plt.show()
    # print(myradians)
#   radian_list.sort()
  print(angle_list)

  # Draw matches
  out_img = cv2.drawMatches(img1,kp1,img2,kp2, eight_matches ,None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

  cv2.imwrite(output_filename, out_img)
  return (out_img, eight_matches, kp1, kp2, des1, des2)

def rectify_image(img1, img2, left_points, right_points, F_matrix):
  # Get extrinsic and intrinsic parameters
  (ex, h1, h2) = cv2.stereoRectifyUncalibrated(left_points, right_points, F_matrix, img1.shape[:2])
  # Get combination transform and warp the image
  comb_trans = np.linalg.inv(h1).dot(h2)
  im_warp = cv2.warpPerspective(img1, comb_trans, (img2.shape[1], img1.shape[0]))
  return im_warp

left_points = []
right_points = []
matched = match_images(veronica_left, veronica_right, "veronica_match.jpg")
kp1 = matched[2]
kp2 = matched[3]
for match in matched[1]:
    p1 = kp1[match.queryIdx].pt
    p2 = kp2[match.trainIdx].pt
    # point_list.append((p1, p2))
    left_points.append(p1)
    right_points.append(p2)

left_points = np.array(left_points)
right_points = np.array(right_points)

fundamental_mat_leftright = cv2.findFundamentalMat(left_points, right_points)[0]
fundamental_mat_rightleft = cv2.findFundamentalMat(right_points, left_points)[0]
# fundamental_mat_leftright = cv2.findFundamentalMat(left_points, right_points, cv2.FM_8POINT)[0]
# fundamental_mat_rightleft = cv2.findFundamentalMat(right_points, left_points, cv2.FM_8POINT)[0]

rectified_first = rectify_image(veronica_left, veronica_right, left_points, right_points, fundamental_mat_leftright)
rectified_second = rectify_image(veronica_right, veronica_left, right_points, left_points, fundamental_mat_rightleft)
plt.imshow(rectified_first)
cv2.imwrite("rectified_first.jpg", rectified_first)
cv2.imwrite("rectified_second.jpg", rectified_second)


plt.show()



# RectifiedToAnaglyph(veronica_left, veronica_right)
RectifiedToAnaglyph(rectified_first, rectified_second)

# Good for veronica
stereo = cv2.StereoBM_create(numDisparities=16, blockSize=13)
# stereo = cv2.StereoBM_create(numDisparities=32, blockSize=15)

gray1 = cv2.cvtColor(rectified_first, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(rectified_second, cv2.COLOR_BGR2GRAY)

disparity = stereo.compute(gray1, gray2)
cv2.imwrite("disparity.jpg", disparity)
plt.imshow(disparity,'gray')
plt.show()