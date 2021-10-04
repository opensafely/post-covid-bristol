# Specify command arguments ----------------------------------------------------

args = commandArgs(trailingOnly=TRUE)
mdl  = args[[1]] # "mdl1_unadj"
event  = args[[2]] # "AMI"
agegp  = args[[3]] # "all"

# Load libraries ---------------------------------------------------------------

library(data.table)
library(dplyr)
library(survival)
#library(table1)
library(broom)
library(DBI)
library(ggplot2)
library(nlme)
library(tidyverse)
# library(R.utils)
library(lubridate)
library(purrr)
library(parallel)
# library(multcomp)

# Specify directories (legacy from NHSD TRE) -----------------------------------

res_dir_proj <- "output"
scripts_dir <- "analysis"
res_dir <- res_dir_proj

# Source relavant files --------------------------------------------------------

source(file.path(scripts_dir,"si_02_pipe.R")) # Prepare dataset for model
source(file.path(scripts_dir,paste0("si_call_",mdl,".R"))) # Model specification

# Run model of interest --------------------------------------------------------

get_vacc_res(sex_as_interaction=FALSE,
             event=event,
             agegp=agegp,
             cohort_vac, covars)