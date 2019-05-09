import sys


def parse_samples(path_samples):
    print(f"Start reading from {path_samples}")
    samples = []
    with open(path_samples) as f:
        for line in f:
            if line.strip():
                sample = line.strip()
                samples.append(sample)
    return samples


def parse_mapping(path_mapping):
    print(f"Start reading from {path_mapping}")
    sample_mapping_rate = dict()
    with open(path_mapping) as f:
        for line in f:
            if line.strip():
                line_list = line.strip().split("\t")
                sample_mapping_rate[line_list[1]] = line_list[0]
    return sample_mapping_rate


def get_mapping_info(samples, sample_mapping_rate, path_out):
    print(f"Start writing to {path_out}")
    with open(path_out, "w+") as out:
        for each_sample in samples:
            if each_sample in sample_mapping_rate:
                this_sample_rate = sample_mapping_rate[each_sample]
                out.write(each_sample + "\t" + this_sample_rate + "\n")
            else:
                print(f"sample not in mapping rate:  {each_sample}")
                out.write(each_sample + "\t" + "NA" + "\n")


def main():
    path_samples = sys.argv[1]
    path_mapping = sys.argv[2]
    path_out = sys.argv[3]
    samples = parse_samples(path_samples)
    sample_mapping_rate = parse_mapping(path_mapping)
    get_mapping_info(samples, sample_mapping_rate, path_out)


if __name__ == '__main__':
    main()
