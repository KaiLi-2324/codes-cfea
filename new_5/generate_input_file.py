import os
import sys
from collections import defaultdict


def parse_raw_file(path_raw):
    print(f"Start reading from {path_raw}")
    sample_input = defaultdict(dict)
    with open(path_raw) as file:
        for line in file:
            if line.startswith("Source Name"):
                continue
            line_list = line.strip().split("\t")
            source_name = line_list[0]
            url = line_list[33]
            sample = os.path.basename(url).split("_")[0]
            sample_input[source_name.split("_")[0]][source_name.split("_")[1]] = sample
    return sample_input


def write(sample_input, path_out):
    print(f"Start writing to {path_out}")
    with open(path_out, "w+") as out:
        out.write("5-mC\tinput\n")
        for each_sample in sample_input:
            this_sample_5mc = sample_input[each_sample]["5-mC"]
            this_sample_input = sample_input[each_sample]["input"]
            out.write(this_sample_5mc + "\t" + this_sample_input + "\n")


def main():
    path_raw = sys.argv[1]
    path_out = sys.argv[2]
    sample_input = parse_raw_file(path_raw)
    write(sample_input, path_out)


if __name__ == '__main__':
    main()
