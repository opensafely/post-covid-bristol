## =============================================================================
## MAKE SURVIVAL DATA -- FORMAT FOR TIME-DEPENDENT COXPH
##
## Authors: Samantha Ip, Jenny Cooper
## Thanks to: Thomas Bolton, Venexia Walker and Angela Wood
## =============================================================================

fit_get_data_surv <- function(covars, agegp, event, survival_data, cuts_weeks_since_expo){
  print(paste("working on... ", event))
  
  # sanity check dates ----
  cohort_start_date <- as.Date(cohort_start_date, tryFormats = c("%Y-%m-%d"))
  cohort_end_date <- as.Date(cohort_end_date, tryFormats = c("%Y-%m-%d"))
  if (any(survival_data$DATE_OF_DEATH< cohort_start_date, na.rm=TRUE) | 
      any(survival_data$record_date< cohort_start_date, na.rm=TRUE) | 
      any(survival_data$expo_date< cohort_start_date, na.rm=TRUE) ){
    stop("Bad dates -- < cohort_start_date!")}
  
  if (any(survival_data$DATE_OF_DEATH> cohort_end_date, na.rm=TRUE) | 
      any(survival_data$record_date> cohort_end_date, na.rm=TRUE) | 
      any(survival_data$expo_date> cohort_end_date, na.rm=TRUE) ){
    stop("Bad dates -- > cohort_end_date!")}
  
  
  names(survival_data)[names(survival_data) == 'record_date'] <- 'event_date'

  # filter for age group of interest ----
  survival_data$AGE_AT_COHORT_START <- as.numeric(survival_data$AGE_AT_COHORT_START)
  
  setDT(survival_data)[ , agegroup := cut(AGE_AT_COHORT_START, 
                                          breaks = agebreaks, 
                                          right = FALSE, 
                                          labels = agelabels)]
  print("survival_data done")
  
  if (agegp == "all"){
    survival_data -> cohort_agegp
  } else {
    survival_data %>% filter(agegroup== agegp) -> cohort_agegp
  }
  print(paste0("total num events in cohort_agegp (", agegp, "): ", sum(!is.na(cohort_agegp$event_date))))
  
  #------------------ RANDOM SAMPLE NON-CASES for IP WEIGHING ------------------
  set.seed(137)
  if (!is.na(noncase_frac)){
    cases <- cohort_agegp %>% filter((!is.na(event_date)) & 
                                       (
                                         ((event_date <= DATE_OF_DEATH) | is.na(DATE_OF_DEATH)) 
                                       )) 
    
    non_cases_exposed <- cohort_agegp %>% filter((!patient_id %in% cases$patient_id) & (!is.na(expo_date))) 
    non_cases_unexposed <- cohort_agegp %>% filter((!patient_id %in% cases$patient_id) & (is.na(expo_date))) 
    non_cases_unexposed <- sample_frac(non_cases_unexposed, noncase_frac, replace=F)     

    cohort_agegp <- rbind(cases, non_cases_exposed, non_cases_unexposed)
  }
  
  system.time(cohort_agegp <-  transform(cohort_agegp, end_date = pmin(event_date, DATE_OF_DEATH, cohort_end_date, na.rm=TRUE)))
  cat(paste0("any missing end_dates? ", any(is.na(cohort_agegp$end_date)), "\n"))

  cohort_agegp$days_to_end <- as.numeric(cohort_agegp$end_date-cohort_start_date)
   
  # if allow events on the end date to have the day to happen, since we are including the last day's events
  cohort_agegp$days_to_end <- cohort_agegp$days_to_end +1 
  # head(cohort_agegp %>% dplyr::select(!c("SEX", "AGE_AT_COHORT_START", "region_name", "name")) %>% filter(is.na(DATE_VAC_CENSOR)))
  # head(cohort_agegp %>% dplyr::select(!c("SEX", "AGE_AT_COHORT_START", "region_name", "name")) %>% filter(!is.na(DATE_VAC_CENSOR)))
  # head(cohort_agegp %>% dplyr::select(!c("SEX", "AGE_AT_COHORT_START", "region_name", "name")) %>% filter(DATE_VAC_CENSOR==end_date))
  
  noncase_ids <- unique(non_cases_unexposed$patient_id)
  print("cohort_agegp done")
  head(cohort_agegp )
  #===============================================================================
  #   CACHE some features
  #-------------------------------------------------------------------------------  
  df_sex <- cohort_agegp %>% dplyr::select(patient_id, SEX)
  df_age_region <- cohort_agegp %>% dplyr::select(patient_id, AGE_AT_COHORT_START, region_name) %>% rename(age = AGE_AT_COHORT_START)
  df_age_region$age_sq <- df_age_region$age^2
  
  
  print("df_age_region")
  print(head(df_age_region))
  
  #===============================================================================
  # WITH COVID
  #-------------------------------------------------------------------------------
  cohort_agegp %>% 
    filter(!is.na(expo_date)) -> with_expo
  with_expo %>% 
    dplyr::select(patient_id, expo_date, end_date, event_date, days_to_end, DATE_OF_DEATH) %>%  
    mutate(event_status = if_else( (!is.na(event_date)) 
                                     #  & (
                                     #   ((event_date <= end_date) & ((end_date != DATE_VAC_CENSOR) | is.na(DATE_VAC_CENSOR ))) | 
                                     #     ((event_date < end_date) & (end_date == DATE_VAC_CENSOR)) 
                                     # )
                                     , 1, 0)) -> with_expo
  
  # ......................................
  # Need to add 0.001 when days_to_end==0
  if (length(with_expo$days_to_end[with_expo$days_to_end==0])>0){
    with_expo$days_to_end <- ifelse(with_expo$days_to_end==0, with_expo$days_to_end + 0.001, with_expo$days_to_end) 
  }
  
  
  # ......................................
  # CHUNK UP FOLLOW-UP PERIOD by CHANGE OF STATE OF EXPOSURE
  with_expo$day_expo <- as.numeric(with_expo$expo_date - as.Date(cohort_start_date))
  
  d1 <- with_expo %>% dplyr::select(patient_id, expo_date, event_date, DATE_OF_DEATH)
  d2 <- with_expo %>% dplyr::select(patient_id, day_expo, days_to_end, event_status)
  with_expo <- tmerge(data1=d1, data2=d2, id=patient_id,
                      event=event(days_to_end, event_status),
                      expo=tdc(day_expo)) 
  with_expo <- with_expo %>% dplyr::select(!id)
  
  rm(list=c("d1", "d2", "non_cases_exposed", "non_cases_unexposed", "cases"))
  print("tmerge done")
 
  with_expo_postexpo <- with_expo %>% filter(expo==1)
  # ................... SPLIT POST-COVID TIME...................
  with_expo_postexpo <- with_expo_postexpo %>% rename(t0=tstart, t=tstop) %>% mutate(tstart=0, tstop=t-t0)
  with_expo_postexpo <- survSplit(Surv(tstop, event)~., 
                                  with_expo_postexpo,
                                  cut=cuts_weeks_since_expo*7,
                                  episode="weeks_cat"
  )
  with_expo_postexpo <- with_expo_postexpo %>% mutate(tstart=tstart+t0, tstop=tstop+t0) %>% dplyr::select(-c(t0,t))
  print("survSplit done")
  
  # ................... CONCAT BACK PRE-COVID TIME...................
  with_expo_preexpo <- with_expo %>% filter(expo==0)
  with_expo_preexpo$weeks_cat <- 0
  ls_with_expo <- list(with_expo_preexpo, with_expo_postexpo)
  with_expo <- do.call(rbind, lapply(ls_with_expo, function(x) x[match(names(ls_with_expo[[1]]), names(x))]))
  
  
  rm(list=c("ls_with_expo", "with_expo_preexpo", "with_expo_postexpo"))
  
  with_expo  <- with_expo %>%
    group_by(patient_id) %>% arrange(weeks_cat) %>% mutate(last_step = ifelse(row_number()==n(),1,0))
  with_expo$event  <- with_expo$event * with_expo$last_step
  print("with_expo done")
  #===============================================================================
  #-   WITHOUT COVID
  #-------------------------------------------------------------------------------
  cohort_agegp %>%
    filter(is.na(expo_date)) -> without_expo
  
  without_expo %>% 
    dplyr::select(patient_id, expo_date, end_date, event_date, days_to_end, DATE_OF_DEATH) %>%  
    mutate(event = if_else( (!is.na(event_date)) 
                            # & 
                            #   (
                            #     ((event_date <= end_date) & ((end_date != DATE_VAC_CENSOR) | is.na(DATE_VAC_CENSOR ))) | 
                            #       ((event_date < end_date) & (end_date == DATE_VAC_CENSOR)) 
                            #   )
                            , 
                            1, 0)) -> without_expo
  
  
  # ......................................
  without_expo$tstart<- c(0)
  without_expo$tstop <- ifelse(without_expo$days_to_end ==0,  without_expo$days_to_end + 0.001, without_expo$days_to_end)
  without_expo$expo<- c(0)
  without_expo$weeks_cat <- c(0)
  print("without_expo done")
  #===============================================================================
  #-   RBIND WITH & WITHOUT COVID
  #-------------------------------------------------------------------------------
  common_cols <- intersect(colnames(without_expo), colnames(with_expo))
  without_expo <- without_expo %>% dplyr::select(all_of(common_cols))
  with_expo <- with_expo %>% dplyr::select(all_of(common_cols))
  data_surv <-rbind(without_expo, with_expo)
  
  rm(list=c("with_expo", "without_expo"))
  gc()
  
  print("data_surv done")
  print(paste0("total num events in data_surv: ", sum(data_surv$event==1)))
  
  
  #===============================================================================
  #   PIVOT WIDE for WEEKS_SINCE_COVID
  #-------------------------------------------------------------------------------
  data_surv$days_to_expo <- as.numeric(data_surv$expo_date - as.Date(cohort_start_date)  ) 
  
  interval_names <- mapply(function(x, y) ifelse(x == y, paste0("week", x), paste0("week", x, "_", y)), 
                           lag(cuts_weeks_since_expo, default = 0)+1, 
                           cuts_weeks_since_expo, 
                           SIMPLIFY = FALSE)
  cat("...... interval_names...... \n")
  print(interval_names)
  intervals <- mapply(c, lag(cuts_weeks_since_expo, default = 0)+1, cuts_weeks_since_expo, SIMPLIFY = F)
  
  
  i<-0
  for (ls in mapply(list, interval_names, intervals, SIMPLIFY = F)){
    i <- i+1
    print(paste(c(ls, i), collapse="..."))
    data_surv[[ls[[1]]]] <- if_else(data_surv$weeks_cat==i, 1, 0)
  }
  
  print("pivot wide done... examine data_surv for someone with exposure:")
  data_surv %>% filter(tstart>0) %>% arrange(patient_id)%>% head(10) %>% print(n = Inf)
  data_surv %>% filter(expo_date==event_date) %>% arrange(patient_id)%>% head(10) %>% print(n = Inf)
  data_surv <- data_surv %>% left_join(df_sex)
  
  
  # ============================= EVENTS COUNT =================================
  which_week_since_covid <- function(row_data_surv, interval_names){
    week_cols <- row_data_surv %>% dplyr::select(all_of(interval_names))
    row_data_surv$expo_week <- names(week_cols)[which(week_cols == 1)]
    row_data_surv$expo_week <- ifelse(is.na(row_data_surv$expo_week),"pre expo", row_data_surv$expo_week)
    return(row_data_surv)
  }
  
  get_tbl_event_count <- function(data_surv, interval_names){
    df_events <- data_surv %>% filter(event==1)
    ls_data_surv <- split(df_events, 1:nrow(df_events))
    ls_data_surv <- lapply(ls_data_surv, which_week_since_covid, unlist(interval_names))
    ls_data_surv <- do.call("rbind", ls_data_surv)
    tbl_event_count <- aggregate(event ~ expo_week, ls_data_surv, sum)
    tbl_event_count[nrow(tbl_event_count) + 1,] = c("all post expo", sum(tail(tbl_event_count$event, -1))  )
    return(tbl_event_count)
  }
  tbl_event_count_all <- get_tbl_event_count(data_surv, interval_names)
  tbl_event_count_sex1 <- get_tbl_event_count(data_surv %>% filter(SEX=='M'), interval_names)
  tbl_event_count_sex2 <- get_tbl_event_count(data_surv %>% filter(SEX=='F'), interval_names)
  
  tbl_event_count <- list(tbl_event_count_all, tbl_event_count_sex1, tbl_event_count_sex2) %>% reduce(left_join, by = "expo_week")
  
  event_count_levels <- c("pre expo", unlist(interval_names), "all post expo")
  tbl_event_count_levels <- data.frame(event_count_levels)
  names(tbl_event_count_levels) <- c("expo_week")
  

  tbl_event_count <- merge(tbl_event_count_levels, tbl_event_count, all.x = TRUE)
  tbl_event_count[is.na(tbl_event_count)] <- 0
  
  tbl_event_count <- tbl_event_count %>%
    arrange(factor(expo_week, 
                   levels = event_count_levels), 
            expo_week)
  
  names(tbl_event_count) <- c("expo_week", "events_total", "events_M", "events_F")
  
  ind_any_zeroeventperiod <- any((tbl_event_count$events_total == 0) & (!identical(cuts_weeks_since_expo, c(4, 49))))
  
#  if (identical(cuts_weeks_since_expo, c(4, 49))){
#    write.csv(tbl_event_count, paste0(res_dir,"/tbl_event_count_red_" , expo, "_", event, "_", ".csv"), row.names = T)
#  } else (
#    write.csv(tbl_event_count, paste0(res_dir,"/tbl_event_count_" , expo, "_", event, "_", ".csv"), row.names = T)
#  )

  if (identical(cuts_weeks_since_expo, c(4, 49))){
    write.csv(tbl_event_count, paste0(res_dir,"/tbl_event_count_", mdl, "_", expo, "_", event, "_", agegp, ".csv"), row.names = T)
  } else (
    write.csv(tbl_event_count, paste0(res_dir,"/tbl_event_count_", mdl, "_", expo, "_", event, "_", agegp, ".csv"), row.names = T)
  )  
   
  
  #===============================================================================
  # FINALIZE age, region, data_surv
  #-------------------------------------------------------------------------------
  data_surv <- data_surv %>% left_join(df_age_region)
  print("...... finished get_data_surv ......!")
  
  return(list(data_surv, noncase_ids, interval_names, ind_any_zeroeventperiod))
}
