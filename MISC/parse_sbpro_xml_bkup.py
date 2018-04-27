"""
Converts SBPRO XML audio at 24 fps to FCP compatible XML audio at 23.98fps.
Input: XML file to convert to 23.98.
Output: Converted XML file.
Typical Usage: python3 parse_sbpro_xml.py input.xml output.xml
"""

import xml.etree.ElementTree as etree
import sys
import math

input = sys.argv[1]

output = sys.argv[2]

tree = etree.parse(input)

root = tree.getroot()

sequence = root[0]

audio = root[0][8][1]

sequence[4][1].text = "23.98"
sequence[5][0][1].text = "23.98"
sequence[8][0][0][0][4][1].text = "23.98"


duration_unchanged = True #for debugging use only

# for child in audio: #Possibly not needed, might start on following line.
for track in audio:
    for clip in track:
        tc_in = float(clip[3].text)
        tc_out = float(clip[4].text) 
        tc_start = float(clip[5].text)
        tc_end = float(clip[6].text)
        duration = tc_out - tc_in
        print("old tc_in: " + str(tc_in))  #for debugging use only
        tc_in = int(math.ceil(0.9991666 * tc_in))
        print("new tc_in: " + str(tc_in)) #for debugging use only
        clip[3].text = str(tc_in)
        print("old tc_out: " + str(tc_out)) #for debugging use only
        tc_out = int(tc_in + duration)
        print("new tc_out: " + str(tc_out)) #for debugging use only
        clip[4].text = str(tc_out)
        if (duration != tc_out - tc_in):  #for debugging use only
            duration_unchanged = False
        print("old tc_start: " + str(tc_start))  #for debugging use only
        tc_start = int(math.ceil(1.0001 * tc_start))
        print("old tc_start: " + str(tc_start))  #for debugging use only
        clip[5].text = str(tc_start)
        print("new tc_start: " + str(tc_start))  #for debugging use only
        print("old tc_end: " + str(tc_end))  #for debugging use only
        tc_end = int(tc_start + duration)
        clip[6].text = str(tc_end)
        print("new tc_end: " + str(tc_end))  #for debugging use only
if duration_unchanged:  #for debugging use only
    print("duration unchanged")
print("output to: " + output)
tree.write(output)
