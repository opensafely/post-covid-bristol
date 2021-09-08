event <- "AMI"
sex_num <- "all"

hrs_vac <- fread("hrs_vac_AMI.csv")
hrs_vac$agegp <- factor(hrs_vac$agegp, levels=agelabels)
hrs_vac$term <- factor(hrs_vac$term, 
                       levels=unlist(interval_names))


hrs_vac <-hrs_vac %>%
  filter(grepl("week", term)) %>% filter(sex==sex_num)


ggplot(hrs_vac, aes(x=term, y=estimate, group = agegp, color=agegp)) + 
  geom_line() +
  geom_errorbar(aes(ymin=conf.low, ymax=conf.high), width=.2, col="grey",
                position=position_dodge(0.05))+
  geom_point(aes(shape=agegp))+
  theme(axis.text.x = element_text (angle = -50)) +
  labs(x = "Weeks since COVID", y = "Hazard ratio for CVD Event", 
       title = paste0("Hazard Ratios for ", event, " (sex: ", sex_num, ")")) +
  geom_hline(yintercept=1, lwd=0.5, col="red4", linetype = "dashed") 

ggsave(paste0("plt_hrs_INFECTION_", event, "_sex_", sex_num, ".png"))
