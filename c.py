import logging
import os
import sys

import cv2

logname = "record.log"
loglevel = logging.DEBUG

recoreding_output_directionary = os.path.join(os.curdir,"records_2/")
os.makedirs(recoreding_output_directionary, exist_ok=True)

# Set up the screen capture
monitor = {"top": 0, "left": 0, "width": 1280, "height": 720}  # Adjust the dimensions based on your screen resolution
batch_count = 10
fps = 10
sliding_fps_average_size = 5

# DISPLAY
display = True
display_font = cv2.FONT_HERSHEY_SIMPLEX
display_fps_position = (10,30)
display_fps_color = (0, 0, 255)
display_key_position = (10,60)
display_key_color = (0, 0, 255)


log = logging.getLogger("")
log.setLevel(loglevel)
fileHandler = logging.FileHandler(filename=logname)
fileHandler.setLevel(loglevel)
log.addHandler(fileHandler)
streamHandler = logging.StreamHandler(stream=sys.stdout)
streamHandler.setLevel(loglevel)
log.addHandler(streamHandler)


if fps <= 0:
    fps = 1000

