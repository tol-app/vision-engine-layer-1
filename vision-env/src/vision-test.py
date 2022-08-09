from genericpath import isfile
import io
import os
import sys
import numpy as np
import cv2
import json
from pyautogui import size
from google.cloud import vision

# Minimum score required for labels detection
MIN_SCORE_REQUIRED = 0.80

def shape_selection(event, x, y, flags, param):
    # grab references to the global variables
    global ref_point, crop

    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being performed
    if event == cv2.EVENT_LBUTTONDOWN:
        ref_point = [(x, y)]

    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        ref_point.append((x, y))

        # draw a rectangle around the region of interest
        cv2.rectangle(image, ref_point[0], ref_point[1], (0, 255, 0), 2)
        cv2.imshow("image", image)

# If a key is present in /keys and has a correct name, add it to enviroment variable
key_folder = os.path.join("..", "keys")
key_names = ["devKey.json",
              "devkey.json",
              "developerkey.json",
              "developerKey.json"]

for i in key_names:
    success = False
    key_rel_path = os.path.join(key_folder, i)
    key_abs_path = os.path.abspath(key_rel_path)

    if os.path.exists(key_abs_path):
        success = True
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = key_abs_path
        break

if not success:
    print("API keys not found. Closing executable.")
    sys.exit(0)

# User input from the command line
image_name = sys.argv[1]

# The name of the image file to annotate
file_name = os.path.abspath(image_name)

# File path check
if not(os.path.exists(file_name)):
    while True:
        print("Wrong file or file path\n")

        # Press q to exit or enter correct path
        userin = input("Enter the correct path or press q to quit: ")
        if userin == "q" or "Q":
            sys.exit(0)
        else:
            file_name = userin
            break

# Initialize the list of reference point
ref_point = []
crop = False

image = cv2.imread(file_name, 1)

#Fetch screen and image res data
scr_width, scr_height  = size()
img_width, img_height  = image.shape[0], image.shape[1]
img_ratio              = img_height / img_width
resize_factor          = 0.8   # 1 is fullscreen

# Check if image is larger than monitor
if img_width / scr_width > 1 or img_height / scr_height > 1:

    #scale image to a more reasonable size
    scaled_width = int((2 - (img_width / scr_width)) * img_width * resize_factor)
    scaled_height = int(scaled_width / img_ratio)

    image = cv2.resize(image, (scaled_width, scaled_height), interpolation=cv2.INTER_CUBIC)
    cv2.imwrite('~/vision-env/images/testset/test0/copy_res.jpg', image)

#FIXME: fix absolute/relative path problem on Linux on cloning image
clone = image.copy()

cv2.namedWindow("image")
cv2.setMouseCallback("image", shape_selection)

# keep looping until the 'q' key is pressed
while True:
    # display the image and wait for a keypress
    cv2.imshow("image", image)
    key = cv2.waitKey(1) & 0xFF

    # press 'r' to reset the window
    if key == ord("r"):
        image = clone.copy()

    # press 'q' to quit
    if key == ord("q"):
        sys.exit(0)

    # if the 'c' key is pressed, break from the loop
    elif key == ord("c"):
        break

if len(ref_point) == 2:
    crop_img = clone[ref_point[0][1]:ref_point[1][1], ref_point[0][0]:ref_point[1][0]]
    #cv2.imshow("crop_img", crop_img)   #uncomment --> show cropped image
    cv2.waitKey(0)  #maybe useless
    cv2.imwrite(os.path.join("..", "images/testset/test0/copy1.jpg"), crop_img)

# close all open windows
cv2.destroyAllWindows()

# File used for label detection
target_file = os.path.abspath(os.path.join("..", "images/testset/test0/copy1.jpg"))
# Loads the image into memory
with io.open(target_file, 'rb') as image_file:
    content = image_file.read()

# Instantiates a client
client = vision.ImageAnnotatorClient()

#image = vision.Image(content=content)
image = vision.Image(content=content)

# Performs label detection on the image file
response = client.label_detection(image=image)
labels = response.label_annotations

# Labels sorted by attribute score
sorted_labels = sorted(labels, key=lambda x:x.score, reverse=True)

# Labels filtered by attribute score
filtered_labels = filter(lambda x:x.score > MIN_SCORE_REQUIRED, sorted_labels)

print('Labels:')
for label in filtered_labels:
    print(label.description + ' ---> ' + str(label.score))
