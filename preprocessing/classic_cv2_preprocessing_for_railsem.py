import cv2
import numpy as np
import time
import math

'''
def float_img_to_uint(img):
    uimg = img * 255
    uimg = uimg.astype(np.uint8)
    uimg = cv2.normalize(src=uimg, dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    return uimg
'''

def open_image(img_path):
    return cv2.imread(img_path, cv2.IMREAD_UNCHANGED)

def to_grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def open_grayscale(img_path):
    return cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)


def naive_remover(grayscale_img, REMOVED_PERCENT = 0.35):
    naive_mask = np.ones(grayscale_img.shape)
    height, _ = grayscale_img.shape[:2]

    naive_mask[0 : int(height * REMOVED_PERCENT), :] = 0
    naive_mask = cv2.convertScaleAbs(naive_mask)

    return cv2.bitwise_and(grayscale_img, grayscale_img, mask=naive_mask)
 
def sky_remover(grayscale_img):
    # Might work only on day imgs
    
    THRESHOLD = 170
    UPPER_PERCENTAGE = 0.9
    MAX_SKY_POLYGONS = 5

    ret, thresh_img = cv2.threshold(grayscale_img, THRESHOLD, 255, cv2.THRESH_BINARY)

    # cv2.imshow("threshold", thresh_img)
    # cv2.waitKey(0)

    contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    sky_countours = []
    height, _ = grayscale_img.shape[:2]

    for cidx, countour in enumerate(contours):
        upper_points = 0
        for point in countour:
            countour_point = point[0]
            if countour_point[1] < height // 2:
                upper_points += 1

        contour_upper_percetange = upper_points / len(countour)
        if contour_upper_percetange > UPPER_PERCENTAGE:
            sky_countours.append(countour)
        if cidx >= MAX_SKY_POLYGONS:
            break


    img_contours = np.zeros(grayscale_img.shape)
    cv2.drawContours(img_contours, sky_countours, -1, (255), 3)

    # cv2.imshow("countour", img_contours)
    # cv2.waitKey(0)

    for sky_countour in sky_countours:
        cv2.fillPoly(img_contours, pts =[sky_countour], color=(255))

    masked_sky_image = cv2.bitwise_not(cv2.convertScaleAbs(img_contours))

    return cv2.bitwise_and(grayscale_img, grayscale_img, mask=masked_sky_image)
    # cv2.imshow("filled", img_contours)
    # cv2.waitKey(0)

def get_countours(grayscale_img, MIN_LINES_IN_POLYGONE = 1, MAX_LINES_IN_POLYGONE = 7, MIN_PERIMETER = 600, MAX_PERIMETER = 5000, CANNY_THRESHOLD1=30, CANNY_THRESHOLD2=200):
    edged = cv2.Canny(grayscale_img, threshold1=CANNY_THRESHOLD1, threshold2=CANNY_THRESHOLD2)
    # cv2.imwrite("0canny.png", edged)
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # img_contours = np.zeros(grayscale_img.shape)
    # cv2.drawContours(img_contours, contours, -1, (255, 255, 255), 1)
    # cv2.imwrite("1contours.png", img_contours)

    new_contours = []
    # eliminated_countours = []
    # eliminated_countours2 = []
    # maxi = 0
    for c in contours:
        perimeter = cv2.arcLength(c, True)
        # print('Perimeter: ', perimeter)
        # if perimeter > maxi: 
        #    maxi = perimeter
        approx = cv2.approxPolyDP(c, 0.018 * perimeter, True)
        length = len(approx) 
        if perimeter > MIN_PERIMETER and perimeter < MAX_PERIMETER and length < MAX_LINES_IN_POLYGONE and length > MIN_LINES_IN_POLYGONE:
            new_contours.append(c)
            # else:
            #    eliminated_countours2.append(c)
        # else:
        #    eliminated_countours.append(c)

    # img_contours = np.zeros(grayscale_img.shape)
    to_be_returned = np.zeros(grayscale_img.shape)
    # cv2.drawContours(img_contours, new_contours, -1, (0,255,0), 3)
    # cv2.drawContours(img_contours, eliminated_countours, -1, (0, 0, 255), 3)
    # cv2.drawContours(img_contours, eliminated_countours2, -1, (255, 0, 0), 3)

    # cv2.imshow("countour2", img_contours)
    # cv2.waitKey(0)

    # cv2.imwrite("eliminated.png", img_contours)
    cv2.drawContours(to_be_returned, new_contours, -1, (255, 255, 255), 3)
    # cv2.imwrite("2contours.png", to_be_returned)
    return to_be_returned

