# nvidia-gan2

Modified implementation of https://github.com/JonnyJive5/gaugan that's updated to work with the newest version of nvidia's gaugan and implements custom style images and multithreading.

arguments for running:
  -s / --style
  -t / --threads
  
| Flag  | Argument | Example value |
| ------------- | ------------- | ------------- |
| -s / --style  | Style image to be used for generating the output. Can eather be a number from 0 to 10, corresponding to the style from the GauGAN web app from left to right starting with 0 or the path to the custom image you want to use | 0, 1, 8, ../Styles/night.png |
| -t / --threads  | How many threads can be run at once. It will generate that many images at once | 1, 2, 5, 10 |

Instructions:
Create a folder and place gan.py in it. Create two folders inside as well, one named 'In' and one named 'Out' Place your input maps in the in folder. In the terminal, navigate to the location of your folder containing the above. This script can be run with the following command: python3 gan.py -s # -t #
