from PIL import Image
from pathlib import Path, WindowsPath
import os

try:
    os.mkdir('cropped')
except OSError as e:
    print(e)


image_path = Path('./').rglob('*.jpg') #finds all .jpg in current folder
images = [pic for pic in image_path]
count = 1
width = 0
height = 0

def crop(image_path, coords, save_location): #opens image and crops accoridng to given resolution
    image_obj = Image.open(image_path)
    cropped_image = image_obj.crop(coords)
    cropped_image.save(save_location)

for pic in images:
    if(not str(pic).__contains__('~')): #avoids cropping already cropped pictures
        cropped_location = './cropped/cropped_' + str(count) + '~.jpg' #~ is added to differentiate
        picture = Image.open(pic)
        pix = picture.load()
        w,h = picture.size

        for i in range (w - 1, 0, -1): #finds end of white space on width and sets as boundary
            r,g,b = pix[i,300]
            if(r > 245 and g > 245 and b > 245):
                width = i

        for i in range(h - 1, 0, -1): #finds end of white space on height and sets as boundary
            r,g,b = pix[300,i]
            if(r > 245 and g > 245 and b > 245):
                height = i

        crop_res = (3,0,width,height)
        crop(pic, crop_res, cropped_location)

        count += 1

cropped_path = Path('./cropped').rglob('*.jpg')
cropped_images = [pic for pic in cropped_path]
for pic in cropped_images:
    if(str(pic).__contains__("~")): #removes ~ from end of files
        os.rename(str(pic), str(pic)[:len(str(pic)) - 5] + '.jpg')