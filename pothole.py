import numpy as np
import matplotlib.pyplot as plt
import cv2

def ellipse_area(x,y):
    area = 3.142*x*y/4
    return area

def region_of_interest(image):
    height = image.shape[0]
    width = image.shape[1]
    polygons = np.array([[(0, height*0.8), (0, height), (width, height), (width, height*0.8), (width*0.50, height*0.10)]], dtype='int32')
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image

def canny_img(image):
    gauss_h = 3
    gauss_w = 3
    canny_det_edge1 = 50
    canny_det_edge2 = 150
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (gauss_h, gauss_w), 0)
    #noise= cv2.fastNlMeansDenoising(blur)
    canny = cv2.Canny(gray, canny_det_edge1, canny_det_edge2)
    return canny

img = cv2.imread("C:/Users/Sanket/AppData/Local/Programs/Python/Python36/projects/roads/4.jpg")
copy = np.copy(img)
img2 = region_of_interest(copy)

canny_image1 = canny_img(img2)
coun, hier = cv2.findContours(canny_image1,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

print("Number of contours =" + str(len(coun)))

minEllipse = [None]*len(coun)
for i, c in enumerate(coun):
    color = (0, 255, 0)
    if c.shape[0] > 5:
        minEllipse[i] = cv2.fitEllipse(c)
        height = cv2.fitEllipse(c)[1][0]
        width = cv2.fitEllipse(c)[1][1]
        angle = cv2.fitEllipse(c)[2]
        #print(minEllipse[i])
        if ellipse_area(height, width) > 400.0 and angle < 110 and angle > 80 :
            cv2.ellipse(img, minEllipse[i], color, 2)
            print(minEllipse[i])

print(minEllipse[1])

#cv2.imshow('Contours', canny_image1)
cv2.imshow('ellipses', img)
cv2.waitKey(0)
