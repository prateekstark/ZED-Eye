import cv2
import sys
import numpy as np
import pyzed.sl as sl
import numpy as np

# video_capture = cv2.VideoCapture(0)

video_capture = cv2.VideoCapture('a.mp4')
# out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (width,height))

# def open_zed():
#     print("Running...")
#     init = sl.InitParameters()
#     cam = sl.Camera()
#     if not cam.is_opened():
#         print("Opening ZED Camera...")
#     status = cam.open(init)
#     if status != sl.ERROR_CODE.SUCCESS:
#         print(repr(status))
#         exit()

#     runtime = sl.RuntimeParameters()
#     mat = sl.Mat()

 
#     key = ''
#     while key != 113:  # for 'q' key
#         err = cam.grab(runtime)
#         if err == sl.ERROR_CODE.SUCCESS:
#             cam.retrieve_image(mat, sl.VIEW.VIEW_LEFT)
#             instance_image = cv2.imread(mat.get_data(),0)


#             out_path = os.getcwd();
#             in_image = cv2.cvtColor(instance_image, cv2.COLOR_BGR2RGB)
#             plt.imshow("hi",in_image)
#             return
#             out_image = color_frame_pipeline([in_image], solid_lines=True)
#             cv2.imwrite(out_path, cv2.cvtColor(out_image, cv2.COLOR_RGB2BGR))
#             plt.imshow(out_image)
#             # print("hello")
            


#             plt.waitforbuttonpress()
#             plt.close('all')
            

#             # cv2.imshow("ZED", mat.get_data())
#             key = cv2.waitKey(5)
#             settings(key, cam, runtime, mat)
#         else:
#             key = cv2.waitKey(5)
#     cv2.destroyAllWindows()

#     cam.close()
#     print("\nFINISH")



# def settings(key, cam, runtime, mat):
#     if key == 115:  # for 's' key
#         switch_camera_settings()
#     elif key == 43:  # for '+' key
#         current_value = cam.get_camera_settings(camera_settings)
#         cam.set_camera_settings(camera_settings, current_value + step_camera_settings)
#         print(str_camera_settings + ": " + str(current_value + step_camera_settings))
#     elif key == 45:  # for '-' key
#         current_value = cam.get_camera_settings(camera_settings)
#         if current_value >= 1:
#             cam.set_camera_settings(camera_settings, current_value - step_camera_settings)
#             print(str_camera_settings + ": " + str(current_value - step_camera_settings))
#     elif key == 114:  # for 'r' key
#         cam.set_camera_settings(sl.CAMERA_SETTINGS.CAMERA_SETTINGS_BRIGHTNESS, -1, True)
#         cam.set_camera_settings(sl.CAMERA_SETTINGS.CAMERA_SETTINGS_CONTRAST, -1, True)
#         cam.set_camera_settings(sl.CAMERA_SETTINGS.CAMERA_SETTINGS_HUE, -1, True)
#         cam.set_camera_settings(sl.CAMERA_SETTINGS.CAMERA_SETTINGS_SATURATION, -1, True)
#         cam.set_camera_settings(sl.CAMERA_SETTINGS.CAMERA_SETTINGS_GAIN, -1, True)
#         cam.set_camera_settings(sl.CAMERA_SETTINGS.CAMERA_SETTINGS_EXPOSURE, -1, True)
#         cam.set_camera_settings(sl.CAMERA_SETTINGS.CAMERA_SETTINGS_WHITEBALANCE, -1, True)
#         print("Camera settings: reset")
#     elif key == 122:  # for 'z' key
#         record(cam, runtime, mat)



# init = sl.InitParameters()
# cam = sl.Camera()
# if not cam.is_opened():
#     print("Opening ZED Camera...")
# status = cam.open(init)
# if status != sl.ERROR_CODE.SUCCESS:
#     print(repr(status))
#     exit()
# runtime = sl.RuntimeParameters()
# mat = sl.Mat()
# key = ''
# while key != 113:  # for 'q' key
#     err = cam.grab(runtime)
#     if err == sl.ERROR_CODE.SUCCESS:
#         cam.retrieve_image(mat, sl.VIEW.VIEW_LEFT)
#         cv2.imshow("ZED", mat.get_data())
#         key = cv2.waitKey(5)
#         settings(key, cam, runtime, mat)
#     else:
#         key = cv2.waitKey(5)
# cv2.destroyAllWindows()




frame_width = int(video_capture.get(3))
frame_height = int(video_capture.get(4))

out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))






while True:
    

    ret, frame = video_capture.read()
    
    gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    mask_white = cv2.inRange(gray_img, 30, 50)
    mask_yellow = cv2.inRange(gray_img, 80, 100)
    mask_white = cv2.bitwise_or(mask_white, mask_yellow)
    # cv2.imshow("hello",mask_white)

    gauss_img = cv2.GaussianBlur(mask_white, (5,5), 0)

    low_threshold = 50
    high_threshold = 150

    canny_edge_img = cv2.Canny( gauss_img, low_threshold, high_threshold)


    blank_mask = np.zeros_like(canny_edge_img)

    if len(canny_edge_img.shape) > 2:
        no_of_channels = canny_edge_img.shape[2]
        color_blank = (255,)*no_of_channels

    else:
        color_blank = 255



    img_shape = canny_edge_img.shape
    print(img_shape)
    print("My-Shape")
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


    cv2.fillPoly(blank_mask, vertices, color_blank)
    cv2.imshow('achank',blank_mask)


    ROI_img = cv2.bitwise_and(canny_edge_img, blank_mask)


    lines = cv2.HoughLinesP(
        ROI_img,
        rho=2,
        theta=np.pi / 180,
        threshold=10,
        lines=np.array([]),
        minLineLength=40,
        maxLineGap=160
    )
    line_img = np.zeros((ROI_img.shape[0], ROI_img.shape[1], 3), dtype=np.uint8)

    # print(lines)
    # if lines:
    if lines is not None:
        for line in lines:
            # print(line)
            for x1,y1,x2,y2 in line:
                cv2.line(line_img,(x1,y1),(x2,y2), [0,255,0], 2)

    frame1 = cv2.addWeighted(frame, 0.8, line_img, 1.0, 0.0)
    out.write(frame1)
    cv2.imshow('Video', frame1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()