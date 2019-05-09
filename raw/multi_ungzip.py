import sys
import glob
import subprocess
import multiprocessing


def get_files(path_gz):
    print(f"Start reading from {path_gz}")
    gzip_files = glob.glob(f"{path_gz}/*.gz")
    return gzip_files


def unzip_file(each_file):
    print(f"  unzipping:  {each_file}")
    try:
        cmd = f"gzip -d {each_file}"
        subprocess.check_output(cmd, shell=True)
    except Exception as e:
        print(e)


def multi_process_run(gzip_files):
    pool = multiprocessing.Pool(processes=40)
    for each_file in gzip_files:
        pool.apply_async(unzip_file, (each_file,))
    pool.close()
    pool.join()


def main():
    path_gz = sys.argv[1]
    gzip_files = get_files(path_gz)
    multi_process_run(gzip_files)


if __name__ == '__main__':
    main()
