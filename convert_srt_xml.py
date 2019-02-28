"""Takes a .srt list of subtitles and a .xml corresponding to a FCP-format
video sequence and creates a new FCP-format .xml with the same duration and
attributes as the original .xml file and  a single video track containing the
subtitles in the .srt file. It requires in the same location a a blank
FCP-format .xml file named "XML_VIDE.xml" and a second FCP-format .xml named
"XML_TITRE.xml" containing a single title for reference.

It takes three arguments and two optional arguments:

1. location of .srt file
2. location of .xml file
3. name of .xml file to be output (do not include .xml at end).

4. (optional) font type (must specify size as well)
5. (optional) font size (must specify type as well)
"""

import xml.etree.ElementTree as etree
import sys
import math
import uuid_generator
import tc_calc

input_srt = sys.argv[1] #.srt file containing subtitles

input_seq = sys.argv[2] #.xml FCP-format file containing input sequence.

input_name = sys.argv[3]

# default font type and size
font_type = "Arial"
font_size = "26"

if len(sys.argv) >= 5:
    font_type = sys.argv[4] 
    font_size = sys.argv[5]

# extract filename from full path to name sequence in FCP
slash_index = input_name.rfind('/')
print(slash_index)
print(slash_index >= 0)
if slash_index >= 0:
    filename = input_name + '.xml' #filename for .xml file.
    input_name = input_name[slash_index + 1:] # name for FCP sequence
else:
    filename = input_name + '.xml' #filename for .xml file.

#creation of trees from base sequences.

#blank XML
blank_tree = etree.parse('input/XML_VIDE.xml')

blank_root = blank_tree.getroot()

#single title XML
title_tree = etree.parse('input/XML_TITRE.xml')

title_root = title_tree.getroot()

def copy_tree(tree):
    return tree

#input sequence XML
input_tree = etree.parse(input_seq)

input_root = input_tree.getroot()

#output sequence XML
output_tree = copy_tree(title_tree)

output_root = output_tree.getroot()

# extraction of base v1 tracks for titles.
title_v1 = title_root[0][8][0][1]

output_v1 = output_root[0][8][0][1]

# extraction of a sample title
sample_title = title_v1[0]

def copy_title(title):
    return(title)

output_v1[1] = copy_title(sample_title)

# parsing of .srt file
srt_parsed = [] # contains 3-tuples:
                #(int(Frame IN)),(int(Frame OUT)),(str(Title Text))

with open(input_srt, 'r') as srt_source:
    lines = [line for line in srt_source]
    lines[0] = lines[0][1:] #bugfix: skip first char in file
    count = 0
    for i in range(len(lines)):
        #find title start using Time Codes
        if lines[i][13:16] == '-->':
            # Parse Time Codes
            hour_in = int(lines[i][0:2])
            min_in = int(lines[i][3:5])
            sec_in = int(lines[i][6:8])
            frame_in = math.floor(int(lines[i][9:12])/1000*24)
            hour_out = int(lines[i][17:19])
            min_out = int(lines[i][20:22])
            sec_out = int(lines[i][23:25])
            frame_out = math.floor(int(lines[i][26:29])/1000*24)
            TC_in = (hour_in, min_in, sec_in, frame_in)
            TC_out = (hour_out, min_out, sec_out, frame_out)
            duration_in = tc_calc.tc_calc(TC_in, reverse = True, tc=24)
            duration_out = tc_calc.tc_calc(TC_out, reverse = True, tc=24)
            # Parse Title Text
            if i+5 <= len(lines): # ensure in range
                if lines[i+4][13:16] == '-->': # if one line title
                    srt_parsed.append((duration_in, duration_out, lines[i+1]))
                else: # if two line title
                    srt_parsed.append((duration_in, duration_out,
                                       lines[i+1] + lines[i+2]))
            else: # if last title
                srt_parsed.append((duration_in, duration_out,
                                       lines[i+1] + lines[i+2]))

# change output xml values to match input sequence
output_root[0][0].text = uuid_generator.generate_uuid() #seq uuid

output_root[0][2].text = input_name #name

