"""
Convertit un XML FCP7 en .srt.

Prend deux arguments: input/NOMDUXML - TC
"""

from lxml import etree
import sys
import tc_calc

print('Ne pas oublier de vérifier que le TC est bon avant de travailler sur le document Word.\n')

input_file = sys.argv[1]

tc = "0"

try:
    tc = int(sys.argv[2])
except IndexError:
    print("Don't forget to enter Time Code (24 or 30)")
    sys.exit(0)

filename_srt = input_file[:-4] + '.srt'

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

with open(filename_srt, 'w') as srt_output:
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
