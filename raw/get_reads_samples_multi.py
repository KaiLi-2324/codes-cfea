import os
import sys
import glob
import subprocess
import linecache
import multiprocessing


"""
this script is designed to count reads and samples in our project
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


def count_reads(fastq_file):
    print(f"Start counting {fastq_file}")
    this_sample_tmp_out = f"{fastq_file}.tmp.txt"
    if fastq_file.endswith(".gz"):
        cmd = f"zcat {fastq_file} | wc -l > {this_sample_tmp_out}"
    else:
        cmd = f"wc -l {fastq_file} > {this_sample_tmp_out}"
    try:
        subprocess.check_output(cmd, shell=True)
    except Exception as e:
        print(e)


def run_parallel(files):
    pool = multiprocessing.Pool(processes=60)
    for fastq_file in files:
        pool.apply_async(count_reads, (fastq_file,))
    pool.close()
    pool.join()


def count_total(path, path_out, pattern):
    tmp_files = glob.glob(f"{path}/*.tmp.txt")
    if not tmp_files:
        tmp_files = glob.glob(f"{path}/*/*.tmp.txt")
    total_reads = 0
    for each_file in tmp_files:
        this_sample_reads = int(linecache.getlines(each_file)[0].strip().split()[0])
        if this_sample_reads % 4 != 0:
            print(f"  Invalid read counts:  {each_file}")
        total_reads += this_sample_reads
    # for each_file in tmp_files:
    #    os.remove(each_file)
    samples = list(map(lambda k: os.path.basename(k).split(f"{pattern}")[0], tmp_files))
    samples = list(set(samples))
    with open(path_out, "w+") as out:
        out.write(f"total reads: {total_reads}\n")
        out.write(f"total samples: {len(samples)}")


def main():
    path = sys.argv[1]  # path to fastq files
    path_out = sys.argv[2]  # bioproject_13.reads_samples.txt
    pattern = sys.argv[3]  # pattern to split fastq names
    files = get_samples(path)
    run_parallel(files)
    count_total(path, path_out, pattern)


if __name__ == '__main__':
    main()
