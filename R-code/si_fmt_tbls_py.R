## =============================================================================
## READS IN & FORMATS DATABRICKS RESULTS 
##
## Author: Samantha Ip
## =============================================================================

library(data.table)
library(dplyr)
library(DBI)
library(R.utils)
library(purrr)
#===============================================================================
# Read in PY incidence rates & event counts
#...............................................................................
con <- dbConnect(odbc::odbc(), "Databricks", timeout=60, PWD=rstudioapi::askForPassword("enter databricks personal access token:"))
rm(list=setdiff(ls(), c("con")))

setwd("/mnt/efs/hyi20/dvt_icvt_results/2021-07-20_infection/")
gc()


ls_events <- c("AMI", "PE")
# readRDS("/mnt/efs/hyi20/dvt_icvt_results/ls_events.rds")
print(ls_events)

# ..............................................................................
date_extension <- "_0721"

outcome_vac_combos <- expand.grid(ls_events, c("hospitalised", "non_hospitalised"))
names(outcome_vac_combos) <- c("outcome", "vac")

ls_ir_counts <- map2(outcome_vac_combos$outcome, outcome_vac_combos$vac, function(event, vac) dbGetQuery(
  con, paste0('SELECT * FROM dars_nic_391419_j3w9t_collab.ccu002_01_ircounts_', tolower(event), "_", vac, date_extension)))



interval_names <- mapply(function(x, y) ifelse(x == y, paste0("week", x), paste0("week", x, "_", y)), 
                         lag(cuts_weeks_since_expo, default = 0)+1, 
                         cuts_weeks_since_expo, 
                         SIMPLIFY = FALSE)
df <- rbindlist(ls_ir_counts)
df <- arrange(df, outcome, agegroup, factor(period, levels = c("unexposed", unlist(interval_names))))

get_IRratio_wrt_unexposed <- function(df){
  df$ratio <- df$IR_py_sexall/(df[which(df$period=="unexposed"),]$IR_py_sexall)
  return(df)
}

ls_df <- lapply(split(df, list(df$vac, df$agegroup, df$outcome), drop = TRUE), get_IRratio_wrt_unexposed)
df <- rbindlist(ls_df)



col_order <- c("outcome", "vac", "agegroup", "period", "events_sexall", "n_days_sexall", "IR_py_sexall", "ratio")
df <- df %>% dplyr::select(col_order)
# df <- df %>% relocate(col_order)
df[, c("IR_py_sexall", "ratio")] <-round(df[, c("IR_py_sexall", "ratio")], 3)

names(df) <- c(
  "Outcome",
  "Vaccine",
  "Age group",
  "Period w.r.t. expo",
  "N events (Any sex)",
  "N years (Any sex)",
  "IR per 100,000 person-yrs (Any sex)",
  "IR_period:IR_unexposed"
)
df %>% View()
write.csv(df, file = paste0("ircounts_vac.csv"), row.names=F)
