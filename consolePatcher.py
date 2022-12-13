#Developped by patataofcourse
#Revised by TheAlternateDoctor
import argparse

parser = argparse.ArgumentParser("consolePatcher.py",
                                 description="Changes a specific slot's console in the Museum")

parser.add_argument("input", help="Original base.bin.")
parser.add_argument("index", help="Index of the game to change.")
parser.add_argument("console", help="Console to change to (0:GBA, 1:DS, 2:Wii, 3:3DS)")
parser.add_argument("-o", "--output", help="File to save the edited base.bin to", default="edited.bin", required=False)

args = parser.parse_args()

base = bytearray(open(args.input, "rb").read())

out = open(args.output, "wb")

if "x" in args.index:
    index = args.index[2:]
else:
    index = args.index
index = int(index, base=16)

console = int(args.console).to_bytes(4, "little")


if index >= 0x100:

    index -= 0x100

    for i in range(4):

        base[0x3358 + index*0x24  + i] = console[i]

else:

    for i in range(4):

        base[index*0x34  + i] = console[i]


out.write(base)

out.close()