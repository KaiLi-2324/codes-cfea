import re
import os
import sys
from collections import defaultdict


def get_qc_result(path_qc_result):
    print(f"Start reading frm {path_qc_result}")
    sample_qc_results = defaultdict(dict)
    with open(path_qc_result) as f:
        for line in f:
            if line.startswith("Sample"):
                continue
            line_list = line.strip().split("\t")
            if not line_list[0].endswith(".dedup.bam"):
                # sample_srr = re.sub(r".bam", "", line_list[0])
                sample_srr = line_list[0].split(".")[0]
            else:
                sample_srr = re.sub(r".dedup.bam", "", line_list[0])
            sample_qc_results[sample_srr]["adapter_content"] = line_list[1]
            sample_qc_results[sample_srr]["duplication_level"] = line_list[3]
            sample_qc_results[sample_srr]["base_quality"] = line_list[6]
            sample_qc_results[sample_srr]["basic_statistics"] = line_list[10]
            sample_qc_results[sample_srr]["overrepresented_sequences"] = line_list[15]
    return sample_qc_results


def get_samples(path_samples):
    print(f"Start reading from {path_samples}")
    samples = []
    with open(path_samples) as f:
        for line in f:
            if line.strip():
                sample = re.sub("_f1\.fastq\.gz", "", os.path.basename(line.strip().split(";")[0]))
                samples.append(sample)
    return samples


def compare(samples, sample_qc_results, path_out):
    items = ["adapter_content", "duplication_level",
             "base_quality", "basic_statistics", "overrepresented_sequences"]
    with open(path_out, "w+") as out:
        for each_sample in samples:
            if each_sample in sample_qc_results:
                this_sample_values = sample_qc_results[each_sample]
                this_sample_out = "\t".join([this_sample_values[each_item] for each_item in items])
                out.write(each_sample + "\t" + this_sample_out + "\n")
            else:
                print(f"sample not in results:  {each_sample}")
                out.write(each_sample + "\t" + "\t".join(["NA"] * 5) + "\n")


def main():
    path_qc_result = sys.argv[1]
    path_samples = sys.argv[2]
    path_out = sys.argv[3]
    sample_qc_results = get_qc_result(path_qc_result)
    samples = get_samples(path_samples)
    compare(samples, sample_qc_results, path_out)


if __name__ == '__main__':
    main()
