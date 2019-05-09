#!/usr/bin/env bash
cov_dir=$1
cd ${cov_dir}
for file in $(find . -name "*.cov.gz")
do
    echo "Start parsing ${file}"
    file_out="${file}.tmp"
    zcat ${file} | awk 'BEGIN{FS="\t";OFS="\t"}{split($0, line, "\t");cov=line[4];cov_out=cov/100;print $1,$2,$3,cov_out,$5,$6}' > ${file_out}
    if [[ ! -d "Raw" ]]
    then
        mkdir "Raw"
    fi
    mv ${file} "Raw"
    gzip ${file_out}
    mv "${file_out}.gz" ${file}
done
