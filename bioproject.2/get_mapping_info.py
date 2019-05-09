import re
import os
import sys


def get_mapping_result(path_mapping_result):
    print(f"Start reading frm {path_mapping_result}")
    sample_mapping_result = dict()
    with open(path_mapping_result) as f:
        for line in f:
            if line.startswith("Sample"):
                continue
            line_list = line.strip().split("\t")
            # this_sample = re.sub(r"\.txt", "", line_list[0])
            this_sample = line_list[0].split(".")[0]
            # sample_mapping_result[this_sample] = line_list[1]
            sample_mapping_result[this_sample] = line_list[10]
    return sample_mapping_result


def get_samples(path_samples):
    print(f"Start reading from {path_samples}")
    samples = []
    with open(path_samples) as f:
        for line in f:
            if line.strip():
                sample = re.sub(".sra", "", os.path.basename(line.strip()))
                samples.append(sample)
    return samples


def compare(samples, sample_mapping_result, path_out):
    with open(path_out, "w+") as out:
        for each_sample in samples:
            if each_sample in sample_mapping_result:
                this_sample_values = sample_mapping_result[each_sample]
                out.write(each_sample + "\t" + this_sample_values + "\n")
            else:
                print(f"sample not in results:  {each_sample}")
                out.write(each_sample + "\t" + "NA" + "\n")


def main():
    path_mapping_result = sys.argv[1]
    path_samples = sys.argv[2]
    path_out = sys.argv[3]
    sample_mapping_result = get_mapping_result(path_mapping_result)
    samples = get_samples(path_samples)
    compare(samples, sample_mapping_result, path_out)


if __name__ == '__main__':
    main()
