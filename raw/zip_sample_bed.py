import re
import os
import sys
import subprocess
import multiprocessing
from collections import defaultdict


def parse_meta(path_meta):
    print(f"Start reading from {path_meta}")
    zip_samples = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    with open(path_meta) as file:
        for line in file:
            if line.startswith("sample"):
                continue
            line_list = line.strip().split("\t")
            if len(line_list) == 0:
                continue
            marker = line_list[4].strip()
            disease_state = re.sub(" ", "_", line_list[1].strip())
            method = re.sub(" ", "_", line_list[3].strip())
            cfea_number = line_list[23]
            if os.path.exists(f"{cfea_number}.bed"):
                zip_samples[marker][method][disease_state].append(f"{cfea_number}.bed")
            else:
                print(f"{cfea_number}.bed does not exist!")
    return zip_samples


def zip_cmd(this_sample_out, this_sample_files):
    try:
        cmd = f"zip -r {this_sample_out} {this_sample_files}"
        subprocess.check_output(cmd, shell=True)
    except Exception as e:
        print(e)


def zip_file(zip_samples):
    print("Start zipping samples")
    pool = multiprocessing.Pool(processes=30)
    for each_marker in zip_samples:
        for each_method in zip_samples[each_marker]:
            for each_disease in zip_samples[each_marker][each_method]:
                if each_marker == "DNA methylation":
                    this_sample_out = f"5mc_{each_method}_{each_disease}.zip"
                elif each_marker == "DNA hydroxymethylation":
                    this_sample_out = f"5hmc_{each_method}_{each_disease}.zip"
                else:
                    this_sample_out = f"np_{each_method}_{each_disease}.zip"
                this_sample_files = " ".join(zip_samples[each_marker][each_method][each_disease])
                print(f"Zipping:  {this_sample_out}")
                pool.apply_async(zip_cmd, (this_sample_out, this_sample_files,))
    pool.close()
    pool.join()


def main():
    # please place this file in the bed directory
    path_meta = sys.argv[1]
    zip_samples = parse_meta(path_meta)
    zip_file(zip_samples)


if __name__ == '__main__':
    main()
