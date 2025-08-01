import os
import glob

output = glob.glob("output/*.jpg")

for image in output:
    print(f"removed {image}")
    os.remove(image)

print("Workspace Cleared")

