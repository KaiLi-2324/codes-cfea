import re
import sys
import urllib.request as ur
from collections import defaultdict


def crawl_page(url):
    # for example, url is http://bigd.big.ac.cn/bioproject/browse/PRJCA000816
    print(f"Start crawling from {url}")
    each_sample_info = defaultdict(dict)
    response = ur.urlopen(url)
    html = response.read().decode()
    pattern_sam = re.compile(r'<a href=\"\.\./\.\./biosample/browse/(SAM.*?)\">')
    pattern_cra = re.compile(r'<a href=\"\.\./\.\./gsa/browse/(CRA.*?)\">')
    total_sams = pattern_sam.findall(html)
    cra = pattern_cra.findall(html)[0]
    if len(pattern_cra.findall(html)) >= 2:
        raise ValueError("Length of cra >= 2!")
    for each_sam in total_sams:
        print(f"\tStart crawling sample {each_sam}")
        sam_url = f"http://bigd.big.ac.cn/biosample/browse/{each_sam}"
        sam_response = ur.urlopen(sam_url)
        sam_html = sam_response.read().decode()
        this_sample = re.findall(r'<th width=\"160\">Accession</th>\s+<td>(SAM.*?)<span></span></td>', sam_html)[0]
        this_sample_name = re.findall(r'<th>Sample name</th>\s+<td>(.*?)</td>', sam_html)[0]
        this_sample_title = re.findall(r'<th>Title</th>\s+<td>(.*?)</td>', sam_html)[0]
        this_sample_org = re.findall(r'<th>Organism</th>\s+<td><a href=\"https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax\.cgi\?id=9606\" target=\"_blank\">(.*?)</a></td>', sam_html)[0]
        this_sample_description = re.findall(r'<th>Description</th>\s+<td>(.*?)</td>', sam_html)[0]
        this_sample_tissue = re.findall(r'<th>\s+Tissue\s+</th>\s+<td>\s+(.*?)\s+</td>', sam_html)[0]
        this_cell_type = re.findall(r'<th>\s+Cell type\s+</th>\s+<td>\s+(.*?)\s+</td>', sam_html)[0]
        this_disease_state = re.findall(r'<th>\s+Disease stage\s+</th>\s+<td>\s+(.*?)\s+</td>', sam_html)[0]
        this_disease = re.findall(r'<th>\s+Disease\s+</th>\s+<td>\s+(.*?)\s+</td>', sam_html)[0]
        this_phenotype = re.findall(r'<th>\s+Phenotype\s+</th>\s+<td>\s+(.*?)\s+</td>', sam_html)[0]
        each_sample_info[each_sam]["sample"] = this_sample if this_sample else "NA"
        each_sample_info[each_sam]["sample_name"] = this_sample_name if this_sample_name else "NA"
        each_sample_info[each_sam]["sample_title"] = this_sample_title if this_sample_title else "NA"
        each_sample_info[each_sam]["organism"] = this_sample_org if this_sample_org else "NA"
        each_sample_info[each_sam]["sample_description"] = this_sample_description if this_sample_description else "NA"
        each_sample_info[each_sam]["sample_tissue"] = this_sample_tissue if this_sample_tissue else "NA"
        each_sample_info[each_sam]["cell_type"] = this_cell_type if this_cell_type else "NA"
        each_sample_info[each_sam]["disease_state"] = this_disease_state if this_disease_state else "NA"
        each_sample_info[each_sam]["disease"] = this_disease if this_disease else "NA"
        each_sample_info[each_sam]["phenotype"] = this_phenotype if this_phenotype else "NA"
    print("Finish parsing each sample page, start crawling crr")
    cra_url = f"http://bigd.big.ac.cn/gsa/browse/{cra}"
    cra_response = ur.urlopen(cra_url)
    cra_html = cra_response.read().decode()
    page = int(re.findall(r'<li class=\"total\">Page&nbsp;1/(\d+)&nbsp;</li>', cra_html)[0])
    for i in range(1, page + 1):
        print(f'\tStart crawling page {i}')
        each_cra_url = f"http://bigd.big.ac.cn/gsa/browse/detail?pageNo={i}&pageSize=20&accession={cra}"
        each_cra_response = ur.urlopen(each_cra_url)
        each_cra_html = each_cra_response.read().decode()
        each_page_samples = re.findall(r'<a href=\"http://bigd.big.ac.cn/biosample/browse/(SAM.*?)\">', each_cra_html)
        each_page_cra = re.findall(r'<a href=\"browse/CRA.*/(CRR.*?)\">', each_cra_html)
        if len(each_page_samples) != len(each_page_cra):
            raise ValueError("length of each_page_samples not equal to each_page_cra")
        for j in range(len(each_page_samples)):
            this_sample_cra = each_page_cra[j]
            this_cra_ftp_1 = f"ftp://download.big.ac.cn/gsa/{cra}/{this_sample_cra}/{this_sample_cra}_f1.fastq.gz"
            this_cra_ftp_2 = f"ftp://download.big.ac.cn/gsa/{cra}/{this_sample_cra}/{this_sample_cra}_r2.fastq.gz"
            each_sample_info[each_page_samples[j]]["CRR"] = f"{this_cra_ftp_1};{this_cra_ftp_2}"
    print(each_sample_info)
    return each_sample_info


def write(path_out, each_sample_info):
    items = ["sample_name", "sample_title", "organism", "sample_description",
             "sample_tissue", "cell_type", "disease_state", "disease", "phenotype", "CRR"]
    print(f"Start writing to {path_out}")
    with open(path_out, "w+") as out:
        out.write("sample" + "\t" + "\t".join(items) + "\n")
        for each_sample in each_sample_info:
            this_sample_values = [each_sample_info[each_sample][each_item] for each_item in items]
            out.write(each_sample + "\t" + "\t".join(this_sample_values) + "\n")


def main():
    if len(sys.argv) != 3:
        print("Usage: python parseRawData_new_3.py http://bigd.big.ac.cn/bioproject/browse/PRJCA000816 new.3.meta.xls")
        exit(-1)
    url = sys.argv[1]
    path_out = sys.argv[2]
    each_sample_info = crawl_page(url)
    write(path_out, each_sample_info)


if __name__ == '__main__':
    main()
