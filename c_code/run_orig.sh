#!/bin/bash

for f in ../test_data/in_*.txt
do
  # echo $f
  filename=$(basename "$f")
  outfile=test/${filename/in/out_orig}
  # echo $outfile
  echo ./a.exe "$f" "$outfile"
  time ./a.exe "$f" "$outfile"
done
