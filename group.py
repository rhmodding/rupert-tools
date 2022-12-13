import argparse
from pathlib import Path

parser = argparse.ArgumentParser("group.py",
                                 description="Change a music group's index")

parser.add_argument("group", help="Any music group. Sick Beat's gate group recommended")
parser.add_argument("index", help="SFX index to point to")

startingPoint = [0x69, 0x3d0, 0x2f]
startIndex = 0x1000101

args = parser.parse_args()

if __name__ == '__main__':
    #Check for file
    if not Path(args.group).is_file():
        print("Not a file!")
        exit()
    with open(args.group, "r+b") as group:
        #Check for BCGRP
        magic = group.read(4)
        if magic != b'CGRP':
            print("Not a Megamix group!")
        else:
            #Transforming the index if needed
            #This allows passing 1AB, 0x1AB or 0x10001AB as arguments
            if "x" in args.index:
                index = args.index[2:]
            else:
                index = args.index
            index = int(index, base=16)
            if index < 0x1000000:
                index = index + 0x1000000
            offset = index - startIndex
            if offset < 0:
                print("Invalid offset!")
            else:
                #Writing 0x5C!
                group.seek(0)
                group.seek(0x5c)
                group.write((startingPoint[0]+offset).to_bytes(32, byteorder='little',signed=False))
                #Writing 0x6C!
                group.seek(0)
                group.seek(0x6c)
                group.write((startingPoint[1]+offset).to_bytes(32, byteorder='little',signed=False))
                #Writing 0xDC!
                group.seek(0)
                group.seek(0xdc)
                group.write((startingPoint[2]+offset).to_bytes(32, byteorder='little',signed=False))