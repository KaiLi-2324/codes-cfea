library(readxl)


raw_data <- read_excel("cfDNA_sampls_meta.xlsx")
raw_data_5hmc <- raw_data[raw_data$PMID == 28925386,]
raw_data_5hmc_plasma <- raw_data_5hmc[raw_data_5hmc$sample_characteristics == "plasma",]
urls <- raw_data_5hmc_plasma$raw_data

path <- "F:\\DataDownloadcfDNADatabase\\bioproject.13_28925386_plasma"

for(each_url in urls){
    cat("Start parsing ", each_url, "\n")
    shell_cmd <- paste0("IDMan.exe", " /d ", each_url, " /n ", "/a ", "/p ", path)
    shell(shell_cmd)
}

shell("IDMan.exe /s")
