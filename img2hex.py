import argparse, sys
from PIL import Image

def padded_hex(number, padding=2):
    # get hexadecimal representation at least [padding] digits wide
    return "{0:#0{1}x}".format(number,padding+2)

parser = argparse.ArgumentParser(description="turn images into sequences of hexadecimal values")
parser.add_argument("-w", "--width", help="digits of output hex numbers. defaults to 2.", type=int, action="store")
parser.add_argument("path", help="path to image", action="store")

args = parser.parse_args()
width = args.width
if width == None:
    width = 2

try:
    image = Image.open(args.path)
except FileNotFoundError:
    print("FATAL: could not find image at \"{}\"".format(args.path))
    sys.exit(-1)

data = image.getdata()

n = 0
number = 0
numbers = []
for i,pixel in enumerate(data):
    if (pixel == 0):
        number += 2**(4*width-n-1)
    n += 1
    if (n == 4*width):
        numbers.append(number)
        n = 0
        number = 0
    if (i == len(data)-1 and n != 0):
        print("({}) WARNING: image resolution is not a multiple of {}!".format(i,width))

array = "{ "
for i in range(len(numbers)):
    if ( i != len(numbers)-1 ):
        array += padded_hex(numbers[i],width) + ", "
    else:
        array += padded_hex(numbers[i],width)

array += " }"

print(array)


