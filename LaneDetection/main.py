import matplotlib.pyplot as plt
import cv2
import os
from os.path import join, basename
from collections import deque
from lane_detection import color_frame_pipeline
import pyzed.sl as sl
import numpy as np



#####################################################################################################
# if __name__ == '__main__':

#     resize_h, resize_w = 540, 960

#     verbose = True
#     if verbose:
#         plt.ion()
#         figManager = plt.get_current_fig_manager()
#         # figManager.window.showMaximized()
#         plt.show()

#     # test on images/
#     test_images_dir = join('data', 'test_images')
#     test_images = [join(test_images_dir, name) for name in os.listdir(test_images_dir)]

#     for test_img in test_images:

#         print('Processing image: {}'.format(test_img))

#         out_path = join('out', 'images', basename(test_img))
#         in_image = cv2.cvtColor(cv2.imread(test_img, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
#         print(type(in_image))

#         print("helo")
#         out_image = color_frame_pipeline([in_image], solid_lines=True)
#         cv2.imwrite(out_path, cv2.cvtColor(out_image, cv2.COLOR_RGB2BGR))
#         if verbose:
#             plt.imshow(out_image)
#             plt.waitforbuttonpress()
#     plt.close('all')








#####################################################################################################
    # test on videos
# Open zed camera**************************************************************************************

def open_zed():
    print("Running...")
    init = sl.InitParameters()
    cam = sl.Camera()
    if not cam.is_opened():
        print("Opening ZED Camera...")
    status = cam.open(init)
    if status != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit()

    runtime = sl.RuntimeParameters()
    mat = sl.Mat()

 
    key = ''
    while key != 113:  # for 'q' key
        err = cam.grab(runtime)
        if err == sl.ERROR_CODE.SUCCESS:
            cam.retrieve_image(mat, sl.VIEW.VIEW_LEFT)
            instance_image = cv2.imread(mat.get_data(),0)


            out_path = os.getcwd();
            in_image = cv2.cvtColor(instance_image, cv2.COLOR_BGR2RGB)
            plt.imshow("hi",in_image)
            return
            out_image = color_frame_pipeline([in_image], solid_lines=True)
            cv2.imwrite(out_path, cv2.cvtColor(out_image, cv2.COLOR_RGB2BGR))
            plt.imshow(out_image)
            # print("hello")
            


            plt.waitforbuttonpress()
            plt.close('all')
            

            # cv2.imshow("ZED", mat.get_data())
            key = cv2.waitKey(5)
            settings(key, cam, runtime, mat)
        else:
            key = cv2.waitKey(5)
    cv2.destroyAllWindows()

    cam.close()
    print("\nFINISH")



def settings(key, cam, runtime, mat):
    if key == 115:  # for 's' key
        switch_camera_settings()
    elif key == 43:  # for '+' key
        current_value = cam.get_camera_settings(camera_settings)
        cam.set_camera_settings(camera_settings, current_value + step_camera_settings)
        print(str_camera_settings + ": " + str(current_value + step_camera_settings))
    elif key == 45:  # for '-' key
        current_value = cam.get_camera_settings(camera_settings)
        if current_value >= 1:
            cam.set_camera_settings(camera_settings, current_value - step_camera_settings)
            print(str_camera_settings + ": " + str(current_value - step_camera_settings))
    elif key == 114:  # for 'r' key
        cam.set_camera_settings(sl.CAMERA_SETTINGS.CAMERA_SETTINGS_BRIGHTNESS, -1, True)
        cam.set_camera_settings(sl.CAMERA_SETTINGS.CAMERA_SETTINGS_CONTRAST, -1, True)
        cam.set_camera_settings(sl.CAMERA_SETTINGS.CAMERA_SETTINGS_HUE, -1, True)
        cam.set_camera_settings(sl.CAMERA_SETTINGS.CAMERA_SETTINGS_SATURATION, -1, True)
        cam.set_camera_settings(sl.CAMERA_SETTINGS.CAMERA_SETTINGS_GAIN, -1, True)
        cam.set_camera_settings(sl.CAMERA_SETTINGS.CAMERA_SETTINGS_EXPOSURE, -1, True)
        cam.set_camera_settings(sl.CAMERA_SETTINGS.CAMERA_SETTINGS_WHITEBALANCE, -1, True)
        print("Camera settings: reset")
    elif key == 122:  # for 'z' key
        record(cam, runtime, mat)

open_zed()


# Open zed camera**************************************************************************************

# ***********************************MY CODE*********************************************

# camera_directory = "~/../../usr/local/zed/tools/ZED\\ Explorer"
# cap = cv2.VideoCapture(1)

