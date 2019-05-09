import sys
import xlrd
from collections import defaultdict


def parse_excel(path_excel):
    print(f"Start reading from {path_excel}")
    data = xlrd.open_workbook(path_excel)
    sheets = data.sheet_names()
    excel_data = defaultdict(list)
    for each_sheet in sheets:
        print(f"Start parsing sheet {each_sheet}")
        table = data.sheet_by_name(each_sheet)
        for each_row in range(table.nrows):
            this_line = table.row(each_row)
            this_line = list(map(lambda k: str(k.value), this_line))
            excel_data[each_sheet].append(this_line)
    return excel_data


def write(excel_data, path_out):
    print(f"Start writing to {path_out}")
    for each_sheet in excel_data:
        print(f"Start writing sheet {each_sheet}")
        this_sheet_out = f"{path_out}.{each_sheet}"
        this_sheet_values = excel_data[each_sheet]
        with open(this_sheet_out, "w+") as out:
            for each_line in this_sheet_values:
                out.write("\t".join(each_line) + "\n")


def main():
    path_excel = sys.argv[1]
    path_out = sys.argv[2]
    excel_data = parse_excel(path_excel)
    write(excel_data, path_out)


if __name__ == '__main__':
    main()
