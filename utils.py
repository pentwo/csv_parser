import threading
import itertools
import time


def spinner():
    # Spinner animation characters
    spinner_icons = itertools.cycle(['-', '\\', '|', '/'])
    while True:
        print(next(spinner_icons), end='\r', flush=True)
        time.sleep(0.1)  # Control the speed of the spinner

# To stop the spinner, you'll need to kill the thread
# after your processing is complete
