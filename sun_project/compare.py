import sys


def parse_a(path_a):
    print(f"Start reading from {path_a}")
    sample_a = []
    with open(path_a) as f:
        for line in f:
            if line.strip():
                sample = line.strip()
                sample_a.append(sample)
    return sample_a


def parse_b(path_b):
    print(f"Start reading from {path_b}")
    sample_b = []
    with open(path_b) as f:
        for line in f:
            if line.strip():
                sample = line.strip()
                sample_b.append(sample)
    return sample_b


def compare(sample_a, sample_b):
    for each_sample in sample_a:
        if each_sample not in sample_b:
            print(f"in a not in b:  {each_sample}")
    for each_sample in sample_b:
        if each_sample not in sample_a:
            print(f"in b not in a:  {each_sample}")


def main():
    path_a = sys.argv[1]
    path_b = sys.argv[2]
    sample_a = parse_a(path_a)
    sample_b = parse_b(path_b)
    compare(sample_a, sample_b)


if __name__ == '__main__':
    main()
