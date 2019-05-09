import re
import sys


def parse_meta(path, path_out):
    print(f"Start parsing {path}")
    out = open(path_out, "w+")
    with open(path) as f:
        for line in f:
            if line.startswith("sample"):
                continue
            line_list = line.strip().split("\t")
            line_list = list(map(lambda k: k.strip(), line_list))
            if len(line_list) == 0:
                continue
            pmid = re.sub('\.0$', '', line_list[2])
            mysql_cmd = f"INSERT INTO meta VALUE ('{line_list[23]}', '{line_list[0]}', '{line_list[1]}', '{line_list[11]}', '{line_list[12]}', '{pmid}', '{line_list[3]}', '{line_list[26]}', '{line_list[10]}', '{line_list[6]}', '{line_list[15]}', '{line_list[13]}', '{line_list[14]}', '{line_list[17]}', '{line_list[18]}', '{line_list[19]}', '{line_list[20]}', '{line_list[21]}', '{line_list[22]}', '{line_list[24]}');"
            out.write(mysql_cmd + "\n")
    out.close()


def main():
    path = sys.argv[1]
    path_out = sys.argv[2]
    parse_meta(path, path_out)


if __name__ == '__main__':
    main()
