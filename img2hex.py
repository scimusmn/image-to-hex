
import argparse, sys
from PIL import Image

def padded_hex(number, padding=2, invert=False):
    # get hexadecimal representation at least [padding] digits wide
    if (invert):
        number = number ^ (2**(4*padding) - 1)
    return "{0:#0{1}x}".format(number,padding+2)

parser = argparse.ArgumentParser(description="turn images into sequences of hexadecimal values")
parser.add_argument("-w", "--width", help="digits of output hex numbers. defaults to 2.", type=int, action="store")
parser.add_argument("-i", "--invert", help="bitflip resulting array (white is 1 and black is 0)", action="store_true")
parser.add_argument("-r", "--reverse", metavar="N", help="reverse array order, in blocks of N bytes", type=int, action="store")
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
    add_bit = False
    if (type(pixel) == tuple):
        if (pixel == (0,0,0) or pixel==(0,0,0,255)):
            add_bit = True
    else:
        if (pixel == 0):
            add_bit = True

    if add_bit:
        number += 2**(4*width-n-1)
    n += 1
    if (n == 4*width):
        numbers.append(number)
        n = 0
        number = 0
    if (i == len(data)-1 and n != 0):
        print("({}) WARNING: image resolution is not a multiple of {}!".format(i,width))

        
if (args.reverse != None):
    # reverse array in blocks of size args.reverse
    numbers_reversed = []
    for i in range(0,len(numbers),args.reverse):
        l = []
        for j in range(args.reverse):
            l.append(numbers[i+j])
        numbers_reversed.append(l)
    numbers_reversed.reverse()
    numbers = [ number for sublist in numbers_reversed for number in sublist ]
        
array = "{ "
for i in range(len(numbers)):
    if ( i != len(numbers)-1 ):
        array += padded_hex(numbers[i],width,args.invert) + ", "
    else:
        array += padded_hex(numbers[i],width,args.invert)

array += " }"

print(array)


