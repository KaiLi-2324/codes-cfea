import re
import sys
import time
import urllib.request as ur
from collections import defaultdict


def crawl_page(path):
    print(f"Start crawling {path}")
    sample_items = defaultdict(dict)
    pattern_srx = re.compile(r'<dl class=\"rprtid\"><dt>Accession: </dt> <dd>(SRX\d+)</dd></dl>')
    response = ur.urlopen(path)
    html = response.read().decode()
    total_srx = pattern_srx.findall(html)
    for each_srx in total_srx:
        try:
            print(f"Start crawling {each_srx}")
            sra_url = f"https://www.ncbi.nlm.nih.gov/sra/?term={each_srx}"
            sra_response = ur.urlopen(sra_url)
            sra_html = sra_response.read().decode()
            library_strategy = re.findall(r"<div>Strategy: <span>(.*?)</span>", sra_html)
            layout = re.findall(r"<div>Layout: <span>(.*?)</span></div>", sra_html)
            srr = re.findall(r'<a href=\"//trace.ncbi.nlm.nih.gov/Traces/sra/\?run=(SRR\d+)\">', sra_html)
            if len(srr) >= 2:
                raise ValueError("Invalid SRR numbers!")
            this_srr_out = "{}.sra".format(srr[0])
            srr_url = "https://ftp.ncbi.nih.gov/sra/sra-instant/reads/ByRun/sra/SRR/{}/{}/{}".format(
                srr[0][:6], srr[0], this_srr_out
            )
            sample_items[each_srx]["library_strategy"] = library_strategy[0]
            sample_items[each_srx]["layout"] = layout[0]
            sample_items[each_srx]["sra_url"] = srr_url
            time.sleep(1)
        except Exception as e:
            print(e)
    return sample_items


def write(sample_items, path_out):
    print(f"Start writing to {path_out}")
    with open(path_out, "w+") as out:
        out.write("sample\tlibrary_strategy\tlayout\tsra_url\n")
        for each_sample in sample_items:
            this_sample_values = [sample_items[each_sample][each_item] for each_item in ["library_strategy",
                                                                                         "layout", "sra_url"]]
            print(this_sample_values)
            out.write(each_sample + "\t" + "\t".join(this_sample_values) + "\n")


def main():
    path = sys.argv[1]
    sample_items = crawl_page(path)
    write(sample_items, sys.argv[2])


if __name__ == '__main__':
    main()
