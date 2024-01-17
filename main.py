import time
from pynput.keyboard import Key, Controller, Listener
from threading import Thread, Event

keyboard = Controller()

# Key sequence and timings
keys_to_press = "567890-"  #String to press
press_interval = 0.05      #Time between chars
sequence_interval = 0.5    #Time between attempts

# Event to stop the thread
stop_event = Event()

# Thread reference
thread = None

def press_keys():
    print("Sequence started.")
    while not stop_event.is_set():
        for key in keys_to_press:
            if stop_event.is_set():
                break  # Break the inner loop if stop_event is set
            keyboard.press(key)
            keyboard.release(key)
            time.sleep(press_interval)
        time.sleep(sequence_interval)
    print("Sequence stopped.")

def on_press(key):
    global thread
    if key == Key.caps_lock:  # Assuming F5 is the toggle key
        if thread is None or not thread.is_alive():
            # Start the thread
            stop_event.clear()
            thread = Thread(target=press_keys)
            thread.start()
            print("Thread started.")
        else:
            # Stop the thread
            stop_event.set()
            thread.join()  # Wait for the thread to finish
            thread = None
            print("Thread stopped.")

# Listener to detect key presses
with Listener(on_press=on_press) as listener:
    listener.join()