'''
def draw_lines(lines, cdst, color=(0, 0, 255)):

  if lines is not None:
    for i in range(0, len(lines)):
      rho = lines[i][0][0]
      theta = lines[i][0][1]
      a = math.cos(theta)
      b = math.sin(theta)
      x0 = a * rho
      y0 = b * rho
      pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
      pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
      cv2.line(cdst, pt1, pt2, color, 2, cv2.LINE_AA)

  return cdst 

def draw_hl(dst, cdst):

  lines1 = cv2.HoughLines(image=dst, rho=1, theta=np.pi / 180, threshold=150, srn=None, stn=0, min_theta=0, max_theta=np.pi / 3)
  lines2 = cv2.HoughLines(image=dst, rho=1, theta=np.pi / 180, threshold=150, srn=None, stn=0, min_theta=np.pi * 3 / 4 , max_theta=np.pi)
       
  cdst = draw_lines(lines1, cdst)
  cdst = draw_lines(lines2, cdst, color=(255, 0, 0))

def hl_pipeline(countour_img, color_image):
  countour_img = resize_img(countour_img)
  color_image = resize_img(color_image)
  draw_hl(countour_img, color_image)
  return color_image

def resize_img(image_to_resize, new_width=1200):
    height, width = image_to_resize.shape[:2]
    ratio = height / width

    new_height = int(ratio * new_width)

    resized = cv2.resize(image_to_resize, (new_width, new_height), interpolation = cv2.INTER_CUBIC)
    return resized
'''

img_path1 = "test_img/rs00027.jpg"
img_path2 = "test_img/rs00155.jpg"
img_path3 = "test_img/rs00397.jpg"

def classic_cv_pipeline(img_path, REMOVED_PERCENT = 0.35, MIN_LINES_IN_POLYGONE = 1, MAX_LINES_IN_POLYGONE = 10, MIN_PERIMETER = 600, MAX_PERIMETER = 5000, CANNY_THRESHOLD1=30, CANNY_THRESHOLD2=200):

    # img = open_image(img_path)
    grayscale_img = open_grayscale(img_path)
    start = time.time()
    # grayscale_img = to_grayscale(img)
    # cv2.imwrite("00grayscale.png", grayscale_img)
    # start = time.time()
    
    sky_removed = naive_remover(grayscale_img, REMOVED_PERCENT)
    # cv2.imwrite("00naive.png", sky_removed)
    
    result = get_countours(sky_removed,  MIN_LINES_IN_POLYGONE, MAX_LINES_IN_POLYGONE, MIN_PERIMETER, MAX_PERIMETER, CANNY_THRESHOLD1, CANNY_THRESHOLD2)
    end = time.time()
    # cv2.imwrite("classic_cv/countour_" + img_path.split('/')[-1], result)
    # print(end - start)
    cv2.imwrite("classic_cv/" + img_path.split('/')[-1], result)
# cv2.imshow("results", result)
# cv2.waitKey(0)
classic_cv_pipeline(img_path1)
'''

result2 = cv2.imread("classic_cv/countour.png", cv2.IMREAD_GRAYSCALE)
hl_image = hl_pipeline(result2, result)

cv2.imshow("HL", hl_image)
cv2.waitKey(0)
'''



