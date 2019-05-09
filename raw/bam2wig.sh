#!/usr/bin/env bash

# this script is designed to convert 5hmc/Methyl-cap seq bam files into wig file
# __author__ = likai
# __email__ = likai@wibe.ac.cn

# before running this script, we have to install deeptools, one convenient way
# is to install through conda, and make sure bigWigToWig is in your environment

# conda create -n py2 python=2.7
# conda install -n py2 deeptools
# source activate py2


source activate /share/pub/lik/soft/miniconda3/envs/py2
bam_dir=$1
wig_dir=$2


if [[ $# != 2 ]]
then
    echo
    echo "Usage:"
    echo "    bash bam2wig.sh [bam_dir] [wig_dir]"
    echo
fi


if [[ ! -d ${wig_dir} ]]
then
    echo "${wig_dir} does not exist, creating it..."
    mkdir ${wig_dir}
fi


cd ${bam_dir}
bam_files=$(find . -name "*.dedup.bam")


if [[ ${#bam_files} == 0 ]]
then
    echo "No bam files found in your directory, please check it!"
    exit -1
fi


function bam2wig {
    # we use bamCoverage to convert bam into bigwig after making index files by samtools
    # and finally convert bigwig to wig file by bigWigToWig
    this_bam=$1
    prefix=$(basename ${this_bam} | sed s'/.dedup.bam//g')
    echo "Start parsing ${prefix}"
    bigwig="${prefix}.bw"
    samtools index -@ 30 ${this_bam}
    bamCoverage -p 2 --normalizeUsing RPKM --binSize 100 -b ${this_bam} -o ${bigwig}
    wig="${prefix}.wig"
    bigWigToWig ${bigwig} ${wig}
    echo "Finish parsing ${prefix}"
    mv ${bigwig} ${wig_dir}
    mv ${wig} ${wig_dir}
}


mkfifo tmp
exec 5<>tmp
rm -rf tmp

for((i=1;i<=30;i++))
do
    echo -ne "\n" 1>&5;
done

for bam in ${bam_files}
do
    read -u5
    {
        bam2wig ${bam}
        echo -ne "\n" 1>&5
    }&
done
wait
exec 5>&-



