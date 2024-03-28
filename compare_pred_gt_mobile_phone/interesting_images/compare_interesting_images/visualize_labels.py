import matplotlib.pyplot as plt
import matplotlib.patches as patches
import cv2
import numpy as np
from pathlib import Path
import os
from ultralytics import YOLO
from tqdm import tqdm

model = YOLO(r"C:\Users\scanman\Documents\Jannik_Vikari\final_results\python_scripts\tree_species_weighted_sampler\train_yolo_weighted_sampler_augment_tuned\runs\segment\train\weights\best.pt")

# get names of labels
def format_string(dict_input):
    formatted_dict = {}
    for key, value in dict_input.items():
        words = value.split('_')
        words[0] = words[0].capitalize()
        formatted_dict[key] = ' '.join(words)
    return formatted_dict

class_names = model.names

class_names = format_string(class_names)

print(class_names)

# img folder:
img_folder = r"C:\Users\scanman\Documents\Jannik_Vikari\final_results\python_scripts\compare_pred_gt_mobile_phone\interesting_images"
annot_folder = r"C:\Users\scanman\Documents\Jannik_Vikari\final_results\image_data\tree_species_data_15_01_24\test\labels"
predict_folder = r"C:\Users\scanman\Documents\Jannik_Vikari\final_results\python_scripts\compare_pred_gt_mobile_phone\pred_yolo_n_weighted_sampler_augment_tuned_conf_standard\labels"
output_folder = r"C:\Users\scanman\Documents\Jannik_Vikari\final_results\python_scripts\compare_pred_gt_mobile_phone\interesting_images\compare_interesting_images"

# Create a colormap
cmap = plt.get_cmap('nipy_spectral', 24)

# Generate an array of indices from 0 to 21
indices = np.arange(24)

# Use the colormap to get the colors
color_map = cmap(indices)

img_files = [Path(r"C:\Users\scanman\Documents\Jannik_Vikari\final_results\python_scripts\compare_pred_gt_mobile_phone\interesting_images\1684339987324_jpg.rf.19143cafde9bbea81225e89c7523fcb7.jpg"),
             Path(r"C:\Users\scanman\Documents\Jannik_Vikari\final_results\python_scripts\compare_pred_gt_mobile_phone\interesting_images\1685527625760_jpg.rf.993cccdc9a9a014b03922edb6be741f3.jpg"),
             Path( r"C:\Users\scanman\Documents\Jannik_Vikari\final_results\python_scripts\compare_pred_gt_mobile_phone\interesting_images\1687267992097_jpg.rf.0a9ce45b8dd4e42849e36818a2ec079b.jpg"),
             Path(r"C:\Users\scanman\Documents\Jannik_Vikari\final_results\python_scripts\compare_pred_gt_mobile_phone\interesting_images\1686646206427_jpg.rf.1223e915ed03f28eca5d015f6da2fe84.jpg")]

titles = ['I) Pseudotsuga menziesii', 'II) Pseudotsuga menziesii', 'III) Abies alba', 'IV) Pseudotsuga menziesii']



# create big plot 
fig, ax = plt.subplots(3, 4, figsize=(7, 7))
# Adjust the space between subplots
plt.subplots_adjust(wspace=0.05, hspace=0.03)

used_classes = set()
legend_patches = []

for i_file, file in tqdm(enumerate(img_files), total=len(list(img_files))):
    file_name = file.stem

    # Open the image file
    im = cv2.imread(os.path.join(img_folder, f'{file_name}.jpg'))
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

    # Display the image
    ax[0][i_file].imshow(im, aspect="auto")
    ax[1][i_file].imshow(im, aspect="auto")
    ax[2][i_file].imshow(im, aspect="auto")

    # Set titles and remove axes
    ax[0][i_file].axis('off')
    ax[1][i_file].axis('off')
    ax[2][i_file].axis('off')
    
    ax[0][i_file].set_title(titles[i_file], fontsize=7)
    ax[0][i_file].text(0.045, 0.902, f'A{i_file}', transform=ax[0][i_file].transAxes, fontsize=10, fontweight='bold', color='white', bbox=dict(facecolor='black', edgecolor='black'))
    ax[1][i_file].text(0.045, 0.902, f'B{i_file}', transform=ax[1][i_file].transAxes, fontsize=10, fontweight='bold', color='white', bbox=dict(facecolor='black', edgecolor='black'))
    ax[2][i_file].text(0.045, 0.902, f'C{i_file}', transform=ax[2][i_file].transAxes, fontsize=10, fontweight='bold', color='white', bbox=dict(facecolor='black', edgecolor='black'))

    # Open the annotation file
    try:
        with open(os.path.join(annot_folder, f'{file_name}.txt')) as f:
            lines = f.readlines()

            if all(line == '\n' for line in lines):
                continue  # when the annotation file is empty there can be nothing compared
    except FileNotFoundError:
        continue  # if there is no true label file it can not be compared. go to next image file

    # Loop over the lines in the annotation file
    for line in lines:
        # Split the line into parts
        parts = line.strip().split()

        # Get the class and coordinates
        class_index = int(parts[0])
        coords = list(map(float, parts[1:]))

        # Reshape the coordinates into a 2D array
        coords = np.array(coords).reshape(-1, 2)

        # Create a Polygon patch
        polygon = patches.Polygon(coords * [im.shape[1], im.shape[0]], fill=True,
                                  edgecolor=color_map[class_index], facecolor=color_map[class_index], linewidth=2, alpha=0.4)

        # Add the patch to the Axes
        ax[1][i_file].add_patch(polygon)

        # only create patch if not already created
        if class_index not in used_classes:
            # Create a patch for the legend
            if class_index == 23:
                legend_patch = patches.Patch(
                    color=color_map[class_index], label='no_label')
                legend_patches.append(legend_patch)
            else:
                legend_patch = patches.Patch(
                    color=color_map[class_index], label=str(class_names[class_index]))
                legend_patches.append(legend_patch)

        # add class to used classes set
        used_classes.add(class_index)

        # calculate top letf corner
        top_left = polygon.get_xy().min(axis=0)

    # Open the prediction file
    try:
        with open(os.path.join(predict_folder, f'{file_name}.txt')) as f:
            lines = f.readlines()

        # Loop over the lines in the prediction file
        for line in lines:
            # Split the line into parts
            parts = line.strip().split()

            # Get the class and coordinates
            class_index = int(parts[0])
            coords = list(map(float, parts[1:]))

            # Reshape the coordinates into a 2D array
            coords = np.array(coords).reshape(-1, 2)

            # Create a Polygon patch
            polygon = patches.Polygon(coords * [im.shape[1], im.shape[0]], fill=True,
                                      edgecolor=color_map[class_index], facecolor=color_map[class_index], linewidth=2, alpha=0.4)

            # Add the patch to the Axes
            ax[2][i_file].add_patch(polygon)

            # only create patch if not already created
            if class_index not in used_classes:
                legend_patch = patches.Patch(
                    color=color_map[class_index], label=str(class_names[class_index]))
                legend_patches.append(legend_patch)

            # add class to used classes set
            used_classes.add(class_index)
    except FileNotFoundError:
        pass

# Create an additional subplot for the legend
fig.legend(handles=legend_patches, loc='lower center', bbox_to_anchor=(0.515, 0.055),
            fancybox=False, shadow=False, ncol=3)

plt.savefig(os.path.join(output_folder, f'{file_name}.jpg'), dpi=300, bbox_inches='tight')
plt.close()
