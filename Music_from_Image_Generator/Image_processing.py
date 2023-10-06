import cv2
import matplotlib.pyplot as plt

# Load an image
ori_img = cv2.imread('cat1.jpg')

# Need function that reads pixel hue value
hsv = cv2.cvtColor(ori_img, cv2.COLOR_BGR2HSV)

# Plot the image
fig, axs = plt.subplots(1, 3, figsize=(15, 15))
names = ['BGR', 'RGB', 'HSV']
imgs = [ori_img, ori_img, hsv]  # Replace 'img' with 'ori_img'
i = 0
for elem in imgs:
    axs[i].title.set_text(names[i])
    axs[i].imshow(elem)
    axs[i].grid(False)
    i += 1
plt.show()
