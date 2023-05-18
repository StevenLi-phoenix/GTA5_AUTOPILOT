import os.path

import numpy as np
import cv2
import c


def load_data(name="0.npz"):
    data = np.load(os.path.join(c.recoreding_output_directionary, name), allow_pickle=True)
    frames = data["frames"]
    keys = data["keys"]
    # print(keys)
    if c.display:
        for index, frame in enumerate(frames):
            key = keys[index]
            cv2.putText(frame, f"KEY: {key}", c.display_key_position, c.display_font, 1, (0, 0, 255), 2)
            cv2.imshow("Playback", frame)
            cv2.waitKey(int(1000 / c.fps))
            c.log.debug(f"Index {index}: Keys held down: {key}")
    return frames, keys


quit_flag = False
paths = os.listdir("records")
max_index = max([int(file.split(".")[0]) for file in paths])
status = []
for i in range(max_index + 1):
    frames, keys = load_data(f"{i}.npz")
    status.extend([False for _ in frames])
    for index in range(len(frames)):
        frame = frames[index]
        key = keys[index]
        cv2.putText(frame, f"KEY: {key}", c.display_key_position, c.display_font, 1, (0, 0, 255), 2)
        cv2.imshow("Show", frame)
        key_press = cv2.waitKey(-1) & 0xFF
        if key_press == ord('q'):
            quit_flag = True
            break
        elif key_press == ord("a"):
            c.log.info(f"Accept {c.recoreding_output_directionary}{i}.npz - frame {index}")
            status[index + i * c.batch_count] = True
        elif key_press == ord("d"):
            c.log.info(f"Denied {c.recoreding_output_directionary}{i}.npz - frame {index}")
        elif key_press == ord("s"):
            c.log.info(f"Skip current batch {c.recoreding_output_directionary}{i}.npz - frame {index}")
            break
    if quit_flag:
        break

cv2.destroyAllWindows()
