import PIL.ImageDraw, PIL.ImageFont
import exifread
from PIL import Image
import glob
import time

start = time.time()
images = glob.glob("input/*.jpg")
counter = 0

margin = 100

overlay_portrait = Image.open("overlay.png")
overlay_landscape = Image.open("overlay_Landscape.png")
font = PIL.ImageFont.truetype("arial", 128)

if not images:
    print("No images in input directory found")

for src in images:
    imageMeta = open(src, "rb")
    tags = exifread.process_file(imageMeta)
    print(f"tagging {src}")
    camera = str(tags.get("Image Model"))
    lens = str(tags.get("EXIF LensModel"))
    focalLength = str(tags.get("EXIF FocalLength"))
    aperture = str(tags.get("EXIF FNumber"))
    exposureTime = str(tags.get("EXIF ExposureTime"))
    iso = str(tags.get("EXIF ISOSpeedRatings"))

    a, b = aperture.split("/")
    aperture = int(a) / int(b)
    aperture = f"{aperture}"

    image = Image.open(src)

    none, y = src.split("\\")
    y, none = y.split(".")

    if str(tags.get("Image Orientation")) == "Rotated 90 CCW":
        image = image.rotate(90, expand=True)
        overlay = overlay_landscape
    elif str(tags.get("Image Orientation")) == "Rotated 90 CW":
        image = image.rotate(-90, expand=True)
        overlay = overlay_landscape
    else:
        overlay = overlay_portrait


    overlay = overlay.resize(image.size)

    image = image.convert("RGBA")
    image = Image.alpha_composite(image, overlay)

    draw = PIL.ImageDraw.Draw(image)

    # CameraTag
    draw.text((margin, margin),text=camera,fill=(255,255,255),font=font)

    # FocalLengthTag
    testBox = draw.textbbox((0, 0), f"{focalLength} mm", font=font)
    textWidth = testBox[2] - testBox[0]
    textHeight = testBox[3] - testBox[1]
    draw.text((image.width-textWidth-margin, margin),text=f"{focalLength} mm",fill=(255,255,255),font=font)

    # ApertureTag
    draw.text((margin, image.height - margin-textHeight),text=f"f {aperture}",fill=(255,255,255),font=font)

    # ExposureTimeTag
    testBox = draw.textbbox((0, 0), exposureTime, font=font)
    textWidth = testBox[2] - testBox[0]
    draw.text((image.width/2 - textWidth / 2, image.height - margin-textHeight),text=exposureTime,fill=(255,255,255),font=font)

    # IsoTag
    testBox = draw.textbbox((0, 0), f"ISO {iso}", font=font)
    textWidth = testBox[2] - testBox[0]
    draw.text((image.width-margin-textWidth, image.height - margin-textHeight),text=f"ISO {iso}",fill=(255,255,255),font=font)


    image = image.convert("RGB")
    image.save(f'output/{y}_tagged.jpg')
    print(f"tagged {src}")
    counter += 1
end = time.time()
print(f"completed in {((end - start) * 1000).__round__()} ms")
