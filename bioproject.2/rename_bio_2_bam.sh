#!/usr/bin/env bash
bam_dir=$1
cd ${bam_dir}
for file in $(find . -name "*.bam")
do
    echo "Start parsing ${file}"
    file_out=$(basename ${file} | sed 's/_bismark_bt2\.bam/\.bam/g')
    mv ${file} ${file_out}
done
