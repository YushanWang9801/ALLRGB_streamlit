### ALL RGB Image Generator

We create one ALLRGB image generator in this repo. This project will read in one
input image and output an ALLRGB image. 

This project is inspired by the original work done by Michael Fogleman.
https://www.michaelfogleman.com/projects/allrgb/

What different than the previous project is we allow images to enter any sizes. 
Michael Fogleman only allows image to be size of 4096 x 4096. Firstly, we did the resize
and fit into a square size of 4096 x 4096 with black pixels. 

For the concept of ALLRGB image, one could visit https://allrgb.com/ to see more.

after cloning to your local directory, to run this repo:

```{python}
python ./main.py
```
The running program then will ask you to enter the input image path and the desired
output image path. For example:

```{python}
Please enter your input image file path:
input_image.jpg

Please enter your output image file path:
output_image.jpg
```

![demo of generated ALLRGB image](./output_image2.jpg)