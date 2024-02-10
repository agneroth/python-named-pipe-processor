import argparse
import sys
from typing import BinaryIO
from pathlib import Path
import os
import stat
import atexit

class StreamAveragerArgs:
    r"""
    Argument class for automatically parsing the input strings as their respective classes.
    :param str string: The input argument string of the format 'WINDOW,INPUT_PATH,OUTPUT_PATH'
    """

    def __init__(self, string: str):
        arguments = string.split(",")

        # Check if only three arguments are passed at a time
        if len(arguments) != 3:
            raise argparse.ArgumentError(
                argument="streams_averager_arguments",
                message="Invalid number of arguments.",
            )

        self.window = arguments[0]
        self.input = arguments[1]
        self.output = arguments[2]

    def parse_input(self) -> BinaryIO:
        """
        Parses the input string, returning a the respective file handle or buffer.

        :param str string: The name of the input named pipe for the data stream (or '-' for stdin).
        :return: stdin buffer of file handler for the input stream.
        :rtype: BinaryIO
        """
        if self.input == "-":
            return sys.stdin.buffer
        path = Path(self.input)

        if not os.path.exists(path):
            raise FileNotFoundError(f"Input stream {path} not found.")

        if not stat.S_ISFIFO(os.stat(path).st_mode):
            raise ValueError(f"Input {path} is not a stream.")

        fh = open(path, "rb")
        atexit.register(fh.close)
        self.input = fh
        return self.input

    def parse_output(self) -> BinaryIO:
        """
        Parses the output string, returning a the respective file handle or buffer.

        :param str string: The name of the output binary file for the first data stream (or '-' for stdout).
        :return: stdout buffer of file handler for the output binary file.
        :rtype: BinaryIO
        """
        if self.output == "-":
            return sys.stdout.buffer
        path = Path(self.output)

        if os.path.exists(path):
            raise FileExistsError(f"Output file {path} already exists.")
        fh = open(path, "wb")
        atexit.register(fh.close)
        self.output = fh
        return self.output

    def parse_window(self) -> int:
        """
        Parses the window string, returning the respective integer.

        :param str string: Window argument in string format.
        :return: Window lenght.
        :rtype: int
        """
        if not self.window.isdigit():
            raise ValueError(f"Window argument {self.window} is not a digit.")
        self.window = int(self.window)
        return self.window
