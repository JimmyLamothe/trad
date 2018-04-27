"""Takes a .srt list of subtitles and converts it to AVID DS compatible .txt file.

It takes one argument and two optional argument:

1. location of .srt file

(optional)
    2. True -  if you want to force start time code hour from 0 to 10 (default False). 
    3. 30 - if you want 30 frames per second (default 24)

"""

#import xml.etree.ElementTree as etree
import sys
import math
#import uuid_generator
#import tc_calc

input = sys.argv[1] #.srt file containing subtitles

try:
    if sys.argv[2] == "True":
        force_ten = True
    else:
        force_ten = False

except IndexError:
    force_ten = False

try:
    if sys.argv[3] == "30":
        fps = 30
    else:
        fps = 24

except IndexError:
    fps = 24
    
    
# remove .srt from full path and create output file as .txt
dot_index = input.rfind('.')
output = "default.txt" #default filename for .txt file
try:
    output = input[:dot_index] + '.txt' #filename for .txt file.
except IndexError:
    pass

# parsing of .srt file
srt_parsed = [] # contains 3-tuples:
                #(str(TC IN)),(str(TC OUT)),(str(Title Text))

with open(input, 'r') as srt:
    lines = [line for line in srt]
    lines[0] = lines[0][1:] #bugfix: skip first char in file
    count = 0
    for i in range(len(lines)):
        #find title start using Time Codes
        if lines[i][13:16] == '-->':
            # Parse Time Codes
            # Convert milliseconds to frames
            int_frame_in = math.floor(int(lines[i][9:12])/1000*fps)
            int_frame_out = math.floor(int(lines[i][26:29])/1000*fps)
            # Convert to string and add initial 0 if under 10.
            str_frame_in = str(int_frame_in)
            str_frame_out = str(int_frame_out)
            if int_frame_in < 10:
                str_frame_in = "0" + str_frame_in
            if int_frame_out < 10:
                str_frame_out = "0" + str_frame_out
            frame_in = ":" + str_frame_in
            frame_out = ":" + str_frame_out
            if force_ten:
                TC_IN = "10" + lines[i][2:8] + frame_in + " "
                TC_OUT = "10" + lines[i][19:25] + frame_out + "\n"
            else:
                TC_IN = lines[i][0:12] + " "
                TC_OUT = lines[i][17:29] + "\n"
            # Parse Title Text
            if i+5 <= len(lines): # ensure in range
                if lines[i+4][13:16] == '-->': # if one line title
                    srt_parsed.append((TC_IN, TC_OUT, lines[i+1] + "\n"))
                else: # if two line title
                    srt_parsed.append((TC_IN, TC_OUT,
                                       lines[i+1] + lines[i+2] + "\n"))
            else: # if last title
                srt_parsed.append((TC_IN, TC_OUT,
                                       lines[i+1] + lines[i+2] + "\n"))


# writing the final .txt file
with open(output, 'w') as final:
    text = "<begin subtitles>\n\n"
    for i in range(len(srt_parsed)):
        # get variables from corresponding .srt title
        srt_in = srt_parsed[i][0]
        srt_out = srt_parsed[i][1]
        srt_text = srt_parsed[i][2]
        """
        # add special symbol for line breaks - replace later with correct format
        if len(srt_text) > 44:
            half_index = int(len(srt_text)/2)
            break_index = srt_text[0:half_index].rfind(" ")
            srt_text = srt_text[0:break_index] + "BRK_LN" + srt_text[break_index + 1:]
            print(srt_text)
        """
        # write title TC IN, TC OUT
        text += srt_in
        text += srt_out
        # write title text
        text += srt_text
    text += "<end subtitles>"
    final.write(text)
   



"""
# correcting bad line break formatting
filedata = None
with open(filename, 'r') as file :
  filedata = file.read()

filedata = filedata.replace('BRK_LN', '&#13;')

with open(filename, 'w') as file:
  file.write(filedata)
"""
