#Developed by TheAlternateDoctor
#With help from patataofcourse, Cebola
import argparse
from pathlib import Path
import re
import os
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser("diff.py",
                                 description="Create an xmsbt file that includes the differences between an "
                                             "original and an edited file")

parser.add_argument("original", help="Original, unmodified xmsbt file (or folder)")
parser.add_argument("edited", help="xmsbt file(s) that contains modifications over the original (or folder)", nargs='*')

args = parser.parse_args()

if __name__ == '__main__':
    if Path(args.original).is_dir():
        path = args.original
        epaths = args.edited
        directoryMode = True
    else:
        baseFiles = [args.original]
        editedFiles = [args.edited[0]]
        path = ""
        epaths = [""]
        directoryMode = False
    edited = {}
    for epath in epaths:
        if directoryMode:
            baseFiles = [x.name for x in Path(path).iterdir() if x.is_file()]
            editedFiles = [x.name for x in Path(epath).iterdir() if x.is_file()]
        for index, xmsbt in enumerate(baseFiles):
            if xmsbt.endswith('.xmsbt'):  # Ignore files that don't end with extension .xmsbt
                if xmsbt in editedFiles or not directoryMode:  # If directory, ignore any files that are not in boths dirs
                    print("Diffing " + xmsbt + "... ", end="")

                    if not directoryMode:
                        exmsbt = editedFiles[0]
                    else:
                        exmsbt = editedFiles[editedFiles.index(xmsbt)]

                    with open(Path(path).joinpath(xmsbt), encoding="utf-16") as xFile:
                        baseFile = xFile.read()

                    for m in re.finditer(r"&#x[0-9A-F]+;", baseFile):
                        baseFile = baseFile[:m.start()] + "µ" + baseFile[m.start() + 1:]

                    with open(Path(epath).joinpath(exmsbt), encoding="utf-16") as xFile:
                        editFile = xFile.read()

                    for m in re.finditer("&#x[0-9A-F]+;", editFile):
                        editFile = editFile[:m.start()] + "µ" + editFile[m.start() + 1:]

                    base = ET.fromstring(baseFile)
                    edit = ET.fromstring(editFile)
                    if xmsbt in edited:
                        print("Exists!\n")
                        diff = edited[xmsbt]
                    else:
                        diff = ET.Element('xmsbt')
                    for editedTag in edit:
                        existing = False
                        for baseTag in base:
                            if baseTag.attrib == editedTag.attrib:
                                existing = True
                                if baseTag[0].text != editedTag[0].text:
                                    print("\n---------- Not the same! ----------")
                                    print(f"{Path(path).joinpath(xmsbt)}: {baseTag[0].text}")
                                    print(f"{Path(epath).joinpath(exmsbt)}: {editedTag[0].text}")
                                    diff.append(editedTag)
                                    edited[xmsbt] = diff
                        if not existing:
                            print("\n---------- Doesn't exist! ----------")
                            print(f"{Path(epath).joinpath(exmsbt)}: \"{editedTag[0].text}\" ({editedTag.attrib['label']})")
                            diff.append(editedTag)
                            edited[xmsbt] = diff
    for xmsbt, diff in edited.items():
        if diff != False: #Only write to file if there's anything changed
            if directoryMode:
                endPath = "out"
            else:
                endPath = ""
            xmsbt = os.path.basename(xmsbt)
            final = ET.ElementTree(diff)
            if not Path(endPath).exists():
                Path(endPath).mkdir(parents=True, exist_ok=True)
            final.write(Path(endPath).joinpath(xmsbt), encoding="utf-16")
            with open(Path(endPath).joinpath(xmsbt),'r', encoding="utf-16") as xFile:
                outFile = xFile.read()
            for m in re.finditer("µ#x[0-9A-F]+;", outFile):
                outFile = outFile[:m.start()] + "&" + outFile[m.start() + 1:]
            with open(Path(endPath).joinpath(xmsbt),'w', encoding="utf-16") as xFile:
                xFile.write(outFile)
            print("Done!")
