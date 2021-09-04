import pandas as pd 
import numpy as np
from PIL import Image
from colors import color

print("\x1b[2J",end='')

#image source : WIKIMON
img_path = ("Ver.1_egg.gif")
img = np.array(Image.open(img_path).resize((16, 16)).convert("RGB"), dtype=np.uint8)

for row in img:
    for pixel in row:
        if all(pixel):
            print("  ", end="")
        else:
            print(color("  ", bg=f"rgb({pixel[0]}, {pixel[1]}, {pixel[2]})"), end="")
            
    print()