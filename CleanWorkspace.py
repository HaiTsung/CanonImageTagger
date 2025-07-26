import os
from os import remove
import glob

input = glob.glob("input/*.jpg")
output = glob.glob("output/*.jpg")

for image in input:
    print(f"removed {image}")
    os.remove(image)

for image in output:
    print(f"removed {image}")
    os.remove(image)

print("Workspace Cleared")

