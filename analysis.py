"""
These functions serve to take an XML file with subtitles
and create a list of dictionaries with the following keys:

'start': INT - Start frame
'end': INT - End frame
'text': STR - Text of subtitle
'ST': BOOL - True if subtitle text is to be on screen, False if it is to be recorded by an actor
'name': STR - Character name

The XML file needs two tracks: V1 = Subtitles, V2 = Dubbing
"""

import re
import pandas as pd
from lxml import etree
from pathlib import Path

def get_input_file(folder='input'):
    """ Gets latest created file as a default, or user input if different """
    input_folder = Path(folder)
    files = [item for item in input_folder.iterdir() if item.is_file()]
    latest_file = max(files, key=lambda f: f.stat().st_mtime)
    print('Press return if this is the file you want to work with, otherwise type the correct path:')
    print(latest_file)
    answer = input()
    if answer:
        latest_file = Path(answer)
    return latest_file

def get_tc_info(tc=24, hour=0):
    """ Gets TC and start hour values for the output file """
    print('Default input TC is 23.976. Type return to accept or type actual value.')
    answer = input()
    if answer:
        tc = answer
    print('Default start hour is 0. Type return to accept or type actual value.')
    answer = input()
    if answer:
        hour = answer
    return {'tc':tc, 'hour':hour}

def get_user_choice(prompt, choices_map, default_value):
        """Prompt user for a choice, returning the mapped value or default."""
        print(prompt)
        for key, value in choices_map.items():
            print(f"{key}: {value}")
        user_input = input("Choose a number or press Return for default: ").strip()
        return choices_map.get(user_input, default_value)

def get_full_tc_info(tc_in=None, tc_out=None, start_hour=None):
    """ Get needed values to convert frames to different TC values """
    tc_in_map = {
        '1':'23.976',
        '2':'24',
        '3':'25',
        '4':'29.97',
        '5':'30'
        }
    tc_out_map = {
        '1':'23.976',
        '2':'24',
        '3':'25',
        '4':'30',
        '5':'SRT'
        }
    hour_map = {
        '0':0,
        '1':1,
        '10':10
        }
    tc_in_conversion_map = {
        '23.976':24,
        '24':24,
        '25':25,
        '29.97':30,
        '30':30
        }
    if not tc_in:
        tc_in = get_user_choice(
            "\nSelect the input timecode format (default is 23.976):",
            tc_in_map,
            '23.976'
        )
        tc_in = tc_in_conversion_map[tc_in]
    if not tc_out:
        tc_out = get_user_choice(
            "\nSelect the output timecode format (default is SRT):",
            tc_out_map,
            'SRT'
        )
    if not start_hour:
        start_hour = get_user_choice("\nSelect the start hour (default is 0):", hour_map, 0)
    return {'tc_in':tc_in, 'tc_out':tc_out, 'start_hour':start_hour}
    
def get_track_list(video_or_audio):
    return(video_or_audio.findall('track'))

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
    
def analyze_title(title):
    """ Returns the text, start and end times of a title """
    value = get_title_value(title)
    if not value:
        raise ValueError('Empty title')
    value = value.replace('&amp;#13;', '\n')
    text = ""
    previous_letter = ""
    letter_count = 0
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
    start = int(title.find('start').text)
    end = int(title.find('end').text)
    return {'start': start,
            'end': end,
            'text': text}

def get_title_list(track_list, subtitles=False):
    """ Gets list of title dicts from a video track """
    title_list = []
    i = 0
    for title in track_list:
        i += 1
        try:
            title_dict = analyze_title(title)
            title_dict['ST'] = subtitles
            title_list.append(title_dict)
        except ValueError as e:
            print(e)
    return title_list

def get_number(title_text):
    """ Gets the number from a string like this: 2-DIGIT-NUMBER/SPACE/TEXT """
    match = re.match(r"^([1-9][0-9]?)\s.+$", title_text)
    if match:
        return int(match.group(1))  # Extract and return the number
    return None  # Return None for any other format

