import cv2
from gui_buttons import Buttons

# Initialize Buttons
button = Buttons()  # initializing the object of the class Buttons()
button.add_button("person", 20, 20)     # (20,20) means the top left point of the rectangular button
button.add_button("cell phone", 20, 100)
button.add_button("keyboard", 20, 180)
button.add_button("remote", 20, 260)
button.add_button("scissors", 20, 340)
button.add_button("bottle", 20, 420)

colors = button.colors      # a list containing 91 tuples with random values of colours in bgr format.
# colors will store bgr color values for the rectangle (to point out the detected object on frame) of each object

# Opencv DNN
# to load/initialize the Deep Learning network to the system
net = cv2.dnn.readNet("dnn_model/yolov4-tiny.weights", "dnn_model/yolov4-tiny.cfg") # We need to specify 2 files: .weights and .cfg
model = cv2.dnn_DetectionModel(net)     # Defining the model
model.setInputParams(size=(320, 320), scale=1/255)      # size is the size of the square. Bigger the size better the precision but also slower speed.
                                                        # In opencv, value of pixels goes from 0 to 255 while on DNN it goes from 0 to 1. So we have to scale it by 1/255.
# Load class lists
classes = []
with open("dnn_model/classes.txt", "r") as file_object:
    for class_name in file_object.readlines():
        class_name = class_name.strip()
        classes.append(class_name)
# classes[0]= "person", classes[1]="bicycle" etc.
print("Objects list:")
print(classes)


# Initialize camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
# FULL HD 1920 x 1080


def click_button(event, x, y, flags, params):   # (x,y) is the position where we have clicked the button
    if event == cv2.EVENT_LBUTTONDOWN:  # if it is left click
        button.button_click(x, y)   # button_click is a function in gui_buttons.py file. It check whether the left click was inside any of the button or outside.
        # If inside any button, it will change the status o that nutton, i.e, if previously that button was ON, it will OFF that button and vice-versa.

# Create window
cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", click_button) # Everytime we do a click on frame, setMouseCallback() will call click_button function

while True:
    # Get frames
    ret, frame = cap.read()

    # Get active buttons list
    active_buttons = button.active_buttons_list()   # it will return the list of buttons that are ON.
    #print("Active buttons", active_buttons)

    # Object Detection
    (class_ids, scores, bboxes) = model.detect(frame, confThreshold=0.3, nmsThreshold=.4)   # detect from frame all the objects visible currently
    # class_ids= 0 => it is a person etc.
    # score: How confident the model is that the object detected is a person, car, etc. If it is 100% confident then score=1. If it is 20% confident then score is 0.2.
    # bboxes= bounding boxes which contains the position (top left point, the width and height of the rectangle) of the object being detected
    # confThreshold: Confidence threshold. If here the value of score is less than 0.3, then the model won't recognize that object.
    # nms: non maximum supression

    for class_id, score, bbox in zip(class_ids, scores, bboxes):    # zip() is a function used to extract values from multiple arrays
        (x, y, w, h) = bbox
        class_name = classes[class_id]
        color = colors[class_id]       # this particular object with id as: class_id will be pointed using rectangle of this colour: color if button for that object is active

        if class_name in active_buttons:
            cv2.putText(frame, class_name, (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 3, color, 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 3)


    # To display buttons on the frame
    button.display_buttons(frame)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()