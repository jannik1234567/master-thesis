from pathlib import Path
import os
import cv2
import numpy as np
import matplotlib.patches as patches
from shapely.geometry import Polygon


ANNOTATED_IMAGES_PATH = r""
OUT_FOLDER = r""

TILE_SIZE_X = 224
TILE_SIZE_Y = 224
PERCENTAGE_BACKGROUND = 50


def tile_image(image, tile_size_x: int, tile_size_y: int) -> list:
    """Split the image into tiles of the specified size

    Args:
        image: loaded image with open cv
        tile_size (int): size of the tile, it is squared

    Returns:
        list: tiles of the image
    """
    tiles = []
    for y in range(0, image.shape[0], tile_size_y):
        for x in range(0, image.shape[1], tile_size_x):
            tile = image[y:min(y+tile_size_y, image.shape[0]),
                         x:min(x+tile_size_x, image.shape[1])]

            # If the tile is smaller than the desired size, add padding
            if tile.shape[0] < tile_size_y or tile.shape[1] < tile_size_x:
                tile = cv2.copyMakeBorder(tile,
                                          top=0,
                                          bottom=tile_size_y - tile.shape[0],
                                          left=0,
                                          right=tile_size_x - tile.shape[1],
                                          borderType=cv2.BORDER_CONSTANT,
                                          value=[0, 0, 0])  # Change padding color as needed

            tiles.append(tile)

    return tiles


def filter_tiles_backgorund_content(tiles, percentage_background):
    filtered_tiles = []

    for tile in tiles:
        # Calculate the number of black pixels in the tile
        num_black_pixels = np.sum(tile == 0)

        # Calculate the total number of pixels in the tile
        total_pixels = tile.shape[0] * tile.shape[1]

        # Calculate the percentage of black pixels
        percent_black_pixels = (num_black_pixels / total_pixels) * 100

        # If the percentage of black pixels is less than or equal to percentage blackground, add the tile to the filtered list
        if percent_black_pixels <= percentage_background:
            filtered_tiles.append(tile)

    return filtered_tiles


def tile_masks_for_classification(annotated_images_path: str | os.PathLike,
                                  out_folder: str | os.PathLike,
                                  tile_size_x: int, tile_size_y: int,
                                  percentage_background: int):
    """
    reannotate images in folder and move images and annotations to output folder
    """

    # get all tree species folders in folder
    tree_paths = [x for x in Path(
        annotated_images_path).iterdir() if x.is_dir()]

    i_image = 1
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
                i_image = 1

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

                    # Undo normalization (x times width, and y times height)
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

                    tiles = tile_image(
                        cut_image, tile_size_x=tile_size_x, tile_size_y=tile_size_y)

                    # List to hold the tiles with less than x black pixels
                    filtered_tiles = filter_tiles_backgorund_content(
                        tiles=tiles, percentage_background=percentage_background)

                    if 'valid' in str(filename):
                        Path(os.path.join(out_folder, 'val', class_name)).mkdir(
                            parents=True, exist_ok=True)

                        dst_path = os.path.join(
                            out_folder, 'val', class_name)

                    if 'test' in str(filename):
                        Path(os.path.join(out_folder, 'test', class_name)).mkdir(
                            parents=True, exist_ok=True)

                        dst_path = os.path.join(out_folder, "test", class_name)

                    if 'train' in str(filename):
                        Path(os.path.join(out_folder, 'train', class_name)).mkdir(
                            parents=True, exist_ok=True)

                        dst_path = os.path.join(
                            out_folder, "train", class_name)

                    # Loop over the filtered tiles
                    for i_tile, tile in enumerate(filtered_tiles):
                        # Define the filename for each tile
                        name_tile = f"tile_{i_tile}.jpg"

                        complete_file_name = f'{dst_path}/{filename.stem}_{i_image}_{name_tile}'

                        # Save the tile as a .jpg image
                        cv2.imwrite(complete_file_name, tile)

                    # update index
                    i_image += 1


if __name__ == '__main__':
    tile_masks_for_classification(annotated_images_path=ANNOTATED_IMAGES_PATH,
                                  out_folder=OUT_FOLDER,
                                  tile_size_x=TILE_SIZE_X, tile_size_y=TILE_SIZE_Y,
                                  percentage_background=PERCENTAGE_BACKGROUND)
