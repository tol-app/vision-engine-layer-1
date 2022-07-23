import io
import os
import sys
import cv2

# Imports the Google Cloud client library
from google.cloud import vision

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

# User input from the command line
image_name = sys.argv[1]

# The name of the image file to annotate
file_name = os.path.abspath(image_name)

# Initialize the list of reference point
ref_point = []
crop = False
  
image = cv2.imread(file_name)
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
  
    # if the 'c' key is pressed, break from the loop
    elif key == ord("c"):
        break
  
if len(ref_point) == 2:
    crop_img = clone[ref_point[0][1]:ref_point[1][1], ref_point[0][0]:
                                                           ref_point[1][0]]
    #cv2.imshow("crop_img", crop_img)   #uncomment --> show cropped image
    cv2.waitKey(0)  #maybe useless
    cv2.imwrite('copy1.jpg', crop_img)
  
# close all open windows
cv2.destroyAllWindows() 

# File used for label detection
target_file = os.path.abspath('copy1.jpg')

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

print('Labels:')
for label in labels:
    print(label.description)
