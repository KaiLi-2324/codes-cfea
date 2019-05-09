import os
import sys


def parse_meta(path_meta):
    print(f"Start parsing {path_meta}")
    total_samples = []
    with open(path_meta) as f:
        for line in f:
            if line.startswith("sample"):
                continue
            line_list = line.strip().split("\t")
            sra = os.path.basename(line_list[8]).split(".")[0]
            total_samples.append(sra)
    return total_samples


def parse_run_table(path_run_table):
    print(f"Start reading from {path_run_table}")
    sra_samples = []
    with open(path_run_table) as f:
        for line in f:
            if line.startswith("Assay_Type"):
                continue
            line_list = line.strip().split("\t")
            sra_samples.append(line_list[12])
    return sra_samples


def compare(total_samples, sra_samples):
    print("Start comparing")
    for each_sample in sra_samples:
        if each_sample not in total_samples:
            print(each_sample)


def main():
    path_meta = sys.argv[1]
    path_run_table = sys.argv[2]
    total_samples = parse_meta(path_meta)
    sra_samples = parse_run_table(path_run_table)
    compare(total_samples, sra_samples)


if __name__ == '__main__':
    main()
