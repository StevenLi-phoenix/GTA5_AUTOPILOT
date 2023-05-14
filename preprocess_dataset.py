import os.path

import numpy as np
import cv2
import c


def load_data(name="dataset_0.npz"):
    data = np.load(os.path.join(c.recoreding_output_directionary, name), allow_pickle=True)
    frames = data["frames"]
    keys = data["keys"]
    print(keys)
    if c.display:
        for index, frame in enumerate(frames):
            key = keys[index]
            cv2.putText(frame, f"KEY: {key}", c.display_key_position, c.display_font, 1, (0, 0, 255), 2)
            cv2.imshow("Playback", frame)
            cv2.waitKey(int(1000/c.fps))
            print(f"Index {index}: Keys held down: {key}")
    return frames, keys


for i in range(6):
    _, _ = load_data(f"dataset_{i}.npz")
cv2.destroyAllWindows()