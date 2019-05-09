import sys


def parse_meta(path_meta):
    # print(f"Start reading from {path_meta}")
    with open(path_meta) as f:
        for line in f:
            if line.startswith("sample"):
                continue
            line_list = line.strip().split("\t")
            qc_info = line_list[17:22]
            if qc_info.count("NA") != 0 and qc_info.count("NA") != 5:
                raise ValueError("Invalid number of NA")
            for i in range(len(qc_info)):
                if qc_info[i] == "warn":
                    qc_info[i] = "pass"
            if qc_info.count("pass") >= 3:
                print("pass")
            elif qc_info.count("NA") == 5:
                print("NA")
            else:
                print("fail")


def main():
    path_meta = sys.argv[1]
    parse_meta(path_meta)


if __name__ == '__main__':
    main()
