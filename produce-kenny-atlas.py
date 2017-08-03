#!/usr/bin/python

"""
	see here for an example of what an atlas should look like
	https://github.com/photonstorm/phaser-examples/blob/master/examples/assets/buttons/button_texture_atlas.json

	usage produce-kenny-atlas.py -i <xml file> -p <png file>
"""

import sys, json, argparse, os, io

try:
    to_unicode = unicode
except NameError:
    to_unicode = str

parser = argparse.ArgumentParser()
parser.add_argument("-i", required=True)
parser.add_argument("-p", required=True)
args = parser.parse_args()

# input xml found in kenny sprite sheet directory
inputxml_filename = args.i

# input png file found in kenny sprite sheet png
inputimage_filename = args.p

# one outside dependency GRRRR
from PIL import Image
img = Image.open(inputimage_filename)
(image_w,image_h) = img.size

real_input_image_filename = os.path.split(inputimage_filename)[-1]
filename_without_ext = os.path.splitext(inputimage_filename)[0]

o = {}
o["frames"] = {}
o["meta"] = {
	"app" : "Adobe Flash CS6", # feel freeeee to change this
	"version" : "1.0",
	"image" : real_input_image_filename,
	"size" : { "w" : image_w, "h" : image_h }
}

import xml.etree.ElementTree as ET
tree = ET.parse(args.i)
root = tree.getroot()
for child in root:
	if child.tag == "SubTexture":
		tmp = {}
		tmp["frame"] = { 
			"x" : int(child.attrib["x"]),
			"y" : int(child.attrib["y"]),
			"w" : int(child.attrib["width"]), 
			"h" : int(child.attrib["height"]) 
			}
		tmp["rotated"] = False
		tmp["trimmed"] = False
		tmp["spriteSourceSize"] = tmp["frame"]
		tmp["sourceSize"] = { "w" : int(child.attrib["width"]), "h" : int(child.attrib["height"]) }
		tmp["pivot"] = { "x" : 0.5, "y" : 0.5 }
		o["frames"][child.attrib["name"]] = tmp;

output_json = json.dumps(o, ensure_ascii=False)

with io.open(filename_without_ext + ".json", 'w', encoding='utf-8') as outfile:
	outfile.write(to_unicode(output_json));

print(output_json)
