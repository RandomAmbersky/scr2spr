import os
import argparse
import sys
from array import array


def xytoaddr(xcoord, ycoord):
    return ((ycoord & 0x18) << 8) | ((ycoord & 7) << 5) | (xcoord & 31)


def nextline(someaddr):
    if someaddr & 0x700 != 0x700:
        someaddr += 0x100
    elif someaddr & 0xe0 == 0xe0:
            someaddr += 0x20
    else:
        someaddr -= 0x6e0
    return someaddr


def binary2array(nameoffile):
    data = array('B')
    with open(nameoffile, 'rb') as f:
        data.fromfile(f, os.stat(nameoffile).st_size)
    return data


def savebin2file(perem, nameoffile):
    f = open(nameoffile, 'w+b')
    f.write(bytearray(perem))
    f.close()


def takeonesprite(temp_x, temp_y, temp_w, temp_h):
    k = bytearray()
    offset = xytoaddr(temp_x, temp_y)
    for l in range(temp_h * 8):
        k += a[offset:offset + temp_w]
        offset = nextline(offset)
    return k


def createparser():
    myparser = argparse.ArgumentParser()
    myparser.add_argument('-x', '--x', default=0, type=int)
    myparser.add_argument('-y', '--y', default=0, type=int)
    myparser.add_argument('-wide', '--width', type=int)
    myparser.add_argument('-high', '--height', type=int)
    myparser.add_argument('-c', '--count', default=1, type=int)
    myparser.add_argument('-i', '--input', type=str)
    myparser.add_argument('-o', '--output', default='sprite.bin', type=str)
    return myparser


parser = createparser()
namespace = parser.parse_args(sys.argv[1:])
x = namespace.x
y = namespace.y
count = namespace.count
width = namespace.width
height = namespace.height

if width == None or height == None:
    print("Please set length and height of sprite(s)")
    exit(0)

if 32/width*24/height < count:
    print("You want too many sprites....")
    exit(0)

d = bytearray()

a = binary2array(namespace.input)

if len(a) != 6144 | len(a) != 6912:
    print("Strange size of input file. 6144 or 6912 only!")
    exit(0)
for j in range(count):
    d += takeonesprite(x, y, width, height)
    if x + width < 31:
        x += width
    else:
        x = 0
        y += height
        if j != count & y > 23:
            print("The screen is end :(")
            exit(0)

savebin2file(d, namespace.output)
