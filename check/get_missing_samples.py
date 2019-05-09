import re
import os
import sys
import glob


def get_fastq_files(path_fastq, fastq_pattern):
    print(f"Start reading from {path_fastq}")
    fastq_files = glob.glob(f"{path_fastq}/*{fastq_pattern}")
    fastq_samples = []
    for each_file in fastq_files:
        each_sample = re.sub(f"{fastq_pattern}", "", os.path.basename(each_file))
        fastq_samples.append(each_sample)
    return fastq_samples


def get_bam_files(path_bam, bam_pattern):
    print(f"Start reading from {path_bam}")
    bam_files = glob.glob(f"{path_bam}/*{bam_pattern}")
    bam_samples = []
    for each_file in bam_files:
        each_sample = re.sub(f"{bam_pattern}", "", os.path.basename(each_file))
        bam_samples.append(each_sample)
    return bam_samples


def get_missing_samples(fastq_samples, bam_samples):
    print("Start searching for missing samples")
    if len(fastq_samples) > len(bam_samples):
        for each_sample in fastq_samples:
            if each_sample not in bam_samples:
                print(each_sample)
    else:
        for each_sample in bam_samples:
            if each_sample not in fastq_samples:
                print(each_sample)


def main():
    path_fastq = sys.argv[1]
    path_bam = sys.argv[2]
    fastq_pattern = sys.argv[3]
    bam_pattern = sys.argv[4]
    fastq_samples = get_fastq_files(path_fastq, fastq_pattern)
    bam_samples = get_bam_files(path_bam, bam_pattern)
    get_missing_samples(fastq_samples, bam_samples)


if __name__ == '__main__':
    main()
