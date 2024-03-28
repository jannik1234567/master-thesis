import matplotlib.pyplot as plt
import matplotlib.patches as patches
import cv2
import numpy as np
from pathlib import Path
import os
import collections
from ultralytics import YOLO

model = YOLO(r"C:\Users\scanman\Documents\Jannik_Vikari\final_results\python_scripts\tree_species_weighted_sampler\train_yolo_weighted_sampler_augment_tuned\runs\segment\train\weights\best.pt")

# get names of labels
class_names = model.names

# img folder:
img_folder = r"C:\Users\scanman\Documents\Jannik_Vikari\final_results\image_data\tree_species_data_15_01_24\test\images"
annot_folder = r"C:\Users\scanman\Documents\Jannik_Vikari\final_results\image_data\tree_species_data_15_01_24\test\labels"
predict_folder = r"C:\Users\scanman\Documents\Jannik_Vikari\final_results\python_scripts\compare_pred_gt_mobile_phone\pred_yolo_n_weighted_sampler_augment_tuned_conf_standard\labels"
output_folder = r"C:\Users\scanman\Documents\Jannik_Vikari\final_results\python_scripts\compare_pred_gt_mobile_phone\compare_gt_pred"

# Create a colormap
cmap = plt.get_cmap('nipy_spectral', 24)

# Generate an array of indices from 0 to 21
indices = np.arange(24)

# Use the colormap to get the colors
color_map = cmap(indices)

for file in Path(img_folder).glob('*.jpg'):
    file_name = file.stem

    # Open the image file
    im = cv2.imread(os.path.join(img_folder, f'{file_name}.jpg'))
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

    # Create figure and axes
    fig, ax = plt.subplots(1, 2)

    # Adjust the space between subplots
    plt.subplots_adjust(wspace=0.05)

    # Display the image
    ax[0].imshow(im)
    ax[1].imshow(im)

    # Set titles and remove axes
    ax[0].set_title('Original')
    ax[0].axis('off')
    ax[1].set_title('Prediction')
    ax[1].axis('off')

    # Open the annotation file
    try:
        with open(os.path.join(annot_folder, f'{file_name}.txt')) as f:
            lines = f.readlines()
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
        ax[0].add_patch(polygon)

        # calculate top letf corner
        top_left = polygon.get_xy().min(axis=0)

        # add the description
        # there is class index equal to 23. But model has only 22 classes. Mit Julian abklären
        if class_index == 23:
            t_class = ax[0].text(
                top_left[0], top_left[1], f"no_label", color="w", fontsize=5,
                ha='left', va='top'
            )
            t_class.set_bbox(dict(
                facecolor=color_map[class_index], alpha=0.5, edgecolor=color_map[class_index]
            ))
        else:
            t_class = ax[0].text(
                top_left[0], top_left[1], f"{str(class_names[class_index])}", color="w", fontsize=5,
                ha='left', va='top'
            )
            t_class.set_bbox(dict(
                facecolor=color_map[class_index], alpha=0.5, edgecolor=color_map[class_index]
            ))

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
            ax[1].add_patch(polygon)

            # calculate top letf corner
            top_left = polygon.get_xy().min(axis=0)

            # add the description
            t_class = ax[1].text(
                top_left[0], top_left[1], f"{str(class_names[class_index])}", color="w", fontsize=5,
                ha='left', va='top'
            )
            t_class.set_bbox(dict(
                facecolor=color_map[class_index], alpha=0.5, edgecolor=color_map[class_index]
            ))
    except FileNotFoundError:
        pass

    # Save the figure instead of showing it
    plt.savefig(os.path.join(output_folder, f'{file_name}.jpg'), dpi=300)
    plt.close()