# # Check if camera opened successfully
# if (cap.isOpened()== False): 
#   print("Error opening video stream or file")
 
# # Read until video is completed
# while(cap.isOpened()):
#   # Capture frame-by-frame
#   ret, frame = cap.read()
#   if ret == True:
 
#     # Display the resulting frame
#     cv2.imshow('Frame',frame)
 
#     # Press Q on keyboard to  exit
#     if cv2.waitKey(25) & 0xFF == ord('q'):
#       break
 
#   # Break the loop
#   else: 
#     break
 
# # When everything done, release the video capture object
# cap.release()
 
# # Closes all the frames
# cv2.destroyAllWindows()








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







# print('Processing video: {}'.format(cap))


# out = cv2.VideoWriter(join('out', 'videos', basename(cap)),
#                           fourcc=cv2.VideoWriter_fourcc(*'DIVX'),
#                           fps=20.0, frameSize=(resize_w, resize_h))



# frame_buffer = deque(maxlen=10)
# while cap.isOpened():
#     ret, color_frame = cap.read()
#     if ret:
#         color_frame = cv2.cvtColor(color_frame, cv2.COLOR_BGR2RGB)
#         color_frame = cv2.resize(color_frame, (resize_w, resize_h))
#         frame_buffer.append(color_frame)
#         blend_frame = color_frame_pipeline(frames=frame_buffer, solid_lines=True, temporal_smoothing=True)
#         out.write(cv2.cvtColor(blend_frame, cv2.COLOR_RGB2BGR))
#         cv2.imshow('Lane Detection', cv2.cvtColor(blend_frame, cv2.COLOR_RGB2BGR)), cv2.waitKey(1)
#     else:
#         break
# cap.release()
# out.release()
# cv2.destroyAllWindows()



# *********************************************************************************************









    # test_videos_dir = join('data', 'test_videos')
    # test_videos = [join(test_videos_dir, name) for name in os.listdir(test_videos_dir)]
    # camera_directory = "~/../../usr/local/zed/tools/ZED\\ Explorer"
    # cap = cv2.VideoCapture(0)
    # print('Processing video: {}'.format(cap))
        
    # # out = cv2.VideoWriter(join('out', 'videos', basename(cap)),
    # #                           fourcc=cv2.VideoWriter_fourcc(*'DIVX'),
    # #                           fps=20.0, frameSize=(resize_w, resize_h))




    # frame_buffer = deque(maxlen=10)
    # while cap.isOpened():
    #     ret, color_frame = cap.read()
    #     if ret:
    #         color_frame = cv2.cvtColor(color_frame, cv2.COLOR_BGR2RGB)
    #         color_frame = cv2.resize(color_frame, (resize_w, resize_h))
    #         frame_buffer.append(color_frame)
    #         blend_frame = color_frame_pipeline(frames=frame_buffer, solid_lines=True, temporal_smoothing=True)
    #         out.write(cv2.cvtColor(blend_frame, cv2.COLOR_RGB2BGR))
    #         cv2.imshow('Lane Detection', cv2.cvtColor(blend_frame, cv2.COLOR_RGB2BGR)), cv2.waitKey(1)
    #     else:
    #         break
    # cap.release()
    # out.release()
    # cv2.destroyAllWindows()



    # for test_video in test_videos:
    # 	# camera = cv2.VideoCapture(1)
        
    #     print('Processing video: {}'.format(test_video))
    #     # cap = cv2.VideoCapture(test_video)
    #     out = cv2.VideoWriter(join('out', 'videos', basename(test_video)),
    #                           fourcc=cv2.VideoWriter_fourcc(*'DIVX'),
    #                           fps=20.0, frameSize=(resize_w, resize_h))

    #     frame_buffer = deque(maxlen=10)
    #     while cap.isOpened():
    #         ret, color_frame = cap.read()
    #         if ret:
    #             color_frame = cv2.cvtColor(color_frame, cv2.COLOR_BGR2RGB)
    #             color_frame = cv2.resize(color_frame, (resize_w, resize_h))
    #             frame_buffer.append(color_frame)
    #             blend_frame = color_frame_pipeline(frames=frame_buffer, solid_lines=True, temporal_smoothing=True)
    #             out.write(cv2.cvtColor(blend_frame, cv2.COLOR_RGB2BGR))
    #             cv2.imshow('Lane Detection', cv2.cvtColor(blend_frame, cv2.COLOR_RGB2BGR)), cv2.waitKey(1)
    #         else:
    #             break
    #     cap.release()
    #     out.release()
    #     cv2.destroyAllWindows()