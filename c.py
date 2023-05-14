import logging
import os

import cv2

logname = "record.log"
loglevel = logging.DEBUG

recoreding_output_directionary = os.path.join(os.curdir,"records/")
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
display_key_position = (10,60)

log = logging.getLogger("")
fileHandler = logging.FileHandler(filename=logname)
fileHandler.setLevel(loglevel)
log.addHandler(fileHandler)
streamHandler = logging.StreamHandler()
streamHandler.setLevel(loglevel)
log.addHandler(streamHandler)

if fps <= 0:
    fps = 1000

