import os
import sys
import glob
import subprocess
import multiprocessing


def get_files(path, pattern):
    print(f"Start reading from {path}")
    wig_files = glob.glob(f"{path}/*.{pattern}")
    if not wig_files:
        wig_files = glob.glob(f"{path}/*.{pattern}.gz")
    return wig_files


def add_header(path):
    print(f"Start parsing {path}")
    try:
        sample_name = os.path.basename(path).split(".")[0]
        header = f"track type=wiggle_0 name={sample_name}"
        file = path
        if path.endswith(".gz"):
            subprocess.check_output(f"gzip -d {path}", shell=True)
            file = path[:-3]
        cmd = f"sed -i '1i\{header}' {file}"
        subprocess.check_output(cmd, shell=True)
    except Exception as e:
        print(e)


def multi_process_run(wig_files):
    pool = multiprocessing.Pool(processes=50)
    for each_file in wig_files:
        pool.apply_async(add_header, (each_file,))
    pool.close()
    pool.join()


def main():
    path = sys.argv[1]
    pattern = sys.argv[2]
    wig_files = get_files(path, pattern)
    multi_process_run(wig_files)


if __name__ == '__main__':
    main()
