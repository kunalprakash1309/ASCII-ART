from math import floor
from time import time
from PIL import Image, ImageDraw, ImageFont
import sys


if len(sys.argv) != 3:
    sys.exit("Usage: python ascii.py INPUT_FILE OUTPUT_FILE")

input_file = sys.argv[1]
output_file = sys.argv[2]



ASCII_CHARS = {
    0: "@",
    1: "#",
    2: "S",
    3: "%",
    4: "?",
    5: "*",
    6: "+",
    7: ";",
    8: ":",
    9: ",",
    10: ".",
    11: " "
}

sub_part = len(ASCII_CHARS)/255

# normal value of scalar_factor is 0.3
# config for concentrated image
# scalar_factor = 0.6    # 0.6 <= scalar_factor <= 1
# font_width = 2
# font_height = 6

# config for light image
scalar_factor = 0.2      # decrease to less than or equal to 0.1 if size of image is large 
font_width = 5          # you can change this value on your use(between 5 and 25)
font_height = 5         # you can change this value on your use (try to keep it same as font_width)   

# for adding different fonts
# font = ImageFont.truetype("ARIAL.TTF", 15)

def import_image(input_file):
    try: 
        im = Image.open(input_file)
        return im
    except Exception as error:
        print("Provide proper name or extension of input file")
        print(error)
        sys.exit(1)


def greyify_and_resize(im):
    im = im.convert('L')
    width = im.width
    height = im.height
    return im.resize((int(width*scalar_factor), int(height*scalar_factor*(font_width/font_height))))
  

def create_new_image(im):
    width = im.width
    height = im.height

    output_img = Image.new(mode='L', size=(width*font_width, height*font_height), color=(255))
    return output_img


def pixel_to_ascii(rgb):
    if rgb == 255:
        return ASCII_CHARS[len(ASCII_CHARS)-1]
    return ASCII_CHARS[floor(sub_part*rgb)]

def save_image(new_image):
    try:
        new_image.save(output_file)

    except Exception as error:
        print("Provide proper name or extension of Output file")
        print(error)
        sys.exit(1)



def main():
    t1 = time()*1000

    im = import_image(input_file)
    im = greyify_and_resize(im)

    new_image = create_new_image(im)
    d = ImageDraw.Draw(new_image)

    height = im.height
    width = im.width
    print(width, height)

    for i in range(height):
        for j in range(width):

            rgb = im.getpixel((j,i))

            char = pixel_to_ascii(rgb)

            d.text((j*font_width, i*font_height), char, fill=(0))
    
    save_image(new_image)
    im.close()

    t2 = time()*1000
    print(f"Total time taken {(t2-t1)/1000}s")


if __name__ == '__main__':
    main()

