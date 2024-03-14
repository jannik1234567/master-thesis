from pathlib import Path
import os
import shutil


ANNOTATED_IMAGES_PATH = r""
OUT_FOLDER = r""


def make_and_move_annot_images(annotated_images_path: str | os.PathLike,
                               out_folder: str | os.PathLike,
                               create_class_txt=True):
    """
    reannotate images in folder and move images and annotations to output folder
    """

    # set class integer to zero for first iteration
    class_int = 0

    # get all tree species folders in folder
    tree_paths = [x for x in Path(
        annotated_images_path).iterdir() if x.is_dir()]

    # iterate through species folders
    for folder_path in tree_paths:

        # rannotate the labels in specific species folder with current class integer
        # find all txt files in subfolders of given folderpath
        for filename in Path(folder_path).rglob('*.txt'):
            result = ""
            with open(filename, 'r') as f:
                for line in f:
                    list = line.split(' ')
                    list[0] = str(class_int)
                    line = " ".join(list)
                    result += line

            f = open(filename, 'w')  # should be in 'wt or 'w' mode
            f.write(result)
            f.close()

            # copy the label txts in the output folder, but in valid, test, train accordingly
            if 'valid' in str(filename):
                Path(os.path.join(out_folder, 'valid', "labels")).mkdir(
                    parents=True, exist_ok=True)

                dst_path = os.path.join(out_folder, "valid", "labels")

                shutil.copy(src=str(filename), dst=str(dst_path))

            if 'test' in str(filename):
                Path(os.path.join(out_folder, 'test', "labels")).mkdir(
                    parents=True, exist_ok=True)

                dst_path = os.path.join(out_folder, "test", "labels")

                shutil.copy(src=str(filename), dst=str(dst_path))

            if 'train' in str(filename):
                Path(os.path.join(out_folder, 'train', "labels")).mkdir(
                    parents=True, exist_ok=True)

                dst_path = os.path.join(out_folder, "train", "labels")

                shutil.copy(src=str(filename), dst=str(dst_path))

        # copy all images in output folder, but in valid, test and train accordingly
        # find all jpg files in subfolders of given folderpath
        for filename in Path(folder_path).rglob('*.jpg'):
            if 'valid' in str(filename):
                Path(os.path.join(out_folder, 'valid', "images")).mkdir(
                    parents=True, exist_ok=True)

                dst_path = os.path.join(out_folder, "valid", "images")

                shutil.copy(src=str(filename), dst=str(dst_path))

            if 'test' in str(filename):
                Path(os.path.join(out_folder, 'test', "images")).mkdir(
                    parents=True, exist_ok=True)

                dst_path = os.path.join(out_folder, "test", "images")

                shutil.copy(src=str(filename), dst=str(dst_path))

            if 'train' in str(filename):
                Path(os.path.join(out_folder, 'train', "images")).mkdir(
                    parents=True, exist_ok=True)

                dst_path = os.path.join(out_folder, "train", "images")

                shutil.copy(src=str(filename), dst=str(dst_path))

        # add the current class integer and according class label to the classes.txt
        # with that you can check which class integer represents which class
        # class label depends on folder name of species
        if create_class_txt and len(os.listdir(folder_path)) != 0:
            # create path if it does not already exist
            Path(os.path.join(out_folder)).mkdir(
                parents=True, exist_ok=True)

            class_name = folder_path.name
            file_path = os.path.join(out_folder, 'classes.txt')
            f = open(file_path, 'a+')
            f.write(f'{class_int}: {class_name} \n')
            f.close()

        # update class integer for next iterartion/species folder
        class_int += 1


if __name__ == '__main__':
    make_and_move_annot_images(annotated_images_path=ANNOTATED_IMAGES_PATH,
                               out_folder=OUT_FOLDER,
                               create_class_txt=True)
