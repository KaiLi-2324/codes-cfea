library(readxl)


raw_data <- read_excel("cfDNA_samples_meta_plasma.xlsx")
raw_data_sepsis <- raw_data[raw_data$PMID == 30498206,]
raw_data_sepsis_plasma <- raw_data_sepsis[raw_data_sepsis$sample_characteristics == "plasma",]
urls <- raw_data_sepsis_plasma$raw_data

path <- "F:\\DataDownLoadCfDNADataBase\\new_1_plasma"

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
