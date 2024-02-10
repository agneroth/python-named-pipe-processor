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


# TODO: a bit hacky, wait a bit for the first stream to be available
sleep(0.3)

ARGS = args.parse_args()

# Check for duplicate input/outputs

inputs = [arguments.input for arguments in ARGS.streams_averager_arguments]
outputs = [arguments.output for arguments in ARGS.streams_averager_arguments]

if len(inputs) != len(set(inputs)):
    raise Exception("Duplicate input arguments.")
if len(outputs) != len(set(outputs)):
    raise Exception("Duplicate outputs arguments.")

threads = []
stop_event = Event()

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
        logging.info("Recieved keyboard interrupt, quitting...")
        stop_event.set()
        break
    except Exception as e:
        logging.error(e)
        stop_event.set()
        raise e

# Wait for it to finish...
for thread in threads:
    thread.join()
