#!/usr/bin/env bash
samples_dir=$1
cd ${samples_dir}
cat samples.txt | while read line
do
    file=$(echo ${line})
    if [[ -f ${file} ]]
    then
        echo "Start moving ${file}"
        mv ${file} download
    fi
done
