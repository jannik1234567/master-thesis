from pathlib import Path
from collections import Counter
import os
import csv

FOLDER_PATH = r""
OUT_FOLDER = r""


def get_class_count(folder_path, out_folder):
    """
    This function counts the number of instances of each class and the number of images per class in a given folder.
    """
    for file_path in Path(folder_path).rglob('*/'):
        if "labels" in str(file_path):
            label_list = []
            image_list = []
            for file in Path(file_path).glob('*txt'):
                with open(file, 'r') as f:
                    # count instances per class (if there are more than one tree in the image)
                    label_list += [line.split(' ')[0] for line in f]

                # count images per class
                # read only class label of image
                with open(file, 'r') as f:
                    first_line = f.readline()
                    general_label = first_line.split(' ')[0]
                    image_list.append(general_label)

                    if general_label == '':
                        print(file)

            # generate overview
            class_overview = dict(Counter(label_list))
            image_overview = dict(Counter(image_list))

            # save file for train, test and valid
            name = file_path.parent.name

            # first class overview
            overview_file = os.path.join(
                out_folder, f"cls_overview_{name}.txt")
            with open(overview_file, 'w', newline='') as txtfile:
                fieldnames = ['class', 'count']
                writer = csv.DictWriter(txtfile, fieldnames=fieldnames)

                writer.writeheader()
                writer.writerows(
                    [{'class': key, 'count': class_overview[key]} for key in class_overview])

            # second image overview
            img_overview_file = os.path.join(
                out_folder, f"img_overview_{name}.txt")
            with open(img_overview_file, 'w', newline='') as txtfile:
                fieldnames = ['class', 'count']
                writer = csv.DictWriter(txtfile, fieldnames=fieldnames)

                writer.writeheader()
                writer.writerows(
                    [{'class': key, 'count': image_overview[key]} for key in image_overview])


if __name__ == '__main__':
    get_class_count(folder_path=FOLDER_PATH, out_folder=OUT_FOLDER)
