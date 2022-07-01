#!/usr/bin/env python3

"""
Convertit un XML FCP7 en .txt convertible en tableau dans Word avec Time Codes
et identifications de personnages. Prend deux pistes vidéo.

Modifier le nom du personnage de la V1 dans le programme directement.

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

filename_txt = input_file[:-4] + '.txt'

tree = etree.parse(input_file)

root = tree.getroot()

sequence = root.find('sequence')

media = sequence.find('media')

video = media.find('video')

def get_track_list(video_or_audio):
    return(video_or_audio.findall('track'))

track_list = get_track_list(video)
    
v1 = track_list[0]

title_list_v1 = v1.findall('generatoritem')

v2 = track_list[1]

title_list_v2 = v2.findall('generatoritem')

with open(filename_txt, 'w') as txt_output:
    clip_list = []
    name = input("Entrez le nom de l'invité ou l'animateur.\n")
    number = "ST-1"
    for title in title_list_v1:
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
        clip_list.append((start, end, number, name, text))
    name = input("Tapez le nom de l'intervenant principal, s'il y en a un.\n")
    if not name:
        name = "Nom"
    number = "1"
    for title in title_list_v2:
        start = int(title.find('start').text)
        end = int(title.find('end').text)
        effect = title.find('effect')
        parameter = effect.find('parameter')
        value = parameter.find('value').text
        text = ""
        previous_letter = ""
        letter_count = 0
        if not value:
            continue
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
        clip_list.append((start, end, number, name, text))
    sorted_clip_list = sorted(clip_list, key = lambda clip: clip[0])
    #short_clip_list serves to combine subtitles when the same person is talking for a long time.
    short_clip_list = []
    current_start = 0
    current_end = 0
    current_number = "0"
    current_name = ""
    current_text = ""
    for clip in sorted_clip_list:
        #TESTING: For manual breaks, using "*" to indicate new block start
        if clip[4][0] == '*':
            clip = list(clip)
            clip[4] = clip[4][1:] #remove block start indicator
            clip = tuple(clip)
            short_clip_list.append((current_start, current_end, current_number,
                                    current_name, current_text))
            current_start = clip[0]
            current_text=""
        elif clip[0] -  current_end > 60 or clip[3] != current_name:
            short_clip_list.append((current_start, current_end, current_number,
                                    current_name, current_text))
            current_start = clip[0]
            current_text=""
        current_end = clip[1]
        current_number = clip[2]
        current_name = clip[3]
        if current_text:
            current_text += " "
        current_text += clip[4]
    #To catch last title
    if current_text:
        short_clip_list.append((current_start, current_end, current_number,
                                    current_name, current_text))
    for clip in short_clip_list[1:]:
        duration = clip[1] - clip[0]
        tc_in = tc_calc.tc_calc(clip[0], hour = 10, tc = tc)
        tc_out = tc_calc.tc_calc(clip[1], hour = 10, tc = tc)
        if duration < 150:
            txt_output.write(tc_in)
        else:
            txt_output.write(tc_in + " à " + tc_out)
        txt_output.write(';')
        txt_output.write(clip[2])
        txt_output.write(';')
        txt_output.write(clip[3])
        txt_output.write(';')
        if value[0] in ['\n','\r','\r\n']:
            txt_output.write(clip[4])
            txt_output.write('\n')
        else:
            txt_output.write(clip[4])
            txt_output.write('\n')
