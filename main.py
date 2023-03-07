import cv2
import numpy as np 
import random
import math

import octree
from PIL import Image

def load_image(file_path=""):
    test_image = Image.open(file_path)

    width,height = test_image.size
    if width >= height:
        width, height = 4096, int(height/width*4096)
    else:
        width, height = int(width/height*4096), 4096
    new_image = test_image.resize((width, height))
    resized_image = np.array(new_image)

    output_image = np.zeros((4096, 4096, 3))
    if resized_image.shape[1] == 4096:
        start_row = (4096-resized_image.shape[0])//2
        output_image[start_row: start_row+resized_image.shape[0], :] = resized_image[:,:,:]
    else:
        start_col = (4096-resized_image.shape[1])//2
        output_image[:, start_col:start_col+resized_image.shape[1]] = resized_image[:,:,:]

    Blue, Green, Red = output_image[:,:,2].reshape(-1), \
                       output_image[:,:,1].reshape(-1), \
                       output_image[:,:,0].reshape(-1)

    return Blue, Green, Red

#### Load Indexes
def load_indexes():
    points = [2048, 2048]  # half of the size
    def index_func(index):
        x, y = index % 4096, index / 4096
        offset = (random.random() - 0.5) * 512
        return min(math.hypot(x - a, y - b) for a, b in points) + offset
    indexes = np.arange(4096*4096)
    random.shuffle(indexes)
    return indexes 

file_path = input("Please enter your input image file path:")
output_path = input("Please enter your output image file path:")

Blue, Green, Red = load_image(file_path)
indexes = load_indexes()
tree = octree.Octree()

colors = [(0, 0, 0)] * (4096 * 4096)

for i, index in enumerate(indexes):
    if i % (65536*32) == 0:
        pct = 100.0 * i / (4096*4096)
        print ('{:2.2f} percent complete'.format(pct))
    colors[index] = tree.pop(int(Red[index]), int(Green[index]), int(Blue[index]))

data = np.array(colors).reshape((4096, 4096,3))
im = Image.fromarray(data.astype(np.uint8), 'RGB')
im.save(output_path)