import os
import glob
import argparse
import subprocess
import multiprocessing


def get_bam_files(mapping_dir):
    print(f"Start reading from {mapping_dir}")
    bam_files = glob.glob(f"{mapping_dir}/*/*.bam")
    return bam_files


def bam2cov(bam, cov_dir, log_dir):
    prefix = os.path.basename(bam).split(".")[0]
    this_cov_dir = f"{cov_dir}/{prefix}"
    this_log_dir = f"{log_dir}/{prefix}.bismark_methylation_extractor.log"
    this_error_log = f"{log_dir}/{prefix}.bismark_methylation_extractor.error.log"
    if not os.path.exists(this_cov_dir):
        os.makedirs(this_cov_dir)
    if bam.endswith("_bt2.bam"):
        cmd_cov = f"bismark_methylation_extractor -s {bam} --bedGraph --counts -o {this_cov_dir} > {this_log_dir} 2>&1"
    elif bam.endswith("_bt2_pe.bam"):
        cmd_cov = f"bismark_methylation_extractor -p {bam} --bedGraph --counts -o {this_cov_dir} > {this_log_dir} 2>&1"
    else:
        cmd_cov = "echo -e '\tInvalid bam, neither paired nor single!'"
    try:
        print(f"    Extracting coverage: {prefix}")
        subprocess.check_output(cmd_cov, shell=True)
    except Exception as e:
        print(e)
        with open(this_error_log, "w+") as out:
            out.write(str(e) + "\n")


def multi_process_run(bam_files, num_process, cov_dir, log_dir):
    pool = multiprocessing.Pool(processes=int(num_process))
    for bam in bam_files:
        pool.apply_async(bam2cov, (bam, cov_dir, log_dir,))
    pool.close()
    pool.join()


def main():
    parser = argparse.ArgumentParser(description="A program to map raw fastq and remove duplicates")
    parser.add_argument("-i", action="store", dest="mapping_dir")
    parser.add_argument("-p", action="store", dest="num_process", help="processes to use in the program", default=10)
    parser.add_argument("-c", action="store", dest="cov_dir", help="path to put mapping result in")
    parser.add_argument("-l", action="store", dest="log_dir", help="path to put log files")
    results = parser.parse_args()
    if not all([results.mapping_dir, results.num_process, results.cov_dir, results.log_dir]):
        print("too few arguments, type -h for more information")
        exit(-1)
    mapping_dir = results.mapping_dir if not results.mapping_dir.endswith("/") else results.mapping_dir.rstrip("/")
    num_process = results.num_process
    cov_dir = results.cov_dir if not results.cov_dir.endswith("/") else results.cov_dir.rstrip("/")
    log_dir = results.log_dir if not results.log_dir.endswith("/") else results.log_dir.rstrip("/")
    for each_dir in [cov_dir, log_dir]:
        if not os.path.exists(each_dir):
            os.makedirs(each_dir)
    bam_files = get_bam_files(mapping_dir)
    multi_process_run(bam_files, num_process, cov_dir, log_dir)


if __name__ == '__main__':
    main()
