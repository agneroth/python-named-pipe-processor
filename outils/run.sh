#!/bin/bash

# ============================================================
# Automatically run the setup....
# ============================================================


./datastream.sh data/sample-data-in,input1, data/sample-data-in,input2 & pid1="$!" ; \
poetry run python processing/run.py 2,input1,output1 2,input2,output2 ;
kill $pid1
