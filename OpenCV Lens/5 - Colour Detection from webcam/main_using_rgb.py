import cv2
import pandas as pd

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Reading csv file with pandas and giving names to each column
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('Colour_Contents.csv', names=index, header=None)

# Function to return colour name based upon R,G,B values
def get_color_name(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname

# Main program
while True:
    ret, frame = cap.read()
    height, width, _ = frame.shape

    cx = int(width / 2)
    cy = int(height / 2)

    # Pick pixel value
    pixel_center_bgr = frame[cy, cx]

    # Pick BGR value
    b, g, r = int(pixel_center_bgr[0]), int(pixel_center_bgr[1]), int(pixel_center_bgr[2])

    # Get colour name
    text = get_color_name(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

    # Display colour
    # Note: Coordinates (x,y)= (0,0) at top left corner of the frame. As x increases, it moves right of frame and as y increases, it moves down the frame !!!

    # Syntax: cv2.rectangle(image, start_point (top left), end_point (bottom right), color, thickness)
    cv2.rectangle(frame, (cx - 400, cy-350), (cx + 400, cy-300), (255, 255, 255), -1)
    # For very light colours we will keep the rectangle background in black colour
    if r + g + b >= 600:
        cv2.rectangle(frame, (cx - 400, cy - 350), (cx + 400, cy - 300), (0, 0, 0), -1)

    # Syntax: cv2.putText(image, text, org (coordinates of the bottom-left corner), font, fontScale, color, thickness)
    cv2.putText(frame, text, (cx - 390, cy-320), 2, 1, (b, g, r), 3, cv2.LINE_AA)      # Here, 0 at 4th position from left represents the particular text format !!!

    # To put circle of green colour on the centre of the frame so as to tell user to focus the object on this circle.
    cv2.circle(frame, (cx, cy), 5, (0, 255, 0), 4)

    # Displaying frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()