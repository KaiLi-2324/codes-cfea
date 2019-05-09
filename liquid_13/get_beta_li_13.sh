#!/usr/bin/env bash
FILE_DIR=$1
cd ${FILE_DIR}
for file in $(find . -name "*.txt")
do
    echo "Start parsing ${file}"
    PREFIX=$(basename ${file} | sed 's/.txt//g')
    OUT_FILE="${PREFIX}.beta_value.txt"
    echo -e "pos\tbeta_value\tp_value" > ${OUT_FILE}
    cat ${file} | grep -P '^cg[0-9]+\s+' >> ${OUT_FILE}
done
