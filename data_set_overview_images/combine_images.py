import matplotlib.pyplot as plt
import matplotlib.patches as patches
import cv2
import numpy as np
from pathlib import Path
import os

output_folder = r"C:\Users\janni\Dokumente\Masterarbeit\python_scripts\final_python_scripts\master-thesis\data_set_overview_images"

img_files = [Path(r"C:\Users\janni\Dokumente\Masterarbeit\python_scripts\final_python_scripts\master-thesis\data_set_overview_images\TLS_1_CFB022.jpg"),
             Path(r"C:\Users\janni\Dokumente\Masterarbeit\python_scripts\final_python_scripts\master-thesis\data_set_overview_images\TLS_2_ettenheim.jpg"),
             Path(r"C:\Users\janni\Dokumente\Masterarbeit\python_scripts\final_python_scripts\master-thesis\data_set_overview_images\TLS_3_ettenheim.jpg"),
             Path(r"C:\Users\janni\Dokumente\Masterarbeit\python_scripts\final_python_scripts\master-thesis\data_set_overview_images\TLS_4_dgl.jpg")]

# titles = ['I) Pseudotsuga menziesii', 'II) Pseudotsuga menziesii', 'III) Abies alba', 'IV) Pseudotsuga menziesii']
letters = ["A", "B", "C", "D"]

# create big plot
fig, ax = plt.subplots(1, 4, figsize=(9, 3.5))
# Adjust the space between subplots
plt.subplots_adjust(wspace=0.05, hspace=0.03)

used_classes = set()
legend_patches = []

for i_file, file in enumerate(img_files):
    file_name = file.stem

    # Open the image file
    im = cv2.imread(str(file))
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

    # Display the image
    ax[i_file].imshow(im, aspect="auto")

    # Set titles and remove axes
    ax[i_file].axis('off')

    ax[i_file].text(0.037, 0.935, letters[i_file], transform=ax[i_file].transAxes, fontsize=10,
                    fontweight='bold', color='white', bbox=dict(facecolor='black', edgecolor='black'))


plt.savefig(os.path.join(output_folder, f'combined_TLS.png'),
            dpi=300, bbox_inches='tight')
plt.close()
