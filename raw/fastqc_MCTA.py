import os
import glob
import argparse
import subprocess
import multiprocessing


def get_files(path_fastq):
    print(f"Start reading from {path_fastq}")
    fastq_samples = os.listdir(path_fastq)
    return fastq_samples


def run_fastqc(each_sample, path_fastq, qc_result_dir, log_dir):
    try:
        print(f"  Fastqc: {each_sample}")
        this_sample_result_dir = f"{qc_result_dir}/{each_sample}"
        this_sample_log = f"{log_dir}/{each_sample}.raw_qc.error.log"
        if not os.path.exists(this_sample_result_dir):
            os.makedirs(this_sample_result_dir)
        fastq_file1 = f"{path_fastq}/{each_sample}/{each_sample}_R1.fastq.gz"
        fastq_file2 = f"{path_fastq}/{each_sample}/{each_sample}_R2.fastq.gz"
        cmd = f"fastqc -q --extract -o {this_sample_result_dir} {fastq_file1} {fastq_file2}"
        subprocess.check_output(cmd, shell=True)
    except Exception as e:
        print(e)
        with open(this_sample_log, "w+") as out:
            out.write(str(e) + "\n")


def multi_process_run(fastq_samples, path_fastq, num_process, qc_result_dir, log_dir):
    pool = multiprocessing.Pool(processes=int(num_process))
    for each_sample in fastq_samples:
        pool.apply_async(run_fastqc, (each_sample, path_fastq, qc_result_dir, log_dir,))
    pool.close()
    pool.join()


def get_fastqc_zip_file(qc_result_dir):
    print(f"Start searching for zip results from {qc_result_dir}")
    zip_files = glob.glob(f"{qc_result_dir}/*/*.zip")
    multiqc_file_path = f"{qc_result_dir}/multiqc_sample.txt"
    with open(multiqc_file_path, "w+") as out:
        out.write("\n".join(zip_files) + "\n")
    return multiqc_file_path


def multiqc(multiqc_file_path, n, qc_result_dir):
    print("Start multiQC")
    cmd = f"multiqc -n {n} -s -o {qc_result_dir} -l {multiqc_file_path}"
    try:
        subprocess.check_output(cmd, shell=True)
    except Exception as e:
        print(e)


def main():
    parser = argparse.ArgumentParser(description="A program to do FastQC and MultiQC for MCTA-seq data")
    parser.add_argument("-i", action="store", dest="path_fastq")
    parser.add_argument("-p", action="store", dest="num_process", help="processes to use in the program", default=40)
    parser.add_argument("-q", action="store", dest="qc_result_dir", help="path to put qc result in")
    parser.add_argument("-l", action="store", dest="log_dir", help="path to put log files")
    parser.add_argument("-n", action="store", dest="n", help="project name to use in MultiQC output[bioproject.13]")
    results = parser.parse_args()
    if not all([results.path_fastq, results.num_process, results.qc_result_dir, results.log_dir, results.n]):
        print("too few arguments, type -h for more information!")
        exit(-1)
    path_fastq = results.path_fastq if not results.path_fastq.endswith("/") else results.path_fastq.rstrip("/")
    num_process = results.num_process
    qc_result_dir = results.qc_result_dir if not results.qc_result_dir.endswith("/") else results.qc_result_dir.rstrip(
        "/")
    log_dir = results.log_dir if not results.log_dir.endswith("/") else results.log_dir.rstrip("/")
    n = results.n
    fastq_samples = get_files(path_fastq)
    multi_process_run(fastq_samples, path_fastq, num_process, qc_result_dir, log_dir)
    multiqc_file_path = get_fastqc_zip_file(qc_result_dir)
    multiqc(multiqc_file_path, n, qc_result_dir)


if __name__ == '__main__':
    main()
