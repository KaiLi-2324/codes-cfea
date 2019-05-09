#!/usr/bin/env bash
fastq_dir=$1
missing_fastq_dir=$2
missing_file_name=$3

cat ${missing_file_name} | while read line
do
    for file in $(find ${fastq_dir} -name "${line}*")
    do
        echo "moving ${file}"
        mv ${file} ${missing_fastq_dir}
       done
done

