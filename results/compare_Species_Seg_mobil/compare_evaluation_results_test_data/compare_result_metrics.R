library(tidyverse)
library(latex2exp)
# Install and load the package

cbPalette <- c("#999999", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7")

lowercase_second_word <- function(x) {
  s <- strsplit(x, " ")[[1]]
  s[2] <- tolower(s[2])
  return(paste(s, collapse = " "))
}

df_metrics_base_n <- read.table("plots_and_tables/metrics_yolo_n_base_conf_standard.txt", header = T)
  
df_my_model <- read.table("plots_and_tables/metrics_yolo_n_weighted_sampler_augment_conf_standard.txt", header = T)
# combine data
data <- df_metrics_base_n %>% 
  merge(., df_my_model, by=c("species", "class_index")) %>% 
  select(class_index, species, f1_mask_n_base, f1_mask_n_weighted_augment,
         map_50_95_mask_n_base, map_50_95_mask_n_weighted_augment) %>% 
  mutate(species = replace(species, str_detect(species, "all"), "aall")) %>%
  arrange(species) %>%
  mutate(species = replace(species, str_detect(species, "aall"), "all")) %>% 
  mutate(species = str_replace_all(species, "_", " ")) %>%
  mutate(species = str_to_title(species))

# Apply the function to your column
data$species <- sapply(data$species, lowercase_second_word)
data$species[1] <- "All"


data_plot <- data %>% 
  select(species, map_50_95_mask_n_base,  map_50_95_mask_n_weighted_augment) 
  

write.table(data_plot, "combined_metrics.txt", sep = "\t", row.names = FALSE, quote=FALSE)


# compare model MAP 50 95 mask between models:
data_plot %>%
  rename("YOLOv8n-seg" = map_50_95_mask_n_base,
         "SpeciesSeg-mobil" = map_50_95_mask_n_weighted_augment) %>% 
  pivot_longer(!species, names_to = "Model", values_to = "map_05_095") %>% 
  ggplot(., aes(x=fct_inorder(species), y = map_05_095, fill = Model)) + 
  geom_bar(stat='identity', position = position_dodge()) +
  scale_fill_manual(values = cbPalette[2:6]) +
  coord_cartesian(ylim = c(0, 1)) +
  scale_x_discrete("Tree species") + 
  scale_y_continuous(TeX("Segment mAP $_{@0.5-0.95}$"), breaks = seq(0, 1, by = 0.2)) +
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
