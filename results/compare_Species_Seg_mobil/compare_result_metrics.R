library(tidyverse)
# Install and load the package
library("ggsci")

cbPalette <- c("#999999", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7")

wf = windowsFonts()

names(wf[wf=="TT Times New Roman"])

lowercase_second_word <- function(x) {
  s <- strsplit(x, " ")[[1]]
  s[2] <- tolower(s[2])
  return(paste(s, collapse = " "))
}

df_metrics_base_n <- read.table("metrics_yolo_n_base_conf_standard.txt", header = T)
  

df_metrics_weighted_aug_n <- read.table("metrics_yolo_n_weighted_sampler_augment_conf_standard.txt", header = T)

df_metrics_weighted_n <- read.table("metrics_yolo_n_weighted_sampler_conf_standard.txt", header = T)

# combine data
data <- df_metrics_base_n %>% 
  merge(., df_metrics_weighted_n, by=c("species", "class_index")) %>% 
  merge(., df_metrics_weighted_aug_n, by=c("species", "class_index"))

data_plot <- data %>% 
  select(species, map_50_95_mask_n_base, map_50_95_mask_n_weighted, map_50_95_mask_n_weighted_augment) %>% 
  mutate(species = replace(species, str_detect(species, "all"), "aall")) %>%
  arrange(species) %>%
  mutate(species = replace(species, str_detect(species, "aall"), "all")) %>% 
  mutate(species = str_replace_all(species, "_", " ")) %>%
  mutate(species = str_to_title(species))

# Apply the function to your column
data_plot$species <- sapply(data_plot$species, lowercase_second_word)
data_plot$species[1] <- "All"

write.table(data_plot, "combined_metrics.txt", sep = "\t", row.names = FALSE, quote=FALSE)


# compare model MAP 50 95 mask between models:
data_plot %>%
  rename("BM" = map_50_95_mask_n_base,
         "WSM" = map_50_95_mask_n_weighted,
         "WSAM" = map_50_95_mask_n_weighted_augment) %>% 
  pivot_longer(!species, names_to = "Model", values_to = "map_05_095") %>% 
  ggplot(., aes(x=fct_inorder(species), y = map_05_095, fill = Model)) + 
  geom_bar(stat='identity', position = position_dodge()) +
  scale_fill_manual(values = cbPalette[2:6]) +
  coord_cartesian(ylim = c(0, 1)) +
  scale_x_discrete("Species") + 
  scale_y_continuous("MAP (50-95)", breaks = seq(0, 1, by = 0.2)) +
  # ggtitle("Comparison of MAP (50-95) for masks between YOLO models") +
  theme_bw() +
  theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust=1)) +
  theme(legend.position="top") +
  theme(legend.position="top",
        legend.margin=margin(b = -7),  # Adjust this value to suit your needs
        text= element_text(family = "serif", size=12),
        plot.margin = margin(0.1, 0.1, 0.1, 0.1, "cm"))

ggsave("comparison_map_05_095.pdf", width = 5.9, height = 5.9/1.5)

data_filtered <- data %>% 
  select(c(species, map_50_95_mask_n_base, map_50_95_mask_n_weighted, 
           map_50_95_mask_n_weighted_augment)) %>% 
  filter(species == 'all') %>% 
  pivot_longer(!species, names_to = "model", values_to = "MAP_05_095")

write.table(data_filtered, 
            "combined_metrics_map_all.txt", 
            sep = "\t", row.names = FALSE, quote=FALSE)
