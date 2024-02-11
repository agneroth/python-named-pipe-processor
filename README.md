# Named Pipe CLI Processor

This module takes as inputs named pipes (or stdin) which contains bytestreams of little-endian doubles and outputs to a binary files (or stdout) the resulting **moving average** of respective window. It supports any number of inputs and outputs.

It is currently implemented using the multithreading library to better support stdin/stdout, but can be upgraded in the future to multiprocessing for paralellizing faster bytestreams.

## Requirements:

This code was developed using python ^3.11 syntax. It's expected to be ran with a compatible version.

## Usage:

```sh
python processing/run.py [-h] window,input_stream,output_stream [window,input_stream,output_stream ...]
```

**Positional arguments**:

`window,input_stream,output_stream`

- **window**: Size of the average window.
- **input_stream**: The path of the input named pipe for the data stream (or '-' for stdin).
- **output_stream**: The path of the output binary file for the data stream (or '-' for stdout).

**Options**:

- `-h, --help`: Show the help message and exit

You can look at an always up to date documentation by running:

```sh

python processing/run.py --help

```

### TODOS:

- Add input bytestream format as an option.
- Change API to use the `python -m processing` syntax.
- Better specify the usecase requirements for determining if multithreading or multiprocessing are a better option.
- Add support to other algorithms than moving average.
- Add outil to decode an input/output binary stream into text for visual testing.
- Add a way to close files in case of an exception
- Reduce number of local variables in the `process_stream` function.
- Better specify the usecase to possibly remove the bytestream buffering before the unpacking to improve performance
- Add aditional tests