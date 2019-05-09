import sys
import glob
import subprocess
import multiprocessing


def get_files(path_fastq):
    if path_fastq.endswith(".gz"):
        cmd = f"zcat {path_fastq} | sed -n '$p'"
    else:
        cmd = f"sed -n '$p' {path_fastq}"
    result = subprocess.check_output(cmd, shell=True)
    if not result.decode().endswith("\n"):
        print(f"Truncated file: {path_fastq}")


def multiprocess_run(path):
    print(f"Start reading from {path}")
    fastq_files = glob.glob(f"{path}/*.fastq")
    if not fastq_files:
        fastq_files = glob.glob(f"{path}/*.fastq.gz")
    pool = multiprocessing.Pool(processes=60)
    for each_file in fastq_files:
        pool.apply_async(get_files, (each_file,))
    pool.close()
    pool.join()


def main():
    path = sys.argv[1]
    multiprocess_run(path)


if __name__ == '__main__':
    main()
