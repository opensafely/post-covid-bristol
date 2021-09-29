# Specify arguments ------------------------------------------------------------
# Age groups can be specified as 'all' or age breaks seperated by underscores (e.g., age_grps = '40_60_80')

args = commandArgs(trailingOnly=TRUE)
age_grps = args[[1]]

# Load libraries ---------------------------------------------------------------

library(magrittr)

# Load data --------------------------------------------------------------------

df <- data.table::fread("output/input.csv", data.table = FALSE)  

# Implement age groupings ------------------------------------------------------

if (age_grps=="all") {
  
  df$age_grp <- paste0(min(df$cov_age),"-",max(df$cov_age))
  
} else {
  
  age_grps_numeric <- as.numeric(unlist(strsplit(age_grps,"_")))
  
  df$age_grp <- NA
  
  if (length(age_grps_numeric)>=2) {
    for (i in 2:(length(age_grps_numeric))) {
      df$age_grp <- ifelse(age_grps_numeric[i-1]<=df$cov_age & df$cov_age<age_grps_numeric[i], paste0(age_grps_numeric[i-1],"-",age_grps_numeric[i]-1), df$age_grp)
    }
  }
  
  df$age_grp <- ifelse(df$cov_age<age_grps_numeric[1], paste0(min(df$cov_age),"-",age_grps_numeric[1]-1), df$age_grp)
  df$age_grp <- ifelse(df$cov_age>=age_grps_numeric[length(age_grps_numeric)], paste0(age_grps_numeric[length(age_grps_numeric)],"-",max(df$cov_age)), df$age_grp)
  
}

# Identify exposures, outcomes and covariates ----------------------------------

exposures <-  colnames(df)[grepl("exp_",colnames(df))]

outcomes <- colnames(df)[grepl("out_",colnames(df))]

covariates <- colnames(df)[grepl("cov_",colnames(df))]

# Restrict dataset -------------------------------------------------------------

df <- df[,c("patient_id","age_grp",exposures,outcomes,covariates)]

# Remove variables with more than 11 categories --------------------------------
# Note: 11 because it allows 10 categories plus missing (e.g., IMD) ------------

if  (length(covariates)>0) {
  for (i in 1:length(covariates)) {
    
    tmp <- length(unique(df[,covariates[i]]))
    
    if (tmp>11) {
      df[,covariates[i]] <- NULL
    }
    
  }
}

# Convert exposures and outcomes to indicators ---------------------------------

if (length(exposures)>0) {
  for (i in 1:length(exposures)) {
    df[,exposures[i]] <- as.numeric(!is.na(df[,exposures[i]]))
  }
}

if (length(outcomes)>0) {
  for (i in 1:length(outcomes)) {
    df[,outcomes[i]] <- as.numeric(!is.na(df[,outcomes[i]]))
  }
}

# Aggregated table -------------------------------------------------------------

output <- aggregate(df$patient_id, by = df[,c(setdiff(colnames(df),c("patient_id")))], FUN = length)
output <- dplyr::rename(output, "N" = "x")

# Save output ------------------------------------------------------------------

data.table::fwrite(output,paste0("output/covariate_check_ages_",age_grps,".csv"))
