import cv2
import numpy as np
import math
#from moviepy.editor import VideoFileClip


# image = cv2.imread('lane3.jpg',1)
#cap = cv2.VideoCapture('solidWhiteRight.mp4')
video_capture = cv2.VideoCapture('a.mp4')

def draw_lines(img, lines, color=[0, 255, 0], thickness=3):

    
    # blank image is created.
    line_img = np.zeros((img.shape[0],img.shape[1],3),dtype=np.uint8,)

    # Drawing lines over the image
    if line is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_img, (x1, y1), (x2, y2), color, thickness)

    # Imposing it ove the original image
    img = cv2.addWeighted(img, 0.8, line_img, 1.0, 0.0)

    return img


def ImageProcess(img):
    
    # Image is converted in Gray Scale.

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Image is converted to HSV image.

    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Now we set range for colors we want to extract from the image
    # We are interested in Yellow and White color

    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])

    # Now we will make a mask for our image which will specify the colors of interest in our image.
    # We will create mask for each color.

    mask_yellow = cv2.inRange(hsv_img, lower_yellow, upper_yellow)
    mask_white = cv2.inRange(gray_img, 200, 255)

    # Now we make a combine mask of both yellow and white color

    mask_yw = cv2.bitwise_or(mask_yellow, mask_white)

    # Now we will apply it to our gray scale image

    mask_img_yw = cv2.bitwise_and(gray_img, mask_yw)

    # Now we will apply Gaussian Blur to our image
    # Best results are shown for kernel size (5,5)

    gauss_img = cv2.GaussianBlur(mask_img_yw, (5,5), 0)

    # Now we will find the edges in the image by canny edge algorithm
    # We define low threshold and high threshold
    # Recommended ratio for high and low threshold value should be 1:3 or 1:2

    low_threshold = 100
    high_threshold = 150

    canny_edge_img = cv2.Canny( gauss_img, low_threshold, high_threshold)

    # Now we are going to mark our ROI i.e. Region of interest
    # First we create a mask of similar size of our image

    blank_mask = np.zeros_like(canny_edge_img)

    # Then we assign colour to our region according to number of channels in our image

    if len(canny_edge_img.shape) > 2:
        no_of_channels = canny_edge_img.shape[2]
        color_blank = (255,)*no_of_channels

    else:
        color_blank = 255
        
    # Now we will define the dimensions of box which is our region of interest
    # Arrange vertices in Clockwise direction
    img_shape = canny_edge_img.shape
    upper_right = [0.57*img_shape[1], img_shape[0]*0.40]
    lower_right = [img_shape[1]*0.95 , img_shape[0]]
    lower_left = [0, img_shape[0]*0.9] 
    upper_left = [img_shape[1]*0.380 , img_shape[0]*0.4]
    temp1 = [img_shape[1]*0.4 , img_shape[0]*0.4]
    temp2 = [0, img_shape[0]]
    temp3 = [img_shape[1]*0.85, img_shape[0]]
    temp4 = [0.55*img_shape[1], img_shape[0]*0.40]
    temp5 = [0, img_shape[0]]
    vertices = [ np.array([lower_left, upper_left, temp1, temp2, temp3, temp4, upper_right, lower_right,temp5], dtype=np.int32)]

    # We make the ROI of white color and apply it on our blank mask

    cv2.fillPoly(blank_mask, vertices, color_blank)

    # Now we will apply our blank mask on our image to get our ROI

    ROI_img = cv2.bitwise_and(canny_edge_img, blank_mask)

    # Now we will apply Hough Transform to make lines on our edges in our image

    #threshold = 20
    #min_line_len = 50
    #max_line_gap = 200
    lines = cv2.HoughLinesP(
        ROI_img,
        rho=2,
        theta=np.pi / 180,
        threshold=20,
        lines=np.array([]),
        minLineLength=50,
        maxLineGap=150
    )

# This will print the coordinates of line joining points.
    print(lines)

# Now we will make the right and left into a single lane.

    lx_line = []
    ly_line = []
    rx_line = []
    ry_line = []
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                slope = (y2 - y1) / (x2 - x1) 
                if math.fabs(slope) < 0.5: 
                    continue
                if slope <= 0: 
                    lx_line.extend([x1, x2])
                    ly_line.extend([y1, y2])
                else: 
                    rx_line.extend([x1, x2])
                    ry_line.extend([y1, y2])

    yMin = img.shape[0] * (3 / 5) 
    yMax = img.shape[0] 

    poly_left = np.poly1d(np.polyfit( ly_line, lx_line, deg=1))

    lStart_x = int(poly_left(yMax))
    lEnd_x = int(poly_left(yMin))

    poly_right = np.poly1d(np.polyfit( ry_line, rx_line, deg=1))

    rStart_x = int(poly_right(yMax))
    rEnd_x = int(poly_right(yMin))

    line_image = draw_lines(image,[[ [int(lStart_x), int(yMax), int(lEnd_x), int(yMin)], [int(rStart_x), int(yMax), int(rEnd_x), int(yMin)],]], thickness=5,)

    return line_image


    """
while True:
    ret,frame = video_capture.read()
    final_image =  ImageProcess(frame)

    cv2.imshow('image',final_image)
    cv2.waitkey(0)

video_capture.release()    
cv2.destroyAllWindows()
