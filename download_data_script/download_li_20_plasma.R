library(readxl)


raw_data <- read_excel("cfDNA_sampls_meta.xlsx")
raw_data_rrbs <- raw_data[raw_data$PMID == 28263317,]
raw_data_rrbs_plasma <- raw_data_rrbs[raw_data_rrbs$sample_characteristics == "plasma",]
urls <- raw_data_rrbs_plasma$raw_data

path <- "F:\\DataDownLoadCfDNADataBase\\liquid_20_plasma"

for(each_url in urls){
    each_url_split <- unlist(strsplit(each_url, split = ","))
    if(length(each_url_split) >= 2){
        cat("\tThis url contains", length(each_url_split), "urls\n")
    }
    for(this_url in each_url_split){
        cat("Start parsing ", this_url, "\n")
        shell_cmd <- paste0("IDMan.exe", " /d ", this_url, " /n ", "/a ", "/p ", path)
        shell(shell_cmd)
    }
}

shell("IDMan.exe /s")

