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
img = r"C:\Users\scanman\Documents\Jannik_Vikari\final_results\python_scripts\final_python_code_rep\master-thesis\data_set_overview_images\visualize_annot\1685089748847_jpg.rf.8515a577fab5b07736c99bfbc7454178.jpg"
annot = r"C:\Users\scanman\Documents\Jannik_Vikari\final_results\python_scripts\final_python_code_rep\master-thesis\data_set_overview_images\visualize_annot\1685089748847_jpg.rf.8515a577fab5b07736c99bfbc7454178.txt"
output_folder = r"C:\Users\scanman\Documents\Jannik_Vikari\final_results\python_scripts\final_python_code_rep\master-thesis\data_set_overview_images\visualize_annot"

# get names of labels
class_names = model.names

# Open the image file
im = cv2.imread(img)
im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

print(im)

# Create figure and axes
fig, ax = plt.subplots(1, 2)

# Adjust the space between subplots
plt.subplots_adjust(wspace=0.05)

# Display the image
ax[0].imshow(im)
ax[1].imshow(im)

# Set titles and remove axes
ax[0].axis('off')
ax[1].axis('off')

# Open the annotation file
with open(annot) as f:
    lines = f.readlines()

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
                              edgecolor="r", facecolor="r", linewidth=2, alpha=0.4)

    # Add the patch to the Axes
    ax[1].add_patch(polygon)

    # calculate top letf corner
    top_left = polygon.get_xy().min(axis=0)

    # add the description
    # there is class index equal to 23. But model has only 22 classes. Mit Julian abklären

    t_class = ax[1].text(
        top_left[0], top_left[1], f"{str(class_names[class_index])}", color="w", fontsize=8,
        ha='left', va='top'
    )


# Save the figure instead of showing it
plt.savefig(os.path.join(output_folder, f'annot.jpg'), dpi=300)
plt.close()
