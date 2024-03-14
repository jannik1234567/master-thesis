from pathlib import Path
import os
import shutil
import cv2
import numpy as np
import matplotlib.patches as patches
from shapely.geometry import Polygon


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

    i = 1
    # iterate through species folders
    for folder_path in tree_paths:

        # get class name
        class_name = folder_path.name

        # copy all images in output folder, but in valid, test and train accordingly
        # find all jpg files in subfolders of given folderpath
        for filename in Path(folder_path).rglob('*.jpg'):

            # Construct the corresponding txt file path
            txt_file_path = filename.parent.parent / 'labels' / filename.name

            txt_filename = txt_file_path.with_name(txt_file_path.stem + '.txt')

            # Check if the txt file exists
            if txt_filename.exists():
                # Open the txt file
                with open(txt_filename, 'r') as f:
                    lines = f.readlines()

                # create index if more masks are on one image
                i = 1

                # Loop over the lines in the annotation file
                for line in lines:

                    # Open the image file
                    img_bgr = cv2.imread(str(filename))

                    # Split the line into parts
                    parts = line.strip().split()

                    # Get coordinates
                    normalized_coords = list(map(float, parts[1:]))

                    # Reshape the coordinates into a 2D array
                    normalized_coords = np.array(
                        normalized_coords).reshape(-1, 2)

                    # Undo normalization
                    coords = normalized_coords * \
                        [img_bgr.shape[1], img_bgr.shape[0]]

                    # Create a Polygon patch
                    polygon = patches.Polygon(
                        coords, fill=True, edgecolor='white', facecolor='white', linewidth=2, alpha=0.4)

                    # Convert the matplotlib patch to a Shapely polygon
                    shapely_polygon = Polygon(polygon.get_xy())

                    # Convert the polygon coordinates to integer for OpenCV
                    poly_coords = np.array(
                        shapely_polygon.exterior.coords, dtype=np.int32)

                    # Create a black image with the same dimensions as your original image
                    mask = np.zeros_like(img_bgr)

                    # Fill the polygon with white in the black image
                    cv2.fillPoly(mask, [poly_coords], (255, 255, 255))

                    # Bitwise AND operation between the mask and original image
                    result = cv2.bitwise_and(img_bgr, mask)

                    # Get the bounding rectangle for the polygon
                    x, y, w, h = cv2.boundingRect(poly_coords)

                    # Cut out the bounding box from the image
                    cut_image = result[y:y+h, x:x+w]

                    if 'valid' in str(filename):
                        Path(os.path.join(out_folder, 'valid', class_name)).mkdir(
                            parents=True, exist_ok=True)

                        dst_path = os.path.join(
                            out_folder, 'valid', class_name)

                        cv2.imwrite(
                            f'{dst_path}/{filename.stem}_{i}.jpg', cut_image)

                    if 'test' in str(filename):
                        Path(os.path.join(out_folder, 'test', class_name)).mkdir(
                            parents=True, exist_ok=True)

                        dst_path = os.path.join(out_folder, "test", class_name)

                        cv2.imwrite(
                            f'{dst_path}/{filename.stem}_{i}.jpg', cut_image)

                    if 'train' in str(filename):
                        Path(os.path.join(out_folder, 'train', class_name)).mkdir(
                            parents=True, exist_ok=True)

                        dst_path = os.path.join(
                            out_folder, "train", class_name)

                        cv2.imwrite(
                            f'{dst_path}/{filename.stem}_{i}.jpg', cut_image)

                    # update index
                    i += 1


if __name__ == '__main__':
    move_annot_images(annotated_images_path=ANNOTATED_IMAGES_PATH,
                      out_folder=OUT_FOLDER)
