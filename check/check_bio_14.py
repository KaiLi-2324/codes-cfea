import re
import os
import sys
import glob


def get_raw_samples(path_raw):
    print(f"Start parsing {path_raw}")
    raw_samples = []
    with open(path_raw) as f:
        for line in f:
            if line.strip():
                raw_samples.append(re.sub(".sra", "", os.path.basename(line.strip())))
    return raw_samples


def get_result_samples(path_result):
    print(f"Start reading from {path_result}")
    result_files = glob.glob(f"{path_result}/*/*.xls")
    return list(map(lambda k: re.sub("_peaks.xls$", "", os.path.basename(k)), result_files))


def compare(raw_samples, result_samples):
    for each_sample in raw_samples:
        if each_sample not in result_samples:
            print(f"raw not result: {each_sample}")
    for each_sample in result_samples:
        if each_sample not in raw_samples:
            print(f"result sample not raw: {each_sample}")


def main():
    path_raw = sys.argv[1]
    path_result = sys.argv[2]
    raw_samples = get_raw_samples(path_raw)
    result_samples = get_result_samples(path_result)
    compare(raw_samples, result_samples)


if __name__ == '__main__':
    main()
