#!/bin/bash

for filepath in data/*.gr
do
    filename=$(basename "${filepath%.*}")
    python treewidth.py -f $filename
done
