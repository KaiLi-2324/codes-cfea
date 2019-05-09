#!/usr/bin/env bash
bed_dir=$1
cd ${bed_dir}

for file in $(find . -name "*.txt")
do
    prefix=$(basename ${file} | sed s'/\.txt//g')
    cov="${prefix}.cov"
    if [[ -f ${cov} ]]
    then
        echo "${cov} exists!"
    else
        echo "Renaming ${file} to ${cov}"
        mv ${file} ${cov}
    fi
done
