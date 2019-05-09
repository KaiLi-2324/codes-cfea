library(readxl)


raw_data <- read_excel("cfDNA_sampls_meta.xlsx")
raw_data_mctaseq <- raw_data[raw_data$method == "MCTA-Seq",]
raw_data_mctaseq_plasma <- raw_data_mctaseq[raw_data_mctaseq$sample_characteristics == "plasma",]
urls <- raw_data_mctaseq_plasma$raw_data

for(each_url in urls){
    cat("Start downloading ", each_url, "\n")
    shell_cmd <- paste0("IDMan.exe", " /d ", each_url, " /n ", " /a")
    shell(shell_cmd)
}

shell("IDMan.exe /s")
