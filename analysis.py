#!/usr/bin/env python3

"""
Sert à créer un dictionnaire à partir d'un XML Adobe Premiere.

Prend deux pistes vidéo: V1 = Sous-titres / V2 = Surimpression

"""

from lxml import etree
import tc_calc

def get_track_list(video_or_audio):
    return(video_or_audio.findall('track'))

def create_char_dict(number):
    """ Returns character dict with name for each character number """
    char_dict = {}
    confirmed = False
    while not confirmed:
        name = input(f'Type name for character {number}:')
        print('Press Return to confirm or anything else to try again:')
        print(f'{number}: {name}')
        confirmed = input()
        if not confirmed:
            confirmed = True #Yes I know this is stupid but it's simple and works
        else:
            confirmed = False
    char_dict['name'] = name

def get_title_value(title):
    """ Gets the value of a title """
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
    return value
    
def analyze_title(title, character_dict):
    """ Returns the text, start and end times of a title """
    value = get_title_value(title)
    if not value:
        raise ValueError('Empty title')
    value = value.replace('&amp;#13;', '\n')
    text = ""
    previous_letter = ""
    letter_count = 0
    for letter in value:
        if letter_count
        if letter in ['\n','\r','\n\r','\r\n']:
            if letter_count == 0:
                pass
            else: 
                text += " "
        else:
            text += letter
        previous_letter = letter
        letter_count += 1
    start = int(title.find('start').text)
    end = int(title.find('end').text)
    return {'start': start,
            'end': end,
            'text': text)

def get title_list(track_list, subtitles=False):
    """ Gets list of title dicts from a video track """
    title_list = []
    i = 0
    for title in track_list:
        i += 1
        title_dict = analyze_title(title)
        title_dict['ST'] = subtitles
        title_list.append(title_dict)

def add_names(title_list, chara):
    """ Adds a 'name' key to a title_dict and updates the character_list """
        
def dict_from_xml(input_file, tc, hour):
    output_file = input_file[:-4] + '.txt'
    tree = etree.parse(input_file)
    root = tree.getroot()
    sequence = root.find('sequence')
    media = sequence.find('media')
    video = media.find('video')
    track_list = get_track_list(video)
    v1 = track_list[0]
    titles_v1 = v1.findall('clipitem')
    v2 = track_list[1]
    titles_v2 = v2.findall('clipitem')
    character_dict = {}
    full_title_dict = {}
    full_title_list = []
    title_list_v1 = get_title_list(titles_v1, subtitles=True)
    title_list_v2 = get_title_list(titles_v2, subtitles=False)
    full_title_list = title_list_v1 + title_list_v2
    sorted_title_list = sorted(full_title_list, key=lambda x:x['start'])
    
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
