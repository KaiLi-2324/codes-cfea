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
            sample_srr = line_list[0].split(".")[0]
            sample_qc_results[sample_srr]["adapter_content"] = line_list[1]
            sample_qc_results[sample_srr]["duplication_level"] = line_list[3]
            sample_qc_results[sample_srr]["base_quality"] = line_list[6]
            sample_qc_results[sample_srr]["basic_statistics"] = line_list[10]
            sample_qc_results[sample_srr]["overrepresented_sequences"] = line_list[15]
    return sample_qc_results


def get_mapping_results(path_mapping_result, sample_qc_results):
    print(f"Start reading from {path_mapping_result}")
    with open(path_mapping_result) as f:
        for line in f:
            if line.startswith("Sample"):
                continue
            line_list = line.strip().split("\t")
            sample_srr = line_list[0].split(".")[0]
            if sample_srr in sample_qc_results:
                sample_qc_results[sample_srr]["alignment_rate"] = line_list[1]
            else:
                raise ValueError(f"sample {sample_srr} has no mapping results!")
    return sample_qc_results


def parse_meta(path_meta, sample_qc_results):
    print(f"Start parsing {path_meta}")
    with open(path_meta) as f:
        for line in f:
            if line.startswith("sample"):
                continue
            line_list = line.strip().split("\t")
            sample_srr = re.sub(r".sra", "", os.path.basename(line_list[7])) if len(os.path.basename(line_list[7]).split(",")) == 1 else None
            if sample_srr in sample_qc_results and sample_srr is not None:
                sample_qc_results[sample_srr]["GSM"] = line_list[0]
                sample_qc_results[sample_srr]["disease_state"] = line_list[1]
                sample_qc_results[sample_srr]["PMID"] = line_list[2]
                sample_qc_results[sample_srr]["method"] = line_list[3]
                sample_qc_results[sample_srr]["sample_source"] = line_list[5]
            else:
                print(f"sample {sample_srr} is not in bioproject_13!!")
    return sample_qc_results


def write(sample_qc_results, path_out):
    print(f"Start writing to {path_out}")
    titles = ["GSM", "disease_state", "PMID", "method",
              "sample_source", "adapter_content", "duplication_level",
              "base_quality", "basic_statistics", "overrepresented_sequences", "alignment_rate"]
    with open(path_out, "w+") as out:
        out.write("sample\t" + "\t".join(titles) + "\n")
        for each_sample in sample_qc_results:
            this_sample_values = [sample_qc_results[each_sample][each_item] for each_item in titles]
            out.write(each_sample + "\t" + "\t".join(this_sample_values) + "\n")


def main():
    path_qc_result = sys.argv[1]  # multiqc_fastqc.txt
    path_mapping_result = sys.argv[2]  # multiqc_bowtie2.txt
    path_meta = sys.argv[3]  # cfDNA_samples_meta_plasma.xls
    path_out = sys.argv[4]  # bio_project_13_meta_qc_to_sql.xls
    sample_qc_results = get_qc_result(path_qc_result)
    sample_qc_results = get_mapping_results(path_mapping_result, sample_qc_results)
    sample_qc_results = parse_meta(path_meta, sample_qc_results)
    write(sample_qc_results, path_out)


if __name__ == '__main__':
    main()
