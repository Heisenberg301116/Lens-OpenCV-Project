import cv2

# Load Camera
cam = cv2.VideoCapture(0)   # 0 means to load 1st camera, 1 means to load the 2nd camera and so on...

# Now we are going to get frame after frame
while True:
    ret,frame= cam.read()   # ret= true mean we have the frame else false
    cv2.imshow("Frame", frame)  # to show the frame
    key= cv2.waitKey(1) # means wait for 1ms and then go to the next frame. The argument passed must be an integer. If we pass 0 then the camera will only capture 1 frame and will reeze. So to capture multiple frames in shortest time, we will pass argument as 1.
    if key==27: # 27 corresponds to ascii value of Esc key
        break
cam.release()   # to release the camera
cv2.destroyAllWindows()