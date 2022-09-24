import cv2
import numpy as np

class Buttons:
    def __init__(self): # constructor
        # Font
        self.font = cv2.FONT_HERSHEY_PLAIN
        self.text_scale = 3
        self.text_thick = 3
        self.x_margin = 20
        self.y_margin = 10

        # Buttons
        self.buttons = {}   # It is an array of dictionary. Each index corresponds to button_index which will store the following dictionary: {"text": <name of the button>, "position": <top left and bottom right position>, "active": <True/False>}
        self.button_index = 0   # It represents total number of buttons we have specified. 0 represents no buttons, 1 represents 1 button
        self.buttons_area = []

        np.random.seed(0)
        self.colors = []    # colors will store bgr color values for the rectangle (to point out the detected object on frame) of each object
        self.generate_random_colors()

    def generate_random_colors(self):
        for i in range(91):
            random_c = np.random.randint(256, size=3)   # this will generate an array of length 3 with each index containing value from [0,255)
            self.colors.append((int(random_c[0]), int(random_c[1]), int(random_c[2])))

    def add_button(self, text, x, y):   # This will add button to self.buttons dictionary
        # (x,y) means the top left point of the rectangular button
        # Get text size
        # getTextSize() calculates and returns the size of a box (length, width) that contains the specified text.
        textsize = cv2.getTextSize(text, self.font, self.text_scale, self.text_thick)[0]
        right_x = x + (self.x_margin * 2) + textsize[0]
        # right_x will give the value of right x of the rectangular button with the given value of x (x is left x)
        # (self.x_margin * 2) because both sides of the rectangle we have to give give some margin so that the text doesn't start or end from just the boundary of the rectangle
        bottom_y = y + (self.y_margin * 2) + textsize[1]

        self.buttons[self.button_index] = {"text": text, "position": [x, y, right_x, bottom_y], "active": False}
        self.button_index += 1

    def display_buttons(self, frame):   # this will display all those buttons (that have been added into the dictionary) on the frame
        for b_index, button_value in self.buttons.items():  # dict.items() returns both the keys and values. b_index= key, button_value= {text: , font: , text_scale: , thickness: }
            # button_value is a dictionary
            button_text = button_value["text"]
            (x, y, right_x, bottom_y) = button_value["position"]    # top left and bottom right coordinates
            active = button_value["active"]     # True/False

            if active:
                button_color = (0, 255, 0)  # green
                text_color = (255, 0, 0)    # blue
                thickness = -1  # means the whole rectangle will have the color as button_color
            else:
                button_color = (0, 0, 255)  # red
                text_color = (255, 0, 0)    # blue
                thickness = 4   # means only border of thickness 3 will have color as button_color

            # Get  text size
            cv2.rectangle(frame, (x, y), (right_x, bottom_y),
                          button_color, thickness)
            cv2.putText(frame, button_text, (x + self.x_margin, bottom_y - self.y_margin),
                        self.font, self.text_scale, text_color, self.text_thick)
        return frame

    def button_click(self, mouse_x, mouse_y):
        for b_index, button_value in self.buttons.items():
            (x, y, right_x, bottom_y) = button_value["position"]
            active = button_value["active"]
            #area = [(x, y), (right_x, y), (right_x, bottom_y), (x, bottom_y)]
            #inside = cv2.pointPolygonTest(np.array(area, np.int32), (int(mouse_x), int(mouse_y)), False)    # If the position where the user left-clicked is inside the polygon then it means the click was done on that button.
            inside=0
            if mouse_x > x and mouse_x < right_x and mouse_y < bottom_y and mouse_y > y:
                inside=1
            if inside > 0:
                new_status = False if active is True else True
                self.buttons[b_index]["active"] = new_status

    def active_buttons_list(self):  # If a button is active, this function will append the text of that button (class name of object) to the active_list
        active_list = []
        for b_index, button_value in self.buttons.items():
            active = button_value["active"]
            text = button_value["text"]
            if active:
                active_list.append(str(text).lower())

        return active_list