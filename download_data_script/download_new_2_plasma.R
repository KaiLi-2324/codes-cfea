raw_data <- read.table("new.2.meta.xls", sep = "\t", header = T)
urls <- as.vector(raw_data$CRR)
path <- "F:\\DataDownLoadCfDNADataBase\\new_2_plasma"

for(each_url in urls){
    cat("Start parsing ", each_url, "\n")
    for(this_url in unlist(strsplit(each_url, split = ";"))){
        shell_cmd <- paste0("IDMan.exe", " /d ", this_url, " /n ", "/a ", "/p ", path)
        shell(shell_cmd)
    }
}

shell("IDMan.exe /s")
