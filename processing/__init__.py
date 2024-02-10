import argparse
import logging

from processing.parser import StreamAveragerArgs

args = argparse.ArgumentParser(
    prog="Moving averager for datastreams using named pipes as inputs."
)

args.add_argument(
    dest="streams_averager_arguments",
    metavar="window,input_stream,output_stream",
    type=StreamAveragerArgs,
    nargs="+",
    help="""
    window: Size of the average window. 
    input_stream: The name of the input named pipe for the data stream (or '-' for stdin).
    output_stream: The name of the output binary file for the first data stream (or '-' for stdout).
    """
)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logger.addHandler(ch)
