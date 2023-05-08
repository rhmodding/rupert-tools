#!/bin/python3

import argparse
from pathlib import Path

parser = argparse.ArgumentParser("group.py",
                                 description="Make a group with the specified group ID")

parser.add_argument("group", help="Any music group. Sick Beat's gate group recommended")
parser.add_argument("index", help="SFX index to point to")
parser.add_argument("-o", "--output", help="File to save to",default="GROUP_WSD_NEW.bcgrp")

startingPoint = [0xD4, 0x600, 0xA4]
startIndex = 0x1000101
excludedIds = [
    0x100015B,
    0x100015C,
    0x100015D,
]
includedIds = [
    0x10001B0,
    0x10001B7,
]

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
            group.seek(0)
            with open(args.output, "w+b") as newGroup:
                #Dumping the old group in the new one
                newGroup.write(group.read())
                #Transforming the index if needed
                #This allows passing 1AB, 0x1AB or 0x10001AB as arguments
                if "x" in args.index:
                    index = args.index[2:]
                else:
                    index = args.index
                index = int(index, base=16)
                if index < 0x1000000:
                    index = index + 0x1000000
                for exclude in excludedIds:
                    if index > exclude:
                        index -= 1
                for include in includedIds:
                    if index > include:
                        index += 1
                offset = index - startIndex
                if offset < 0:
                    print("Invalid offset!")
                else:
                    #Writing 0x5C!
                    newGroup.seek(0)
                    newGroup.seek(0x5c)
                    newGroup.write((startingPoint[0]+offset).to_bytes(4, byteorder='little',signed=False))
                    #Writing 0x6C!
                    newGroup.seek(0)
                    newGroup.seek(0x6c)
                    newGroup.write((startingPoint[1]+offset).to_bytes(4, byteorder='little',signed=False))
                    #Writing 0xDC!
                    newGroup.seek(0)
                    newGroup.seek(0xdc)
                    newGroup.write((startingPoint[2]+offset).to_bytes(2, byteorder='little',signed=False))