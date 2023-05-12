import os

import cv2

recoreding_output_directionary = os.path.join(os.curdir,"records/")
os.makedirs(recoreding_output_directionary, exist_ok=True)

# Set up the screen capture
monitor = {"top": 0, "left": 0, "width": 800, "height": 600}  # Adjust the dimensions based on your screen resolution
batch_count = 100
fps = -1
sliding_fps_average_size = 10

# DISPLAY
display = True
display_font = cv2.FONT_HERSHEY_SIMPLEX
display_fps_position = (10,30)
display_key_position = (10,60)

if fps <= 0:
    fps = 1000
