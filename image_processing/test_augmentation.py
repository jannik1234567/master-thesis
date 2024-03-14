import albumentations as A
import cv2
import matplotlib.pyplot as plt


transform = A.Compose([
    A.RandomBrightnessContrast(p=1, brightness_limit=(-0.5, -0.5)),
])

image = cv2.imread(
    r"C:\Users\janni\Dokumente\Masterarbeit\images\test\test_image\1668412977862_jpg.rf.7ae946dc550b3acb983b948d0308e103.jpg")


transformed_image = transform(image=image)['image']
transformed_image2 = transform(image=image)['image']
transformed_image3 = transform(image=image)['image']

# Assuming your images are in the variables: image, transformed_image, transformed_image2, transformed_image3

# create a figure with 4 subplots
fig, ax = plt.subplots(1, 4, figsize=(20, 5))

# Plot original image
ax[0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
ax[0].set_title('Original Image')
ax[0].axis('off')

# Plot transformed images
ax[1].imshow(cv2.cvtColor(transformed_image, cv2.COLOR_BGR2RGB))
ax[1].set_title('Transformed Image 1')
ax[1].axis('off')

ax[2].imshow(cv2.cvtColor(transformed_image2, cv2.COLOR_BGR2RGB))
ax[2].set_title('Transformed Image 2')
ax[2].axis('off')

ax[3].imshow(cv2.cvtColor(transformed_image3, cv2.COLOR_BGR2RGB))
ax[3].set_title('Transformed Image 3')
ax[3].axis('off')

plt.show()
