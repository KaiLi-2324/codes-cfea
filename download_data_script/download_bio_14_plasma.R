library(readxl)


raw_data <- as.data.frame(read_excel("cfDNA_sampls_meta.xlsx"))
raw_data_hme <- raw_data[raw_data$PMID == 28820176,]
raw_data_hme_plasma <- raw_data_hme[raw_data_hme$sample_characteristics == "plasma",]
urls <- raw_data_hme_plasma$raw_data

path <- "F:\\DataDownLoadCfDNADataBase\\bioproject_14_plasma"

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
