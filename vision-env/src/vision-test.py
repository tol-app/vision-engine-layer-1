import io
import os
import sys
import cv2
import math
import colors_detection

from google.cloud import vision

# Minimum score required for labels detection
MIN_SCORE_REQUIRED = 0.80

# Minimum pixel_fraction required for color detection.
# Actually unused but useful for filtering colors.
MIN_PFRACTION_REQUIRED = 0.02

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

key_rel_path= os.path.join('..', 'keys', 'developerKey.json')
key = os.path.abspath(key_rel_path)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = key

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
label_response = client.label_detection(image=image)
labels = label_response.label_annotations

# Performs image_properties detection on the image file
colors_response = client.image_properties(image=image)
colors = colors_response.image_properties_annotation.dominant_colors.colors

# Labels sorted by attribute score
sorted_labels = sorted(labels, key=lambda x:x.score, reverse=True)
# Labels filtered by attribute score
filtered_labels = filter(lambda x:x.score > MIN_SCORE_REQUIRED, sorted_labels)

# Labels sorted by attribute score
sorted_colors = sorted(colors, key=lambda x:x.pixel_fraction, reverse=True)
# Colors filtered by attribute pixel_fraction
#filtered_colors = filter(lambda x:x.pixel_fraction > MIN_PFRACTION_REQUIRED, sorted_colors)
# Actually no filtering policy
filtered_colors = sorted_colors

print('\nLabels:')
for label in filtered_labels:
    print('--- Label: ' + label.description + ' ---> ' + str(math.trunc(label.score*100)) + '%' +
            '\n')

print('\nColors:')
for color_info in filtered_colors:
    color = color_info.color

    red = math.trunc(color.red)
    green = math.trunc(color.green)
    blue = math.trunc(color.blue)

    rgb_triplet = (red, green, blue)
    rgb_triplet_str = (str(red) + '%, ', str(green) + '%, ', str(blue) + '%')
    color_name = colors_detection.convert_rgb_to_names(rgb_triplet)

    # uncomment for verbose output
    #print(str(color_info.pixel_fraction) + ' == ' + str(math.trunc(color_info.pixel_fraction*100)) + '%' + '   score: ' + str(color_info.score) + '---> ' + color_name)
    print('--- Pixel Fraction: ' + str(round(color_info.pixel_fraction*100, 3)) + '%' + 
            '\tScore: ' + str(round(color_info.score, 5)) + 
            '\tColor Name: ' + color_name + 
            '\n')
