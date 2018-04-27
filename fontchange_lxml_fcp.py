"""
Converts FCP7 title XML to all italics to prevent Premiere bug.
Converts Font size to 34 for Ocean.
OPTIONAL: Output given font size

Usage: python3 fcp_xml_italic.py input/XMLNAME [asks for font type and font size]

Changes output filename according to input parameters..
"""

from lxml import etree
import sys

#Establish correct input and output file names
input_filename = sys.argv[1]

font_size = "30"

font_size_input = input("Type required font size or RETURN for default value")

if font_size_input:
    font_size = font_size_input

font_name = ""

font_name_input = input("Type required font name or RETURN for default value")

if font_name_input:
    font_name = font_name_input

italic_bool = True

italic_input = input("Type anything to cancel italic conversion. RETURN for italic.")

if italic_input:
    italic_bool = False

slash_index = input_filename.index('/')

filename = input_filename[slash_index + 1 : -4]

italic = "_italic"

output = "output/" + filename

if font_name:
    output += "_"
    output += font_name

if font_size_input:
    output += "_"
    output += font_size

if italic_bool:
    output += italic

output += ".xml"

#Parse XML tree to extract V1 files (titles)

tree = etree.parse(input_filename)

root = tree.getroot()

v1 = root[0][8][0][1]

v1_content = [clip for clip in v1]

clips_v1 = v1_content[:-2]

for clip in clips_v1:
    try:
        if font_name:
            clip[14][6][2].text = font_name
        clip[14][7][4].text = font_size
        if italic_bool:
            clip[14][8][5].text = "3"
    except IndexError:
        if font_name:
            clip[14][6][2].text = font_name
        clip[13][7][4].text = font_size
        if italic_bool:
            clip[13][8][5].text = "3"

# writing the final .xml file
tree.write(output, encoding = 'UTF-8', xml_declaration = True)
