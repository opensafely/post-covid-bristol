## =============================================================================
## Pipeline (2): Reads in analysis-specific data, loads parameters, 
## gets vaccine-specific dataset -- censoring at appropriate dates
##
## Author: Samantha Ip
## =============================================================================
# specify events of interest
#ls_events <- c("AMI")
#("fracture",unstable_angina","stroke_SAH_HS",)
# Doesn't run: "TTP","DIC","ICVT_event","HF","portal_vein_thrombosis","cardiomyopathy"
#All outcomes: "artery_dissect","angina","other_DVT","fracture","thrombocytopenia","life_arrhythmia","pericarditis","TTP","mesenteric_thrombus","DIC","myocarditis","stroke_TIA","stroke_isch","other_arterial_embolism","unstable_angina","PE","AMI","HF","portal_vein_thrombosis","cardiomyopathy","stroke_SAH_HS","Arterial_event","Venous_event","Haematological_event""DVT_event","ICVT_event"

#"angina","other_DVT","fracture","thrombocytopenia","life_arrhythmia","pericarditis","TTP","mesenteric_thrombus","DIC","myocarditis","stroke_TIA","stroke_isch","other_arterial_embolism","unstable_angina","PE","AMI","HF","portal_vein_thrombosis","cardiomyopathy","stroke_SAH_HS","Arterial_event","Venous_event","Haematological_event","DVT_event","ICVT_event")
# specify path to data
master_df_fpath <- "output/input.csv"

# specify study parameters
agebreaks <- c(0, 40, 60, 80, 500)
agelabels <- c("under_40", "40-59", "60-79", "over_80")
noncase_frac <- 0.1


cohort_start_date <- as.Date("2020-01-01")
cohort_end_date <- as.Date("2020-12-07")

cuts_weeks_since_expo <- c(1, 2, 4, 8, 12, 26, as.numeric(ceiling(difftime(cohort_end_date,cohort_start_date)/7))) 
cuts_weeks_since_expo_reduced <- c(4, as.numeric(ceiling(difftime(cohort_end_date,cohort_start_date)/7))) 


expo <- "infection"

# inspect column names of dataset
master_names <- fread(master_df_fpath, nrows=1)
sort(names(master_names))


# ---------------------- READ IN DATA ------------------------------------------
# read in core analysis information -- for not fully-adjusted analyses (e.g. "mdl1_unadj", "mdl2_agesex") and exploration (save memory)
cohort_vac_cols <- c("patient_id", 
                     "cov_sex", 
                     "death_date", 
                     "cov_age", 
                     "exp_confirmed_covid19_date", 
                     "cov_region")

cohort_vac <- fread(master_df_fpath, 
                    select=cohort_vac_cols)

cohort_vac <- dplyr::rename(cohort_vac,
                            DATE_OF_DEATH = death_date,
                            SEX = cov_sex,
                            AGE_AT_COHORT_START = cov_age, 
                            EXPO_DATE = exp_confirmed_covid19_date, 
                            region_name = cov_region)

cohort_vac$DATE_OF_DEATH=na_if(cohort_vac$DATE_OF_DEATH,"")
cohort_vac$DATE_OF_DEATH=as.Date(cohort_vac$DATE_OF_DEATH)
cohort_vac$EXPO_DATE=na_if(cohort_vac$EXPO_DATE,"")
cohort_vac$EXPO_DATE=as.Date(cohort_vac$EXPO_DATE)


print(head(cohort_vac))
gc()


if (! mdl %in% c("mdl1_unadj", "mdl2_agesex")){
  covar_names <- master_names %>% dplyr::select(c(names(master_names)[grepl("cov_", names(master_names))],"patient_id")) %>% names()
  covar_names=covar_names[! covar_names %in% c('cov_sex','cov_age','cov_region')]
  covars <- fread(master_df_fpath, select = covar_names)
  gc()
  source(file.path(scripts_dir, "si_prep_covariates.R")) # wrangles covariates to the correct data types, deal with NAs and missing values, set reference levels
} else {
  covars <- cohort_vac %>% dplyr::select(patient_id)
}



#------------------------ SET DATES OUTSIDE RANGE AS NA ------------------------
set_dates_outofrange_na <- function(df, colname)
{
  df <- df %>% mutate(
    !!sym(colname) := as.Date(ifelse((!!sym(colname) > cohort_end_date) | (!!sym(colname) < cohort_start_date), NA, !!sym(colname) ), origin='1970-01-01')
  )
  return(df)
}


#------------------------ RM GLOBAL OBJ FROM WITHIN FN -------------------------
rm_from_within_fn <- function(obj_name) {
  objs <- ls(pos = ".GlobalEnv")
  rm(list = objs[grep(obj_name, objs)], pos = ".GlobalEnv")
  gc()
}



