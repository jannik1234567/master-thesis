library(tidyverse)

lowercase_second_word <- function(x) {
  s <- strsplit(x, " ")[[1]]
  s[2] <- tolower(s[2])
  return(paste(s, collapse = " "))
}

classes_overview <- read.table("classes.txt",
                               header = F, sep = " ") %>%
  select(V1, V2) %>% 
  mutate(V1 = gsub(":", "", V1)) %>% 
  rename(class = V1,
         class_name = V2) 

# tabel for instances

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
  mutate(sum_count = count_train + count_valid + count_test) %>% 
  arrange(., desc(sum_count)) %>% 
  mutate(class_name = str_replace_all(class_name, "_", " ")) %>%
  mutate(class_name = str_to_title(class_name))

# Apply the function to your column
all_data$class_name <- sapply(all_data$class_name, lowercase_second_word)

write.table(all_data, "combined_overview.txt", quote = FALSE, sep = "\t", row.names = FALSE)


# make table for images
overview_test <- read.table("img_overview_test.txt",
                            header = T, sep = ",") %>% 
  rename(count_test = count)

overview_train <- read.table("img_overview_train.txt",
                             header = T, sep = ",") %>% 
  rename(count_train = count)

overview_valid <- read.table("img_overview_valid.txt",
                             header = T, sep = ",") %>% 
  rename(count_valid = count)



all_data <- merge(classes_overview, overview_train, by = "class") %>% 
  merge(., overview_valid, by = "class") %>% 
  merge(., overview_test, by = "class") %>%
  mutate(sum_count = count_train + count_valid + count_test) %>% 
  arrange(., desc(sum_count)) %>% 
  mutate(class_name = str_replace_all(class_name, "_", " ")) %>%
  mutate(class_name = str_to_title(class_name))

composition_data <- all_data %>% 
  select(c(class, class_name)) %>% 
  rename(ID = class,
         'Species' = class_name)


composition_data_numbers <- read.table("img_and_trees_per_species.txt",
                            header = T, sep = "\t") %>% 
  rename('Species' = species)

composition_data_merge <- merge(composition_data, 
                                composition_data_numbers, 
                                by="Species", all = TRUE) %>%
  rename("Number of trees" = num_trees,
         "Number of images" = num_img_total) %>% 
  select(c(ID, Species, "Number of trees", "Number of images"))

composition_data_merge$Species <- sapply(composition_data_merge$Species, lowercase_second_word)

total <- data.frame(ID = "Total", "Species" = "-", 
                    "Number of trees" = sum(composition_data_merge$`Number of trees`),
                    "Number of images" = sum(composition_data_merge$`Number of images`)) %>% 
  rename("Number of trees" = Number.of.trees,
         "Number of images" = Number.of.images)

composition_data_merge <- rbind(composition_data_merge, total)

write.table(composition_data_merge, "composition_data.txt", quote = FALSE, sep = "\t", row.names = FALSE)

  
