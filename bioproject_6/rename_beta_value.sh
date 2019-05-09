#!/usr/bin/env bash
file_dir=$1
cd ${file_dir}

for file in $(find . -name "*.beta_value.*")
do
    echo "Start renaming ${file}"
    out_name=$(echo ${file} | sed 's/\.beta_value//g')
    mv ${file} ${out_name}
done
