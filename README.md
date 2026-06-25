# metropolis_message_animation
python code that uses metropolis hastings to generate random points that highlight desired message for high number of points. Uses image scanning, and matplotlib's basic stuff plus animation.

the project combines different programs for different steps of the treatment : 

1. filter.py inputs the scanned image of your message and applied a first treatment : converts it into B&W, crops the border (usually with scan default), and removes the remaining defaults by applying a treshold over the B&W value. This returns the filtered image that will be used as input for the next step.

2. diffuse.py inputs the filtered image returned by the previous step. This steps diffuses the message so that the probability density function of your image may be non-zero close to your writing. This step requires to specify the filtered file to input. The way it makes the diffusion is simply via several iterations of convolution within the whole image : you take the mean value of some rectangle around the considered pixel. Convolution width and number of iterations may be adjusted manually depending on your picture.

3. metropolis.py inputs the filtered-then-diffused image to generate the points everywhere on the space and give evolution to their position via metropolis-hastings. This process requires 2D interpolation of image to have the continuity effect over the points distribution rather dans discrete like with the pixel by pixel image. This program inputs the filtered-then-diffused image, makes the 2d interpolation, generate n-points uniformly over the whole domain, and make them evolve for a defined number of iterations (ctrbound) and preventing getting stuck at position (saturationbound). This code finaly displays the distribution of the points after evolution and saves the points dataset ready to be animated.

4. garbage.py animates the points saved by metropolis.py. This is just for means of aesthetics.
