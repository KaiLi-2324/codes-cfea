#!/usr/bin/env bash
SRA_DIR=$1

cd ${SRA_DIR}
for file in $(find . -name "*.sra")
do
    PREFIX=$(basename ${file} | sed 's/.sra//g')
    FASTQ_SINGLE="${PREFIX}.sra.fastq"
    FASTQ_PAIRED_1="${PREFIX}.sra_1.fastq"
    FASTQ_PAIRED_2="${PREFIX}.sra_2.fastq"
    if [[ ! -f ${FASTQ_SINGLE} && ! -f ${FASTQ_PAIRED_1} && ! -f ${FASTQ_PAIRED_2} ]]
    then
        echo ${file}
    fi
done