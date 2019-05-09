import os
import sys
import glob
import subprocess
import multiprocessing


def get_files(path_fastq):
    print(f"Start reading from {path_fastq}")
    fastq_files = glob.glob(f"{path_fastq}/*.gz")
    return fastq_files


def rename(fastq):
    print(f"Start renaming {fastq}")
    try:
        sample = os.path.basename(fastq).split(".")[0]
        sample_name = sample.split("_")[0]
        read = sample.split("_")[1]
        new_name = f"{sample_name}.sra_{read}.fastq.gz"
        os.rename(fastq, f"{os.path.dirname(fastq)}/{new_name}")
        cmd = f"gzip -d {os.path.dirname(fastq)}/{new_name}"
        subprocess.check_output(cmd, shell=True)
    except Exception as e:
        print(e)


def multi_process_run(fastq_files):
    pool = multiprocessing.Pool(processes=30)
    for each_fastq in fastq_files:
        pool.apply_async(rename, (each_fastq,))
    pool.close()
    pool.join()


def main():
    path_fastq = sys.argv[1]
    fastq_files = get_files(path_fastq)
    multi_process_run(fastq_files)


if __name__ == '__main__':
    main()
