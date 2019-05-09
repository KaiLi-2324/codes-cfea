#!/usr/bin/env bash
file_dir=$1
cd ${file_dir}

for file in $(find . -name "*.bismark.cov.gz" -maxdepth 1)
do
    echo "Start parsing ${file}"
    file_out=$(basename ${file} | sed 's/_bismark_bt2\.bismark\.cov\.gz/\.cov\.gz/g')
    mv ${file} ${file_out}
done
