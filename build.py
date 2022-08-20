toCopy = (
    "index.html",
    "nav_bg.png",
    "uni_sans.otf",
    "calibril.ttf"
)

import shutil
import os

shutil.rmtree("out")
os.makedirs("out")


for file in toCopy:
    shutil.copyfile(f"src/{file}", f"out/{file}")

import buildRules
