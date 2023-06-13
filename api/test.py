import numpy as np
from PIL import Image
import cv2

image=Image.open("00000001_000.png")
image = np.asarray(image.resize((224, 224)))
image = cv2.cvtColor(image,cv2.COLOR_GRAY2RGB)
image = np.expand_dims(image, 0)
image = image / 255
print(image)

image3=Image.open("00000001_000.png")
image3 = np.asarray(image3)
image3 = cv2.cvtColor(image3,cv2.COLOR_GRAY2RGB)
image3 = np.expand_dims(image3, 0)
print(image3.shape)

image2=Image.open("1024px-A-DNA,_B-DNA_and_Z-DNA.png")
image2 = np.asarray(image2.resize((224, 224)))[..., :3]
image2 = np.expand_dims(image2, 0)
print(image2.shape)