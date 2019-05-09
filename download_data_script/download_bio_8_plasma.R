library(readxl)


raw_data <- read_excel("cfDNA_sampls_meta.xlsx")
raw_data_bio_8 <- raw_data[raw_data$PMID == 29615462,]
urls <- raw_data_bio_8$raw_data
total_urls <- c()

for(each_url in urls){
    cat("Start seperating ", each_url, "\n")
    each_url_sep <- unlist(strsplit(each_url, split = ","))
    for(each_sep in each_url_sep){
        total_urls <- c(total_urls, each_sep)
    }
}

for(each_url in total_urls){
    cat("Start downloading ", each_url, "\n")
    shell_cmd <- paste0("IDMan.exe", " /d ", each_url, " /n ", " /a")
    shell(shell_cmd)
}

shell("IDMan.exe /s")
