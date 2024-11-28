#!/usr/bin/env Rscript
# args = commandArgs(trailingOnly=TRUE)

a <- data.frame(t1 = 1:5)
# a$t2 <- args[1]
# a$t3 <- args[2]

saveRDS(a,file = "test.rds")