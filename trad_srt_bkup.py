"""
Convertit un XML FCP7 en .srt

Prend trois arguments: input/NOMDUXML -  output/NOMDUTXT - TC
"""

import xml.etree.ElementTree as etree
import sys
import tc_calc

print('Ne pas oublier de vérifier que le TC est bon avant de travailler sur le document Word.\n')

filename = sys.argv[2]

input_file = sys.argv[1]

intervenants = True

tc = "0"

try:
    tc = int(sys.argv[3])
except IndexError:
    print("Don't forget to enter Time Code (24 or 30)")
    sys.exit(0)
"""
if(len(sys.argv) == 5):
    with open(sys.argv[4], 'r') as liste_intervenants:
        for intervenant in liste_intervenants:
            intervenants.append(intervenant)

text_only = False
if(len(sys.argv) > 3):
    if(sys.argv[3] == "text_only"):
        text_only = True
    elif(int(sys.argv[3]) > 0):
        tc = int(sys.argv[3])
"""
final = False

filename_srt = filename + '.srt'

tree = etree.parse(input_file)

root = tree.getroot()

v1 = root[0][8][0][1]

v2 = root[0][8][0][2]

v1_content = [clip for clip in v1]

clips_v1 = v1_content[:-2]

if(intervenants):
    with open(filename_srt, 'w', encoding="utf-8") as srt_output:
        clip_list = []
        for clip in clips_v1:
            start = int(clip[5].text)
            end = int(clip[6].text)
            try:
                value = clip[14][5][2].text
            except IndexError:
                value = clip[13][5][2].text
            text = ""
            previous_letter = ""
            letter_count = 0
            for letter in value:
                if letter in ['\n','\r','\n\r','\r\n']:
                    if letter_count == 0:
                        pass
                    else:
                        text += " "
                elif letter == "-" and letter_count in [0,1,2]:
                    pass
                elif previous_letter == "-" and letter_count in [1,2,3]:
                    pass
                else:
                    text += letter
                previous_letter = letter
                letter_count += 1
            clip_list.append((start, end, text))
        sorted_clip_list = sorted(clip_list, key = lambda clip: clip[0])
        
        count = 0
        for clip in sorted_clip_list:
            count += 1
            duration = clip[1] - clip[0]
            tc_in_base = tc_calc.tc_calc(clip[0], hour = 10, tc = tc)
            tc_in_start = tc_in_base[0:8]
            tc_in_frames = tc_in_base[9:]
            tc_in_milliseconds_base = float(tc_in_frames) / tc
            tc_in_milliseconds = "{0:.3f}".format(tc_in_milliseconds_base)[2:5]
            tc_in = tc_in_start + ',' + tc_in_milliseconds
            tc_out_base = tc_calc.tc_calc(clip[1], hour = 10, tc = tc)
            tc_out_start = tc_out_base[0:8]
            tc_out_frames = tc_out_base[9:]
            tc_out_milliseconds_base = float(tc_out_frames) / tc
            tc_out_milliseconds = "{0:.3f}".format(tc_out_milliseconds_base)[2:5]
            tc_out = tc_out_start + ',' + tc_out_milliseconds
            srt_output.write(str(count))
            srt_output.write('\n')
            srt_output.write(tc_in)
            srt_output.write(' --> ')
            srt_output.write(tc_out)
            srt_output.write('\n')
            srt_output.write(clip[2])
            srt_output.write('\n')
            srt_output.write('\n')
