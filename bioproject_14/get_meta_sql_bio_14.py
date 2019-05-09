import os
import re
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
            sample_srr = re.sub(r".dedup.bam", "", line_list[0])
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
            sample_srr = re.sub(r".txt", "", line_list[0])
            if sample_srr in sample_qc_results:
                sample_qc_results[sample_srr]["alignment_rate"] = line_list[1]
            else:
                raise ValueError(f"sample {sample_srr} has no mapping results!")
    return sample_qc_results


def parse_meta(path_meta, sample_qc_results, pmid):
    print(f"Start parsing {path_meta}")
    with open(path_meta) as f:
        for line in f:
            if line.startswith("sample"):
                continue
            line_list = line.strip().split("\t")
            if len(line_list[8].split(",")) == 2:
                continue
            sample_srr = re.sub(r".sra", "", os.path.basename(line_list[8]))
            if int(line_list[2]) != "NA" and pmid == int(line_list[2]):
                if sample_srr in sample_qc_results:
                    sample_qc_results[sample_srr]["GSM"] = line_list[0]
                    sample_qc_results[sample_srr]["diseases"] = line_list[1]
                    sample_qc_results[sample_srr]["PMID"] = line_list[2]
                    sample_qc_results[sample_srr]["technical"] = line_list[3]
                    sample_qc_results[sample_srr]["source"] = line_list[6]
                    sample_qc_results[sample_srr]["stage"] = line_list[13]
                else:
                    print(f"sample {sample_srr} is not in bioproject_14!!")
    return sample_qc_results


def write(sample_qc_results, path_out):
    print(f"Start writing to {path_out}")
    titles = ["GSM", "diseases", "PMID", "technical",
              "source", "stage", "adapter_content", "duplication_level",
              "base_quality", "basic_statistics", "overrepresented_sequences", "alignment_rate"]
    with open(path_out, "w+") as out:
        out.write("sample" + "\t" + "\t".join(titles) + "\n")
        for each_sample in sample_qc_results:
            this_sample_values = []
            for each_item in titles:
                if each_item in sample_qc_results[each_sample]:
                    this_sample_values.append(sample_qc_results[each_sample][each_item])
                else:
                    this_sample_values.append("NA")
            # if "NA" not in this_sample_values:
            if this_sample_values[0] != "NA" and this_sample_values[1] != "NA" and this_sample_values[2] != "NA":
                out.write(each_sample + "\t" + "\t".join(this_sample_values) + "\n")


def main():
    path_qc_result = sys.argv[1]  # multiqc_fastqc.txt
    path_mapping_result = sys.argv[2]  # multiqc_bowtie2.txt
    path_meta = sys.argv[3]  # cfDNA_samples_meta_plasma.xls
    path_out = sys.argv[4]  # bioproject_14_meta_qc_to_sql.xls
    pmid = int(sys.argv[5])
    sample_qc_results = get_qc_result(path_qc_result)
    sample_qc_results = get_mapping_results(path_mapping_result, sample_qc_results)
    sample_qc_results = parse_meta(path_meta, sample_qc_results, pmid)
    write(sample_qc_results, path_out)


if __name__ == '__main__':
    main()
