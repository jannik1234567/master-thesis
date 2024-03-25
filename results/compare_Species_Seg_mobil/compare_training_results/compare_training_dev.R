library(tidyverse)
library(latex2exp)

cbPalette <- c("#999999", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7")

df_base_n <- read.table("results_yolo_base_n.csv", header = T, sep = ",") %>% 
  select(epoch, 'metrics.mAP50.95.M.') %>% 
  rename("YOLOv8n-seg" = 'metrics.mAP50.95.M.')
df_my_model <- read.table("results_weighted_sampler_fine_tuned.csv", header = T, sep=',') %>% 
  select(epoch, 'metrics.mAP50.95.M.') %>% 
  rename("SpeciesSeg-mobil" = 'metrics.mAP50.95.M.')

df_plot <- df_base_n %>% 
  merge(., df_my_model, by="epoch") %>% 
  pivot_longer(!epoch, names_to = "Model", values_to = "mAP")


max_base_model <- df_base_n[df_base_n$`YOLOv8n-seg` == max(df_base_n$`YOLOv8n-seg`),]
max_my_model <- df_my_model[df_my_model$`SpeciesSeg-mobil` == max(df_my_model$`SpeciesSeg-mobil`),]


ggplot(data = df_plot, aes(x=epoch, y=mAP, color=Model)) +
  geom_line(linewidth=1.2) +
  scale_x_continuous("Epoch", breaks = seq(0,300, 50)) +
  scale_y_continuous(TeX("Segment mAP $_{@0.5-0.95}$"), breaks = seq(0, 1, by = 0.2)) +
  scale_color_manual(values = cbPalette[2:6]) +
  annotate("point", x = max_base_model$epoch, 
           y = max_base_model$`YOLOv8n-seg`,
           colour = "red") +
  annotate("text", x = max_base_model$epoch, 
           y = max_base_model$`YOLOv8n-seg`, label = "maximum mAP \n YOLOv8n-seg", colour = "black", vjust = 1.1) +
annotate("point", x = max_my_model$epoch, 
         y = max_my_model$`SpeciesSeg-mobil`,
         colour = "red") +
  annotate("text", x = max_my_model$epoch, 
           y = max_my_model$`SpeciesSeg-mobil`, label = "maximum mAP \n SpeciesSeg-mobil", colour = "black", vjust = 1.1)+
  # ggtitle("Comparison of MAP (50-95) for masks between YOLO models") +
  theme_bw() +
  theme(text= element_text(family = "serif", size=12),
        plot.margin = margin(0.1, 0.1, 0.1, 0.1, "cm"),
        legend.position=c(0.85,.17)) 


ggplot(data = df_plot, aes(x=epoch, y=mAP)) +
  geom_line(linewidth=1.2, aes(color=Model)) +
  scale_x_continuous("Epoch", breaks = seq(0,300, 50)) +
  scale_y_continuous(TeX("Segment mAP $_{@0.5-0.95}$"), breaks = seq(0, 1, by = 0.2)) +
  scale_color_manual(values = cbPalette[2:6]) +
  geom_point(data = max_base_model, aes(x = epoch, y = `YOLOv8n-seg`, color = "YOLOv8n-seg max"), size = 3) +
  geom_text(data = max_base_model, aes(x = epoch, y = `YOLOv8n-seg`, label = "maximum mAP \n YOLOv8n-seg"), colour = "black", vjust = 1.1) +
  geom_point(data = max_my_model, aes(x = epoch, y = `SpeciesSeg-mobil`, color = "SpeciesSeg-mobil max"), size = 3) +
  geom_text(data = max_my_model, aes(x = epoch, y = `SpeciesSeg-mobil`, label = "maximum mAP \n SpeciesSeg-mobil"), colour = "black", vjust = 1.1) +
  theme_bw() +
  theme(text= element_text(family = "serif", size=12),
        plot.margin = margin(0.1, 0.1, 0.1, 0.1, "cm"),
        legend.position=c(0.85,.17)) 
