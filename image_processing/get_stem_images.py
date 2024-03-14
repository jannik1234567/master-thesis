"""
 go through the subfolders of given folder and sample random 20 images and copy them the the destination folder


"""

import shutil
import random
import os

dirpath = r''
destDirectory = r''

for root, dirs, files in os.walk(dirpath):
    for d in dirs:
        folder_path = os.path.join(root, d)

        filenames = os.listdir(folder_path)

        if len(filenames) < 20:
            print(f'less files in{folder_path}')
            filenames_sample = os.listdir(folder_path)
        else:
            filenames_sample = random.sample(os.listdir(folder_path), 20)

        for fname in filenames_sample:
            srcpath = os.path.join(folder_path, fname)
            shutil.copy(srcpath, destDirectory)
