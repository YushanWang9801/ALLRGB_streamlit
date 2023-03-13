import streamlit as st
from PIL import Image

import numpy as np 
import random
import math
import octree
import io

def load_image(test_image):
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

def load_indexes():
    points = [2048, 2048]  # half of the size
    def index_func(index):
        x, y = index % 4096, index / 4096
        offset = (random.random() - 0.5) * 512
        return min(math.hypot(x - a, y - b) for a, b in points) + offset
    indexes = np.arange(4096*4096)
    random.shuffle(indexes)
    return indexes 

def main():
    st.title('Upload image to transfer to ALLRGB images')

    st.subheader('A simple app that one may upload single image get a copy'+
                 'get allRGB image files.')
    
    st.write("This project is inspired by the original work done by Michael Fogleman.")
    st.write("https://www.michaelfogleman.com/projects/allrgb/")

    st.write("What different than the previous project is we allow images to enter"+
             "any sizes. Michael Fogleman only allows image to be size of 4096 x 4096. "+
             "Firstly, we did the resize and fit into a square size of 4096 x 4096" +
             " with black pixels.")
    
    st.write("For the concept of ALLRGB image, one could visit https://allrgb.com/ to see more.")
    
    st.write("if you wish to render your ALLRGB image on your local python environment,"+
             "then you can go to my this github repo: " +
             "https://github.com/YushanWang9801/AllRGB")

    st.write("This is a demo of what you could expect: ")
    st.image('output_image2.jpg', use_column_width=True)

    st.write("Now upload your own photo and start creating ... ")
    st.write('The process might be slow, since there are 4096 x4096 number'+
                 'pixels need to be assigned to different colors')
    uploaded_file = st.file_uploader("Choose a image to uplaoad: ", 
                                        accept_multiple_files=False,
                                        type=['jpg','png','jpeg'])

    indexes = load_indexes()
    tree = octree.Octree()

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        Blue, Green, Red = load_image(image)
        colors = [(0, 0, 0)] * (4096 * 4096)
        my_bar = st.progress(0)

        print("Start Processing, it would take a while ...")
        for i, index in enumerate(indexes):
            if i % (65536) == 0:
                percent_complete = i / (4096*4096)
                my_bar.progress(percent_complete)
            colors[index] = tree.pop(int(Red[index]), int(Green[index]), int(Blue[index]))
        
        data = np.array(colors).reshape((4096, 4096,3))
        im = Image.fromarray(data.astype(np.uint8), 'RGB')
        st.write("Here is your ALLRGB image: ")
        st.image(im, use_column_width=True)

        buf = io.BytesIO()
        image.save(buf, format='JPEG')
        image = buf.getvalue()


        st.download_button(
            label="Download image",
            data=image,
            file_name="allRGB.png",
            mime="image/png"
          )
        
    st.write("if you like this design, you can also checkout my website: ")
    st.write("https://yushanwang9801.github.io/ ")


if __name__ == "__main__":
    main()