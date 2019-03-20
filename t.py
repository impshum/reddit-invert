from PIL import Image
import PIL.ImageOps


image = Image.open('data/x4RUp9d.jpg')

inverted_image = PIL.ImageOps.invert(image)

inverted_image.save('data/out.jpg')
