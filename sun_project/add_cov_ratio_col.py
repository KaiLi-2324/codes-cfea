import os
import sys
import glob
import subprocess
import multiprocessing


def get_files(path_cov):
    print(f"Start reading from {path_cov}")
    cov_files = glob.glob(f"{path_cov}/*.met.cov")
    return cov_files


def add_cov_ratio(cov, cov_out_dir):
    print(f"Start parsing {cov}")
    sample = os.path.basename(cov).split(".")[0]
    cov_out = f"{cov_out_dir}/{sample}.cov"
    awk_cmd = 'awk \'BEGIN {FS="\t";OFS="\t"} {split($0, line, "\t");ratio=line[4]/(line[5]+line[4]);print line[1],line[2],line[3],ratio,line[4],line[5]}\''
    cmd = f"cat {cov} | {awk_cmd} > {cov_out}"
    try:
        subprocess.check_output(cmd, shell=True)
    except Exception as e:
        print(e)


def multi_process_run(cov_files, cov_out_dir):
    pool = multiprocessing.Pool(processes=40)
    for each_cov in cov_files:
        pool.apply_async(add_cov_ratio, (each_cov, cov_out_dir,))
    pool.close()
    pool.join()


def main():
    path_cov = sys.argv[1]
    cov_out_dir = sys.argv[2]
    cov_files = get_files(path_cov)
    multi_process_run(cov_files, cov_out_dir)


if __name__ == '__main__':
    main()
