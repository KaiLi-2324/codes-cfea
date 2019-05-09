f = open("test.fasta", "r")
former_chr = ""
former_line = ""
chr_len = dict()
for line in f:
    if line.startswith(">"):
        line_list = line.split()
        chromosome = line_list[0].lstrip(">")
        if former_chr:
            print("Start parsing {}".format(former_chr))
            chr_len[former_chr] = len(former_line)
            former_line = ""
        former_chr = chromosome
    else:
        former_line += line.strip()
chr_len[former_chr] = len(former_line)

out = open("test.txt", "w")
for each_chr in chr_len:
    out.write(each_chr + "\t" + str(chr_len[each_chr]) + "\n")

f.close()
out.close()
