import logging
import os
import time

from pynput import keyboard
import numpy as np
import cv2
import mss
import multiprocessing
import c


def write_to_disk(frames, keys, batch_count):
    # Save the screen captures and corresponding key inputs as a single file
    combined_data = {'frames': frames, 'keys': keys}
    np.savez_compressed(os.path.join(c.recoreding_output_directionary, f'dataset_{batch_count}.npz'), **combined_data)
    c.log.debug(f"Savez_compressed:{batch_count}")

def main():
    quit_flag = False

    # Create an mss instance
    sct = mss.mss()

    index = 0

    frames = []
    key = set()
    keys = []
    write_manager = []

    # Variables for tracking FPS
    frame_times = []
    sliding_fps = []

    pool = multiprocessing.Pool(processes=4)

    def on_key_press(event):
        nonlocal key
        try:
            key.add(event.char)
            if event.char == 'q':
                nonlocal quit_flag
                quit_flag = True
                key = set()
                listener.stop()
        except AttributeError:
            key.add(str(event))

    def on_key_release(event):
        try:
            key.discard(event.char)
        except AttributeError:
            key.discard(str(event))

    with keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as listener:
        while not quit_flag:
            index += 1
            start_time = time.time()
            c.log.info(f"[{index}]{key}")
            frame = np.array(sct.grab(c.monitor))
            frames.append(frame)
            keys.append(key.copy())

            # FPS limiter and smooth fps indicator
            # ---
            elapsed_time = time.time() - start_time
            if elapsed_time < 1 / c.fps:
                time.sleep(1 / c.fps - elapsed_time)
            # ---
            elapsed_time = time.time() - start_time
            current_fps = 1 / elapsed_time
            frame_times.append(current_fps)
            frame_times = frame_times[-c.sliding_fps_average_size:]
            sliding_fps_average = sum(frame_times) / len(frame_times)
            sliding_fps.append(sliding_fps_average)
            sliding_fps = sliding_fps[-c.sliding_fps_average_size:]

            if c.display: # enable only when config to save time
                frame_C = frame.copy()
                frame_C = cv2.resize(frame_C, (320,180))
                cv2.putText(frame_C, f"FPS: {round(sliding_fps_average, 2)}", c.display_fps_position, c.display_font, 1, c.display_fps_color, 3)
                cv2.putText(frame_C, f"KEY: {key}", c.display_key_position, c.display_font, 1, c.display_key_color, 3)
                cv2.imshow("Screen Capture", frame_C)
                cv2.waitKey(1)

            if index % c.batch_count == 0:
                # Write to disk in a separate process
                write_process = pool.apply_async(write_to_disk, args=(frames, keys, index // c.batch_count - 1))
                write_manager.append((index // c.batch_count - 1, write_process))
                frames = []
                keys = []

            if quit_flag:
                if index % c.batch_count == 0:
                    break
                # Write to disk part before exit
                write_process = pool.apply_async(write_to_disk, args=(frames, keys, index // c.batch_count))
                write_manager.append((index // c.batch_count, write_process))
                break



    # Close the windows
    cv2.destroyAllWindows()

    c.log.info("Record process end, current status of writing process")
    c.log.info("Waiting for the following write manager to finish")
    pool.close()
    wait_time = 0
    # Monitor the status of workers
    while any(not result[1].ready() for result in write_manager):
        wait_time += 1
        time.sleep(1)
        c.log.info(f"====[total:{len(write_manager)}, wait:{wait_time}s]====")
        for result in write_manager:
            c.log.info(f"\rWork {result[0]} {result[1].ready()}")
    pool.join()


if __name__ == '__main__':
    main()
