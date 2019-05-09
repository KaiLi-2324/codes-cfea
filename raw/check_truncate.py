import re
import os
import sys
import glob


def truncate(qc_result_dir, path_out, fastq_dir):
    print(f"Start reading from {qc_result_dir}")
    samples = list(map(lambda k: re.sub(".fastq", "", os.path.basename(k)), glob.glob(f"{fastq_dir}/*.fastq")))
    zip_samples = list(map(lambda k: re.sub("_fastqc.zip", "", os.path.basename(k)), glob.glob(f"{qc_result_dir}/*/*.zip")))
    truncate_files = []
    for each_sample in samples:
        if each_sample not in zip_samples:
            truncate_files.append(each_sample)
    if truncate_files:
        print(f"Start writing to {path_out}")
        with open(path_out, "w+") as out:
            out.write("\n".join(truncate_files) + "\n")


def main():
    if len(sys.argv) != 4:
        print("Usage: python3 check_truncate.py [qc_result_dir] [path_out] [fastq_dir]")
        exit(-1)
    qc_result_dir = sys.argv[1]
    path_out = sys.argv[2]
    fastq_dir = sys.argv[3]
    truncate(qc_result_dir, path_out, fastq_dir)


if __name__ == '__main__':
    main()
