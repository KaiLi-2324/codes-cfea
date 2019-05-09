import re
import sys


def parse_file(path_raw):
    # print(f"Start reading from {path_raw}")
    with open(path_raw) as file:
        for line in file:
            if line.startswith("sample"):
                continue
            line_list = line.strip().split("\t")
            if re.search("benign", line_list[1]):
                print("benign")
            else:
                print(line_list[14])


def main():
    path_raw = sys.argv[1]
    parse_file(path_raw)


if __name__ == '__main__':
    main()
