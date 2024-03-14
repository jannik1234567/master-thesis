from pathlib import Path
import os
import shutil


ANNOTATED_IMAGES_PATH = r""
OUT_FOLDER = r""


def move_annot_images(annotated_images_path: str | os.PathLike,
                      out_folder: str | os.PathLike):
    """
    reannotate images in folder and move images and annotations to output folder
    """

    # get all tree species folders in folder
    tree_paths = [x for x in Path(
        annotated_images_path).iterdir() if x.is_dir()]

    # iterate through species folders
    for folder_path in tree_paths:

        # get class name
        class_name = folder_path.name

        # copy all images in output folder, but in valid, test and train accordingly
        # find all jpg files in subfolders of given folderpath
        for filename in Path(folder_path).rglob('*.jpg'):
            if 'valid' in str(filename):
                Path(os.path.join(out_folder, 'valid', class_name)).mkdir(
                    parents=True, exist_ok=True)

                dst_path = os.path.join(out_folder, 'valid', class_name)

                shutil.copy(src=str(filename), dst=str(dst_path))

            if 'test' in str(filename):
                Path(os.path.join(out_folder, 'test', class_name)).mkdir(
                    parents=True, exist_ok=True)

                dst_path = os.path.join(out_folder, "test", class_name)

                shutil.copy(src=str(filename), dst=str(dst_path))

            if 'train' in str(filename):
                Path(os.path.join(out_folder, 'train', class_name)).mkdir(
                    parents=True, exist_ok=True)

                dst_path = os.path.join(out_folder, "train", class_name)

                shutil.copy(src=str(filename), dst=str(dst_path))


if __name__ == '__main__':
    move_annot_images(annotated_images_path=ANNOTATED_IMAGES_PATH,
                      out_folder=OUT_FOLDER)