def get_new_name(number):
    """ Gets name from user input for new character number """
    confirmed = False
    while not confirmed:
        name = input(f'Type name for character {number}:')
        print('Press Return to confirm or anything else to try again:')
        print(f'{number}: {name}')
        user_input = input()
        if not user_input:
            confirmed = True
        else:
            confirmed = False
    return name

def get_name(number, character_dict):
    try:
        name = character_dict[number]
    except KeyError:
        name = get_new_name(number)
        character_dict[number] = name
    return name

def remove_name_id(title_dict):
    """ Removes the two digit name identifier at the start of a title """
    number = get_number(title_dict['text'])
    if number:
        title_dict['text'] = title_dict['text'].split(" ", 1)[1]
    
def add_names(title_list, character_dict):
    """ Adds a 'name' key to a title_dict and updates the character_dict """
    number = None
    last_dubbed_name = None  # Tracks the last dubbed speaker (ST=False)
    last_subtitled_name = None  # Tracks the last subtitled speaker (ST=True)
    for title_dict in title_list:
        try:
            number = get_number(title_dict['text'])
            if not number:
                raise ValueError
            name = get_name(number, character_dict)
            title_dict['text'] = title_dict['text'].split(" ", 1)[1]  # Remove number
            title_dict['split'] = True # Don't combine titles even if same speaker
        except ValueError:
            # If no new number, use the last known speaker for the current type
            if title_dict['ST']:
                name = last_subtitled_name
            else:
                name = last_dubbed_name
            title_dict['split'] = False
        if not name:
            raise ValueError('First title must have a character number')
        title_dict['name'] = name
        # Update the last speaker for the appropriate type
        if title_dict['ST']:
            last_subtitled_name = name
        else:
            last_dubbed_name = name
        
def get_title_dicts(input_file, surimpression=True):
    """ Creates a list of subtitle dicts from an xml file """
    tree = etree.parse(str(input_file))
    root = tree.getroot()
    sequence = root.find('sequence')
    media = sequence.find('media')
    video = media.find('video')
    track_list = get_track_list(video)
    full_title_list = []
    v1 = track_list[0]
    titles_v1 = v1.findall('clipitem')
    title_list_v1 = get_title_list(titles_v1, subtitles=True)
    full_title_list += title_list_v1
    if surimpression:
        v2 = track_list[1]
        titles_v2 = v2.findall('clipitem')
        title_list_v2 = get_title_list(titles_v2, subtitles=False)
        full_title_list += title_list_v2
    sorted_title_list = sorted(full_title_list, key=lambda x:x['start'])
    if surimpression:
        character_dict = {}
        add_names(sorted_title_list, character_dict)
    else:
        for title in sorted_title_list:
            remove_name_id(title)
    return sorted_title_list

def combine_titles(title_list, max_gap = 24):
    """ Combine subtitles when one character is talking continuously """
    combined_titles = []
    buffer = None
    for title in title_list:
        # If 'ST' is True or we forced a split, don't combine
        if title['ST'] or title.get('split', False):
            if buffer:
                combined_titles.append(buffer)
                buffer = None
            combined_titles.append(title)
            continue
        # If there's no buffer, start one
        if buffer is None:
            buffer = title
        else:
            # Check if the gap is within max_gap and speaker matches
            if title['start'] - buffer['end'] <= max_gap and title['name'] == buffer['name']:
                # Combine titles
                buffer['end'] = title['end']
                buffer['text'] += " " + title['text']
            else:
                # Add the buffered title to the list and start a new buffer
                combined_titles.append(buffer)
                buffer = title
    # Add any remaining buffer
    if buffer:
        combined_titles.append(buffer)
    return combined_titles

def add_duration(title_list):
    """ Adds the duration in frames to each title """
    for title in title_list:
        title['duration'] = title['end'] - title['start']
    return title_list

def get_character_timing(title_list):
    """ Takes a subtitle dict and gets the total speaking time for each character """
    df = pd.DataFrame(title_list)
    df = df[df['ST'] == False]
    result = df.groupby('name')['duration'].sum().reset_index()
    total_duration = result['duration'].sum()
    timing_list = result.values.tolist()
    timing_list.append(['Durée totale', total_duration])
    return timing_list
