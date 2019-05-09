import os
import sys
import glob
import subprocess
import multiprocessing


def get_cov_files(path_cov):
    print(f"Start reading from {path_cov}")
    cov_files = glob.glob(f"{path_cov}/*.cov")
    return cov_files


def add_chr(each_cov, path_bed):
    print(f"Start parsing {each_cov}")
    try:
        sample_name = os.path.basename(each_cov).split(".")[0]
        this_sample_out = f"{path_bed}/{sample_name}.bed"
        awk_cmd = '''awk \'BEGIN {FS="\t";OFS="\t"} {split($0, line, "\t");if(line[1] == "MT"){print "chrM",line[2],line[3],line[4],line[5],line[6]}else{chr_out="chr"""line[1];print chr_out,line[2],line[3],line[4],line[5],line[6]}}\''''
        cmd = f"cat {each_cov} | {awk_cmd} > {this_sample_out}"
        subprocess.check_output(cmd, shell=True)
    except Exception as e:
        print(e)


def multi_process_run(cov_files, path_bed):
    pool = multiprocessing.Pool(processes=50)
    for each_cov in cov_files:
        pool.apply_async(add_chr, (each_cov, path_bed,))
    pool.close()
    pool.join()


def main():
    path_cov = sys.argv[1]
    path_bed = sys.argv[2]
    if not os.path.exists(path_bed):
        os.makedirs(path_bed)
    cov_files = get_cov_files(path_cov)
    multi_process_run(cov_files, path_bed)


if __name__ == '__main__':
    main()
