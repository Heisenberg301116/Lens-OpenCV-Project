import cv2
import pandas as pd

img = cv2.imread('Houses.jpg')      # to load image

# declaring global variables (are used later on)
clicked = False
r = g = b = x_pos = y_pos = 0

# Reading csv file with pandas and giving names to each column
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('Colour_Contents.csv', names=index, header=None)

# function to calculate minimum distance from all colors and get the most matching color
def get_color_name(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname

# function to get x,y coordinates of mouse double click
def draw_function(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # If you do left click at any point on the image then b,g,r will store the respective values
        global b, g, r, x_pos, y_pos, clicked
        clicked = True
        x_pos = x
        y_pos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)

# Syntax: cv2.imshow(window_name, image
cv2.namedWindow('image')    # cv2.imshow() method is used to display an image in a window. The window automatically fits to the image size.
cv2.setMouseCallback('image', draw_function)    # whenever a mouse callback is made (i.e, we click the mouse) on the 'image', setMouseCallback() will come into action and it will call draw_function().

while True:

    cv2.imshow("image", img)    # to display the image
    if clicked:
        # Note: Coordinates (x,y)= (0,0) at top left corner of the frame. As x increases, it moves right of frame and as y increases, it moves down the frame !!!

        # cv2.rectangle(image, start point, endpoint, color, thickness) -1 fills entire rectangle with (b,g,r) colour else if we specify positive value then only border of rectangle will have (b,g,r) colour and inner rectangle part will be transparent.
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)      # the rectangle will be of the same colour as we have clicked

        # Creating text string to display( Color name and RGB values )
        text = get_color_name(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

        # cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        # For very light colours we will display text in black colour
        if r + g + b >= 600:
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

        clicked = False     # clicked will become true whenever a mouse callback is made (so that draw_function() may be called out).

    # Break the loop when user hits 'esc' key
    key= cv2.waitKey(1)
    if key==27:
        break

cv2.destroyAllWindows()