from PIL import Image
# pick an image file you have in the working directory
# (or give full path name)
image_file = "bg_changwon.png"
img = Image.open(image_file)
# get the image's width and height in pixels
width, height = img.size

print width, height 