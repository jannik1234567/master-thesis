import os
from pathlib import Path
import cv2

files = Path(
    r"C:\Users\janni\Dokumente\Masterarbeit\python_scripts\final_python_scripts\master-thesis\data_set_overview_images\examples_mobil_phone_data").glob('*.jpg')


for file in files:

    image = cv2.imread(str(file))

    height, width, _ = image.shape
    new_height = 160

    new_width = round(width//(height/new_height))
    new_image = cv2.resize(image, (new_width, new_height),
                           interpolation=cv2.INTER_AREA)

    # new_file_path = f"{os.path.splitext(file)[0]}_resize.jpg"
    cv2.imwrite(filename=str(file), img=new_image)
