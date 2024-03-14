import pandas as pd
import pathlib
import os

import shutil

dst_folder = r""

old_folder = r""

df = pd.read_csv(
    r"image_species_table_lieferung_12_01_24.txt", sep="\t")


for index, row in df.iterrows():
    folder_name = row['label']
    file_name = row['foto']
    file_path = row['filepath']

    # create folder for species if not exists
    pathlib.Path(os.path.join(dst_folder, folder_name)
                 ).mkdir(parents=True, exist_ok=True)

    # check if image already exists in old data set delivery
    # if it already exists do not copy to new species folder
    old_filepath = os.path.join(old_folder, folder_name, file_name)
    if not os.path.isfile(old_filepath):
        # set destination filepath
        dst_file_path = os.path.join(dst_folder, folder_name, file_name)

        # copy file in specific species folder
        shutil.copyfile(src=file_path, dst=dst_file_path)
