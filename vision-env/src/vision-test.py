import io
import os
import sys

# Imports the Google Cloud client library
from google.cloud import vision

# User input from the command line
image_path = sys.argv[1]

# The name of the image file to annotate
file_name = os.path.abspath(image_path)

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

# Instantiates a client
client = vision.ImageAnnotatorClient()

image = vision.Image(content=content)

# Performs label detection on the image file
response = client.label_detection(image=image)
labels = response.label_annotations

print('Labels:')
for label in labels:
    print(label.description)
