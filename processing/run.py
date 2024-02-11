import os
import sys

# Since we don't use the -m python tag, we need to say where our module ends...
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from time import sleep
from threading import Thread, Event
import logging

from processing.averager import process_streams
from processing import args

# Parse input arguments
ARGS = args.parse_args()

# Check for duplicate input/outputs
inputs = [arguments.input for arguments in ARGS.streams_averager_arguments]
outputs = [arguments.output for arguments in ARGS.streams_averager_arguments]

if len(inputs) != len(set(inputs)):
    raise Exception("Duplicate input arguments.")
if len(outputs) != len(set(outputs)):
    raise Exception("Duplicate outputs arguments.")


# Initialize threads list and the main thread stop event.
threads = []
stop_event = Event()

# For each triplet of arguments, create a processing thread and start it.
for stream_averager_args in ARGS.streams_averager_arguments:
    # process_streams(stream_averager_args, stop_event=stop_event)
    thread = Thread(target=process_streams, args=(stream_averager_args, stop_event))
    threads.append(thread)
    thread.start()

# Leave the threads running...
while sum(thread.is_alive() for thread in threads):
    try:
        sleep(0.1)
    except KeyboardInterrupt:
        stop_event.set()
        break
    except Exception as e:
        stop_event.set()
        raise e

# Wait for it to finish...
for thread in threads:
    thread.join()
