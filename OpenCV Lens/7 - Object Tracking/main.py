import cv2
from tracker import *   # * means import everything

# Create tracker object
tracker = EuclideanDistTracker()    # initializing the module in tracker.py file

cap = cv2.VideoCapture("highway.mp4")

# Object detection from Stable camera
object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=100)  # this will extract moving objects from the stable footage
# higher the varThreshold lower will be the detection but also lower false positive.
# lower the varThreshold higher will be the detection but also higher false positive.
while True:
    ret, frame = cap.read()
    height, width, _ = frame.shape

    # Extract Region of interest. Vehicles will be tracked only inside the region of interest.
    roi = frame[340: 720,500: 800]  # We will find region of interest. height range: [340, 720] px, width range: [500, 800] px.

    # 1. Object Detection
    mask = object_detector.apply(roi)   # the goal of mask is that it makes everything that we don't need as black and everything that we need as white.
    _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)  # to filter out white shadows formed due to mask(), we use this such that everything with b,g,r <254 is made black and those objects with all 3 of b,g,r >=254 gets their (b,g,r) transformed to (255,255,255), i.e, complete white.
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)    # The contours are a useful tool for shape analysis and object detection and recognition.
    detections = []
    for cnt in contours:
        # Calculate area and remove small elements
        area = cv2.contourArea(cnt)
        if area > 100:  # 100 pixels
            # cv2.drawContours(roi, [cnt], -1, (147, 20, 255), 2)   # drawing pink contours inside region of interest at objects objects having area > 100 px. -1 means we want to draw all the contours on the frame at once.
            x, y, w, h = cv2.boundingRect(cnt)
            detections.append([x, y, w, h]) # detections will enclose the bounding boxes for all the detected objects at a particular time.

    # 2. Object Tracking
    boxes_ids = tracker.update(detections)  # update() will assign id to each bounding box in detections. It also makes sure that id for the object is same in the current frame as it was in the previous frame and id for the new object must be unique.
    for box_id in boxes_ids:
        x, y, w, h, id = box_id
        # To display text on the object on the frame
        cv2.putText(roi, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 3)

        # To display text on the object on the mask
        cv2.putText(mask, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv2.rectangle(mask, (x, y), (x + w, y + h), (0, 255, 0), 3)

    cv2.imshow("roi", roi)
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)

    key = cv2.waitKey(30)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()