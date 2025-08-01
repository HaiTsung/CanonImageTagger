import PIL.ImageDraw, PIL.ImageFont
import exifread
from PIL import Image
import time
from tkinter import filedialog

counter = 0

images = filedialog.askopenfilename(title="Select file", filetypes=(("Images", "*.jpg"),), multiple=True)
images = list(images)

start = time.time()
def stringToBool(string:str):
    return True if string.lower() == "true" else False

try:
    parameters = open('parameters.txt')
except FileNotFoundError:
    parameters = open('parameters.txt', 'x')
    parameters.write("------PARAMETERS------\n"
"margin:100\n"
"showCameraModel:True\n"
"showFocalLength:True\n"
"showAperture:True\n"
"showExposureTime:True\n"
"showIso:True\n"
"useOverlay:True\n")
    parameters.close()
    parameters = open('parameters.txt')
content = parameters.read()
parameters.close()

content = content.split("\n")

margin = 100
showCameraModel = True
showFocalLength = True
showAperture = True
showExposureTime = True
showIso = True
useOverlay = True

try:
    margin = int(content[1].split(":")[1])
    print("Margin: " + str(margin))
    showCameraModel = stringToBool(content[2].split(":")[1])
    print(f"ShowCameraModel: {showCameraModel}")
    showFocalLength = stringToBool(content[3].split(":")[1])
    print(f"ShowFocalLength: {showFocalLength}")
    showAperture = stringToBool(content[4].split(":")[1])
    print(f"showAperture: {showAperture}")
    showExposureTime = stringToBool(content[5].split(":")[1])
    print(f"showExposureTime: {showExposureTime}")
    showIso = stringToBool(content[6].split(":")[1])
    print(f"showIso: {showIso}")
    useOverlay = stringToBool(content[7].split(":")[1])
    print(f"useOverlay: {useOverlay}")
except ValueError:
    print("Invalid parameter in parameters.txt")


overlay_portrait = Image.open("overlay.png")
overlay_landscape = Image.open("overlayLandscape.png")
font = PIL.ImageFont.truetype("arial", 128)

if not images:
    print("No valid images found")

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


    if aperture.__contains__("/"):
        a, b = aperture.split("/")
        aperture = int(a) / int(b)
        aperture = f"{aperture}"

    image = Image.open(src)

    y = src.split("/")
    y = y[len(y) - 1]
    y, none = y.split(".")

    if str(tags.get("Image Orientation")) == "Rotated 90 CCW":
        image = image.rotate(90, expand=True)
        overlay = overlay_landscape
    elif str(tags.get("Image Orientation")) == "Rotated 90 CW":
        image = image.rotate(-90, expand=True)
        overlay = overlay_landscape
    else:
        overlay = overlay_portrait


    if useOverlay:
        overlay = overlay.resize(image.size)
        image = image.convert("RGBA")
        image = Image.alpha_composite(image, overlay)

    draw = PIL.ImageDraw.Draw(image)

    testBox = draw.textbbox((0, 0), "Y", font=font)
    textHeight = testBox[3] - testBox[1]

    # CameraTag
    if showCameraModel and camera != "None":
        draw.text((margin, margin),text=camera,fill=(255,255,255),font=font)

    # FocalLengthTag
    if showFocalLength and focalLength != "None":
        testBox = draw.textbbox((0, 0), f"{focalLength} mm", font=font)
        textWidth = testBox[2] - testBox[0]
        draw.text((image.width-textWidth-margin, margin),text=f"{focalLength} mm",fill=(255,255,255),font=font)

    # ApertureTag
    if showAperture and aperture != "None":
        draw.text((margin, image.height - margin-textHeight),text=f"f {aperture}",fill=(255,255,255),font=font)

    # ExposureTimeTag
    if showExposureTime and exposureTime != "None":
        testBox = draw.textbbox((0, 0), exposureTime, font=font)
        textWidth = testBox[2] - testBox[0]
        draw.text((image.width/2 - textWidth / 2, image.height - margin-textHeight),text=exposureTime,fill=(255,255,255),font=font)

    # IsoTag
    if showIso and iso != "None":
        testBox = draw.textbbox((0, 0), f"ISO {iso}", font=font)
        textWidth = testBox[2] - testBox[0]
        draw.text((image.width-margin-textWidth, image.height - margin-textHeight),text=f"ISO {iso}",fill=(255,255,255),font=font)


    image = image.convert("RGB")
    image.save(f'output/{y}_tagged.jpg')
    print(f"tagged {src}")
    counter += 1
end = time.time()
print(f"completed in {((end - start) * 1000).__round__()} ms")
