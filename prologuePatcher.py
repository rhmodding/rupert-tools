#Developed by patataofcourse
#Revised by TheAlternateDoctor
import argparse

parser = argparse.ArgumentParser("prologuePatcher.py",
                                 description="Changes a specific slot's prologue music")

parser.add_argument("input", help="Original base.bin.")
parser.add_argument("index", help="Index of the game to change.")
parser.add_argument("sfx", help="Index of the SFX you want as prologue music.")
parser.add_argument("-o", "--output", help="File to save the edited base.bin to.", default="edited.bin", required=False)

args = parser.parse_args()

base = bytearray(open(args.input, "rb").read())

out = open(args.output, "wb")

if "x" in args.index:
    index = args.index[2:]
else:
    index = args.index
index = int(index, base=16)

if "x" in args.sfx:
    sfx = args.sfx[2:]
else:
    sfx = args.sfx
sfx = int(sfx, base=16).to_bytes(4, "little")

if index >= 0x100:
    index -= 0x100
    for i in range(4):
        base[0x3358 + index*0x24 + 0x1c + i] = sfx[i]
else:
    for i in range(4):
        base[index*0x34 + 0x28 + i] = sfx[i]

out.write(base)
out.close()