output_root[0][3].text = input_root[0][3].text #duration
output_root[0][4][0].text = input_root[0][4][0].text #rate/ntsc
output_root[0][4][1].text = input_root[0][4][1].text #timebase
output_root[0][5][0][0].text = input_root[0][5][0][0].text #timecode/ntsc
output_root[0][5][0][1].text = input_root[0][5][0][1].text #timebase
output_root[0][5][1].text = input_root[0][5][1].text #string
output_root[0][5][2].text = input_root[0][5][2].text #frame
output_root[0][5][3].text = input_root[0][5][3].text #source
output_root[0][5][4].text = input_root[0][5][4].text #displayformat
output_root[0][6].text = input_root[0][6].text #in
output_root[0][7].text = input_root[0][7].text #out
output_root[0][8][0][0][0][0].text = input_root[0][8][0][0][0][0].text #media/width
output_root[0][8][0][0][0][1].text = input_root[0][8][0][0][0][1].text #height
output_root[0][8][0][0][0][2].text = input_root[0][8][0][0][0][2].text #anamorphic
output_root[0][8][0][0][0][3].text = input_root[0][8][0][0][0][3].text #pixelaspectratio
output_root[0][8][0][0][0][4].text = input_root[0][8][0][0][0][4].text #fielddominance
output_root[0][8][0][0][0][5][0].text = input_root[0][8][0][0][0][5][0].text #ntsc
output_root[0][8][0][0][0][5][1].text = input_root[0][8][0][0][0][5][1].text #timebase
output_root[0][8][0][0][0][6].text = input_root[0][8][0][0][0][6].text #colordepth
output_root[0][8][0][0][0][7][0].text = input_root[0][8][0][0][0][7][0].text #codec/name
output_root[0][8][0][0][0][7][1][0].text = input_root[0][8][0][0][0][7][1][0].text #appspecificdata/appname 
output_root[0][8][0][0][0][7][1][1].text = input_root[0][8][0][0][0][7][1][1].text #appmanufacturer
output_root[0][8][0][0][0][7][1][2].text = input_root[0][8][0][0][0][7][1][2].text #appversion
output_root[0][8][0][0][0][7][1][3][0][0].text = input_root[0][8][0][0][0][7][1][3][0][0].text #qtcodec/codecname
output_root[0][8][0][0][0][7][1][3][0][1].text = input_root[0][8][0][0][0][7][1][3][0][1].text #codectypename
output_root[0][8][0][0][0][7][1][3][0][2].text = input_root[0][8][0][0][0][7][1][3][0][2].text #codectypecode
output_root[0][8][0][0][0][7][1][3][0][3].text = input_root[0][8][0][0][0][7][1][3][0][3].text #codecvendorcode
output_root[0][8][0][0][0][7][1][3][0][4].text = input_root[0][8][0][0][0][7][1][3][0][4].text #spatialquality
output_root[0][8][0][0][0][7][1][3][0][5].text = input_root[0][8][0][0][0][7][1][3][0][5].text #temporalquality
output_root[0][8][0][0][0][7][1][3][0][6].text = input_root[0][8][0][0][0][7][1][3][0][6].text #keyframerate
output_root[0][8][0][0][0][7][1][3][0][7].text = input_root[0][8][0][0][0][7][1][3][0][7].text #datarate
output_root[0][8][0][0][1][0].text = input_root[0][8][0][0][1][0].text #appspecificdata/appname
output_root[0][8][0][0][1][1].text = input_root[0][8][0][0][1][1].text #appmanufacturer
output_root[0][8][0][0][1][2].text = input_root[0][8][0][0][1][2].text #appversion
output_root[0][8][0][0][1][3][0][0].text = input_root[0][8][0][0][1][3][0][0].text #data/useyuv
output_root[0][8][0][0][1][3][0][1].text = input_root[0][8][0][0][1][3][0][1].text #usesuperwhite
output_root[0][8][0][0][1][3][0][2].text = input_root[0][8][0][0][1][3][0][2].text #rendermode

# integrate titles from .srt file
for child in output_v1:
    output_v1.remove(child) #clear sample titles

for child in output_v1:
    output_v1.remove(child) #necessary - not duplicate

for i in range(len(srt_parsed)):
    title_number = i
    child = etree.parse('input/XML_TITRE.xml').getroot()[0][8][0][1][0] #ugly but BUGFIX 
    # get variables from corresponding .srt title
    srt_in = srt_parsed[title_number][0]
    srt_out = srt_parsed[title_number][1]
    srt_text = srt_parsed[title_number][2]
    # add special symbol for line breaks - replace later with correct format
    if len(srt_text) > 44:
        half_index = int(len(srt_text)/2)
        break_index = srt_text[0:half_index].rfind(" ")
        srt_text = srt_text[0:break_index] + "BRK_LN" + srt_text[break_index + 1:]
        print(srt_text)
    # set variables from corresponding .srt title
    child.set("id","Référence sous-titre"+str(title_number))
    # set title TC IN and TC OUT
    child.find("in").text = "500"
    child.find("out").text = str(500 + srt_out - srt_in)
    child.find("start").text = str(srt_in)
    child.find("end").text = str(srt_out)
    # set title text
    effect = child.find("effect")
    effect[5][2].text = srt_text
    # set font type and size (default Arial 26)
    effect[6][2].text = font_type
    effect[7][4].text = font_size
    # set title uuids
    itemhistory = child.find("itemhistory")
    itemhistory[0].text = uuid_generator.generate_uuid()
    itemhistory[1].text = uuid_generator.generate_uuid()
    # add completed title to xml
    output_v1.append(child) 

# writing the final .xml file
output_tree.write(filename, encoding = 'UTF-8', xml_declaration = True)

# correcting bad line break formatting
filedata = None
with open(filename, 'r') as file :
  filedata = file.read()

filedata = filedata.replace('BRK_LN', '&#13;')

with open(filename, 'w') as file:
  file.write(filedata)

