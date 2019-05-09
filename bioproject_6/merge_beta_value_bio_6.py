import os
import sys
import glob
from collections import defaultdict


def get_files(path_raw):
    print(f"Start reading from {path_raw}")
    beta_value_files = glob.glob(f"{path_raw}/*.txt")
    return beta_value_files


def merge_beta_value(beta_value_files):
    total_samples = []
    each_sample_beta_value = defaultdict(dict)
    for each_file in beta_value_files:
        print(f"Start parsing {each_file}")
        this_sample_name = os.path.basename(each_file).split("-")[0]
        total_samples.append(this_sample_name)
        with open(each_file) as f:
            for line in f:
                if line.startswith("#") or line.startswith("ID_REF"):
                    continue
                line_list = line.strip().split("\t")
                if len(line_list) == 2:
                    each_sample_beta_value[line_list[0]][this_sample_name] = line_list[1]
    return each_sample_beta_value, total_samples


def write(each_sample_beta_value, total_samples, path_out):
    print(f"Start writing to {path_out}")
    with open(path_out, "w+") as out:
        out.write("pos\t" + "\t".join(total_samples) + "\n")
        for each_pos in each_sample_beta_value:
            this_pos_values = each_sample_beta_value[each_pos]
            this_pos_out = []
            for each_sample in total_samples:
                if each_sample in this_pos_values:
                    this_pos_out.append(this_pos_values[each_sample])
                else:
                    this_pos_out.append("NA")
            if "NA" not in this_pos_out:
                out.write(each_pos + "\t" + "\t".join(this_pos_out) + "\n")


def main():
    if len(sys.argv) != 3:
        print("USage: python merge_beta_bio_6.py [path_to_raw_beta] [bioproject_beta_value.txt]")
        exit(-1)
    path_raw = sys.argv[1]
    path_out = sys.argv[2]
    beta_value_files = get_files(path_raw)
    each_sample_beta_value, total_samples = merge_beta_value(beta_value_files)
    write(each_sample_beta_value, total_samples, path_out)


if __name__ == '__main__':
    main()
