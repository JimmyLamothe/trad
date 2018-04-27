"""
Convertit un XML FCP7 en .txt convertible en tableau dans Word avec Time Codes.

Prend trois arguments: input/NOMDUXML -  output/NOMDUTXT - TC
"""

from lxml import etree
import sys
import tc_calc

print('Ne pas oublier de vérifier que le TC est bon avant de travailler sur le document Word.\n')

filename = sys.argv[2]

input_file = sys.argv[1]

tc = "0"

try:
    tc = int(sys.argv[3])
except IndexError:
    print("Don't forget to enter Time Code (24 or 30)")
    sys.exit(0)

filename_txt = filename + '.txt'

tree = etree.parse(input_file)

root = tree.getroot()

sequence = root.find('sequence')

media = sequence.find('media')

video = media.find('video')

def get_track_list(video_or_audio):
    return(video_or_audio.findall('track'))

track_list = get_track_list(video)
    
v1 = track_list[0]

title_list = v1.findall('generatoritem')

with open(filename_txt, 'w') as txt_output:
    clip_list = []
    for title in title_list:
        start = int(title.find('start').text)
        end = int(title.find('end').text)
        effect = title.find('effect')
        parameter = effect.find('parameter')
        value = parameter.find('value').text
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

    for clip in sorted_clip_list:
        duration = clip[1] - clip[0]
        tc_in = tc_calc.tc_calc(clip[0], hour = 10, tc = tc)
        tc_out = tc_calc.tc_calc(clip[1], hour = 10, tc = tc)
        txt_output.write(tc_in)
        txt_output.write(';')
        txt_output.write(clip[2])
        txt_output.write('\n')
