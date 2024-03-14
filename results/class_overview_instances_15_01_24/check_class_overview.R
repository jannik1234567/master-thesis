library(tidyverse)

classes_overview <- read.table("classes.txt",
                               header = F, sep = " ") %>%
  select(V1, V2) %>% 
  mutate(V1 = gsub(":", "", V1)) %>% 
  rename(class = V1,
         class_name = V2) 


overview_test <- read.table("cls_overview_test.txt",
                            header = T, sep = ",") %>% 
  rename(count_test = count)

overview_train <- read.table("cls_overview_train.txt",
                             header = T, sep = ",") %>% 
  rename(count_train = count)

overview_valid <- read.table("cls_overview_valid.txt",
                             header = T, sep = ",") %>% 
  rename(count_valid = count)



all_data <- merge(classes_overview, overview_train, by = "class") %>% 
  merge(., overview_valid, by = "class") %>% 
  merge(., overview_test, by = "class") %>%
  mutate(sum_count = count_train + count_valid + count_test)

write.table(all_data, "combined_overview.txt", quote = FALSE, sep = "\t", row.names = FALSE)  
