from collections import deque
from struct import unpack, pack
from threading import Event
import select
from time import sleep

from processing.parser import StreamAveragerArgs

def process_streams(
    arguments: StreamAveragerArgs,
    exit_event: Event,
    data_format: str = "<d",
    packet_size: int = 8,
    number_of_retries: int = 3
) -> None:
    """
    This function calculates the moving average of an input stream and outputs the result to another stream.
    It takes an instance of StreamAveragerArgs, which contains an window size, an input stream and an output stream. 
    It expecting a bytestream of format `data_format` (by default little-endian double), 
    and bytesize of lenght `packet_size` (by default 8). 

    :param StreamAveragerArgs arguments: 
    :param Event exit_event: Event to control when to quit program.
    :param str data_format: Bytestream format (by default little-endian double)
    :param int packet_size: Bytestream format lenght (by default 8). 
    :param int number_of_retries: Number of retries to open input bytestream.
    """

    # Convert the text encoded inputs into python objects.
    window_size = arguments.parse_window()

    # TODO: A bit hacky... try to open `number_of_retries` times, sleeping 0.1 s between each retry
    retries = 0
    while not exit_event.is_set():
        try:
            input_handle = arguments.parse_input()
        except FileNotFoundError:
            if retries >= number_of_retries:
                raise
            retries += 1
            sleep(0.1)
        else:
            break
    # Return if stop event is set
    if exit_event.is_set():
        return

    output_handle = arguments.parse_output()

    # Double-ended queue for calculating moving average
    queue = deque(maxlen=window_size)
    # Average variable
    average = 0
    # Initialize buffer
    buffer = bytearray()
    remaining_buffer_size = packet_size

    # Pooler to check if the named pipe is closed.
    poller = select.poll()
    poller.register(input_handle, select.POLLHUP)
    pipe_closed = False

    # Use thread-safe event from main thread to quit with Ctrl+C
    while not exit_event.is_set():

        # If pipe is not closed, check if it is closed
        if not pipe_closed:
            for descriptor, mask in poller.poll(0):
                # Can contain at most one element, but use for loop for upacking...
                if descriptor == input_handle.fileno() and mask & select.POLLHUP:
                    pipe_closed = True

        # Read up to remaining buffer memory
        next_bytes = input_handle.read(remaining_buffer_size)

        # If the pipe is closed and there are no remaining bytes, exit
        if pipe_closed and len(next_bytes) == 0:
            return

        buffer.extend(next_bytes)
        # Update remaining buffer memory
        remaining_buffer_size -= len(next_bytes)
        # If buffer is full
        if remaining_buffer_size == 0:
            # Decode buffer
            next_digit = unpack(data_format, buffer)[0]
            # Store weighted element (into the left of the queue)
            next_digit_weighted = next_digit / window_size
            queue.appendleft(next_digit_weighted)
            # print(f"digit: {next_digit}")
            # Update average
            average += next_digit_weighted
            # Reinitialize buffer
            remaining_buffer_size = packet_size
            buffer = bytearray()
        # If currently stored data is the lenght as the window size
        if len(queue) == window_size:
            # Write current average
            output_handle.write(pack("<d", average))
            # Remove digit currently out of the window
            leaving_weighted_digit = queue.pop()
            # print(f"average: {average}")
            # Update the average, removing the leaving digit weighted contribution
            average -= leaving_weighted_digit
