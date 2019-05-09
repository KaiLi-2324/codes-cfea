import sys
import glob
import subprocess


"""
this script is designed to count samples and reads in our project 
__author__ = likai
"""


def get_samples(path):
    print(f"Start reading from {path}")
    files = glob.glob(f"{path}/*.fastq")
    if not files:
        files = glob.glob(f"{path}/*.gz")
        if not files:
            files = glob.glob(f"{path}/*/*.gz")
    return files


def count_reads(files):
    total_reads = 0
    for each_file in files:
        print(f"Start counting {each_file}")
        if each_file.endswith(".gz"):
            cmd = f"zcat {each_file} | wc -l"
        else:
            cmd = f"wc -l {each_file}"
        this_sample_reads = int(subprocess.check_output(cmd, shell=True).decode().split()[0])
        total_reads += this_sample_reads
    print(f"total reads:     {total_reads}")
    print(f"total samples:   {len(files)}")


def main():
    path = sys.argv[1]  # path to fastq files
    files = get_samples(path)
    count_reads(files)


if __name__ == '__main__':
    main()
