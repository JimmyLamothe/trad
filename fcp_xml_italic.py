"""
Converts FCP7 title XML to all italics to prevent Premiere bug.
Converts Font size to 30 for Ocean.
OPTIONAL: Output given font size

Usage: python3 fcp_xml_italic.py input/XMLNAME

Adds _Italic to output file name.
"""

import xml.etree.ElementTree as etree
import sys

#Establish correct input and output file names
input = sys.argv[1]

font_size = "30"

slash_index = input.index('/')

filename = input[slash_index + 1 : -4]

italic = "_italic.xml"

output = "output/" + filename + italic


#Parse XML tree to extract V1 files (titles)

tree = etree.parse(input)

root = tree.getroot()

v1 = root[0][8][0][1]

v1_content = [clip for clip in v1]

clips_v1 = v1_content[:-2]

for clip in clips_v1:
    try:
        clip[14][8][5].text = "3"
    except IndexError:
        clip[13][8][5].text = "3"

# writing the final .xml file
tree.write(output, encoding = 'UTF-8', xml_declaration = True)
