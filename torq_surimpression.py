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

tc = 0

hour = 0


try:
    tc = int(sys.argv[2])
except IndexError:
    print("Don't forget to enter Time Code (24 or 30)")
    sys.exit(0)

try:
    hour = int(sys.argv[3])
except IndexError:
    print("Don't forget to enter TC hour (0 or 10)")

    
filename_txt = input_file[:-4] + '.txt'

tree = etree.parse(input_file)

root = tree.getroot()

sequence = root.find('sequence')

media = sequence.find('media')

video = media.find('video')

def get_track_list(video_or_audio):
    return(video_or_audio.findall('track'))

track_list = get_track_list(video)
    
v1 = track_list[1]

title_list_v1 = v1.findall('clipitem')

v2 = track_list[0]

title_list_v2 = v2.findall('clipitem')

with open(filename_txt, 'w') as txt_output:
    clip_list = []
    name = input("Entrez le nom de l'intervenant principal ou laissez vide s'il n'y en a pas.\n")
    main_character = name
    number = "1"
    title_list = title_list_v1 + title_list_v2
    i = 0
    for title in title_list:
        i += 1
        if i == len(title_list_v1): #When we reach title_list_v2
            name = input("Entrez le nom de l'invité vedette ou l'animateur.\n")
            number = 'ST-1'
        filter_list = title.findall('filter')
        value = ""
        line = 1
        for filter in filter_list:
            if line > 1:
                value += '\n'
            effect = filter.find('effect')
            if effect.find('name').text == None:
                print('Title failed - No value')
                continue
            else:
                value += effect.find('name').text
                line +=1
        text = ""
        previous_letter = ""
        letter_count = 0
        if not value:
            continue
        value = value.replace('&amp;#13;', '\n')
        for letter in value:
            if letter in ['\n','\r','\n\r','\r\n']:
                if letter_count == 0:
                    pass
                else: 
                    text += " "
            else:
                text += letter
            previous_letter = letter
            letter_count += 1
        #print('Title: ' + value.replace('\r', '\n'))
        start = int(title.find('start').text)
        end = int(title.find('end').text)
        clip_list.append((start, end, number, name, text))
    sorted_clip_list = sorted(clip_list, key = lambda clip: clip[0])
    short_clip_list = [] #serves to combine subtitles when the same person is talking for a long time.
    current_start = 0
    current_end = 0
    current_number = "0"
    current_name = ""
    current_text = ""
    name_list = {}
    for index, clip in enumerate(sorted_clip_list):
        clip_start = clip[0]
        clip_end = clip[1]
        clip_number = clip[2] #Ignored in this version for now
        clip_name = clip[3] #Temp value in this version for now
        clip_text = clip[4]
        #TESTING: For manual breaks, using "*1" to indicate new block start + character number
        if clip_text[0] == '*':
            clip_text = clip_text[clip_text.find(' ') + 1:]
            short_clip_list.append((current_start, current_end, current_number,
                                    current_name, current_text))
            current_start = clip_start
            current_text=""
        elif clip_start -  current_end > 36 or clip_name != current_name or clip_number[0:2] == 'ST':
            short_clip_list.append((current_start, current_end, current_number,
                                    current_name, current_text))
            current_start = clip_start
            current_text=""
        current_end = clip_end
        current_number = clip_number
        current_name = clip_name
        if current_text:
            current_text += " "
        current_text += clip_text
    #To catch last title
    if current_text:
        short_clip_list.append((current_start, current_end, current_number,
                                    current_name, current_text))
    with open('input/EMDM3_GHANA_COUNT.txt', 'w') as count_output:
        for clip in short_clip_list[1:]:
            duration = clip[1] - clip[0]
            tc_in_base = tc_calc.tc_calc(clip[0], hour=hour, tc=tc, srt=True)
            tc_in_start = tc_in_base[0:8]
            tc_in_frames = tc_in_base[9:]
            tc_in_milliseconds_base = float(tc_in_frames) / tc
            tc_in_milliseconds = "{0:.3f}".format(tc_in_milliseconds_base)[2:5]
            tc_in = tc_in_start + ',' + tc_in_milliseconds
            tc_out_base = tc_calc.tc_calc(clip[1], hour=hour, tc=tc, srt=True)
            tc_out_start = tc_out_base[0:8]
            tc_out_frames = tc_out_base[9:]
            tc_out_milliseconds_base = float(tc_out_frames) / tc
            tc_out_milliseconds = "{0:.3f}".format(tc_out_milliseconds_base)[2:5]
            tc_out = tc_out_start + ',' + tc_out_milliseconds
            txt_output.write(tc_in)
            txt_output.write(' --> ')
            txt_output.write(tc_out)
            txt_output.write(' - ')
            txt_output.write(f'{max(1, int(duration / tc))} sec')
            txt_output.write('\n')
            txt_output.write(clip[3])
            txt_output.write('\n')
            txt_output.write(clip[4])
            txt_output.write('\n')
            txt_output.write('\n')
            count_output.write(clip[4])
            count_output.write('\n')
        
        
"""        
    for clip in short_clip_list[1:]:
        duration = clip[1] - clip[0]
        tc_in = tc_calc.tc_calc(clip[0], hour = 10, tc = tc)
        tc_out = tc_calc.tc_calc(clip[1], hour = 10, tc = tc)
        if duration < 300:
            txt_output.write(tc_in)
        else:
            txt_output.write(tc_in + " à " + tc_out)
        txt_output.write(';')
        txt_output.write(clip[2])
        txt_output.write(';')
        txt_output.write(clip[3])
        txt_output.write(';')
        txt_output.write(clip[4])
        txt_output.write('\n')
"""




#FOR CHARACTER IDENTIFICATION - FIX LATER

"""
            if not index == 1: #If not very first clip (no current clip)
                short_clip_list.append((current_start, current_end, current_number,
                                        current_name, current_text))
                current_name = ""
                current_text = ""
            character_number = clip_text[1:clip_text.find(' ')]
            clip_text = clip_text[clip_text.find(' '):] #remove block start indicator
            try:
                current_name = name_list[character_number]
            except KeyError:
                current_name = input(f'Type name for character {character_number} or type ENTER for main\n')
                if not current_name:
                    current_name = main_character
                else:
                    name_list[character_number] = current_name
                current_start = clip_start
                current_text = clip_text
"""