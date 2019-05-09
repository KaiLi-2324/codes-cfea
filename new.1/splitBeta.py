import os
import sys
import subprocess


def parse_beta(path_beta):
    print(f"Start reading from {path_beta}")
    file = open(path_beta)
    first_line = file.__next__()
    file.close()
    line_list = first_line.strip().split("\t")
    for each_sample in line_list[1:]:
        this_sample_index = line_list.index(each_sample)
        this_sample_cut_index = this_sample_index + 1
        this_sample_out = f"{os.path.dirname(path_beta)}/{each_sample}.beta_value.txt"
        cmd = f"cut -f 1,{this_sample_cut_index} {path_beta} > "
        print(f"Start writing to {each_sample}")
        try:
            subprocess.check_output(cmd, shell=True)
        except Exception as e:
            print(e)


def main():
    path_beta = sys.argv[1]
    parse_beta(path_beta)


if __name__ == '__main__':
    main()
