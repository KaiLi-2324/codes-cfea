#!/usr/bin/env bash
cov_dir=$1
cd ${cov_dir}

for file in $(find . -name "*.cov")
do
    prefix=$(basename ${file} | sed s'/\.cov//g')
    out_file="${prefix}.bed"
    echo "  Renaming ${file} to ${out_file}"
    mv ${file} ${out_file}
done
