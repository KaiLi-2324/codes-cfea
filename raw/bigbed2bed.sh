#!/usr/bin/env bash
bb_dir=$1
cd ${bb_dir}
for file in $(find . -name "*.bb")
do
    prefix=$(basename ${file} | sed s'/.bb//g')
    output="${prefix}.bed"
    bigBedToBed ${file} ${output}
done
