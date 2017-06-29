#!/bin/bash

for f in ../test_data/out_*.txt
do
  # echo $f
  filename=$(basename "$f")
  outfile=test/${filename/out/out_orig}
  if [ -f $outfile ]; then

    echo diff -w "$f" "$outfile"
    diff -w "$f" "$outfile"
  fi
done
