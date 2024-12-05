import re
from lxml import etree
import tc_calc
from pathlib import Path

def get_input_file(folder='input'):
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
    print('Default TC is 24 (same as 23.98). Type return to accept or type wanted value.')
    answer = input()
    if answer:
        tc = answer
    print('Default start hour is 0. Type return to accept or type wanted value.')
    answer = input()
    if answer:
        hour = answer
    return {'tc':tc, 'hour':hour}

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

def get_title_list(track_list, character_dict, subtitles=False):
    """ Gets list of title dicts from a video track """
    title_list = []
    i = 0
    for title in track_list:
        i += 1
        try:
            title_dict = analyze_title(title, character_dict)
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
        confirmed = input()
        if not confirmed:
            confirmed = True #Yes I know this is stupid but it's simple and works
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

def add_name(name, title_dict):
    """ Adds a name to a title_dict """
    title_dict['name'] = name

def add_names(title_list, character_dict):
    """ Adds a 'name' key to a title_dict and updates the character_dict """
    number = None
    name = None
    for title_dict in title_list:
        try:
            number = get_number(title_dict['text'])
            if not number:
                raise ValueError
            name = get_name(number, character_dict)
            title_dict['text'] = title_dict['text'].split(" ", 1)[1] #Remove number
        except ValueError:
            pass #If no new number, then we keep the old values
        if not name:
            raise ValueError('First title must have a character number')
        title_dict['name'] = name

        
def dict_from_xml(input_file, tc, hour):
    """ Creates a dict of subtitles from an xml file """
    tree = etree.parse(str(input_file))
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
    title_list_v1 = get_title_list(titles_v1, character_dict, subtitles=True)
    title_list_v2 = get_title_list(titles_v2, character_dict, subtitles=False)
    full_title_list = title_list_v1 + title_list_v2
    sorted_title_list = sorted(full_title_list, key=lambda x:x['start'])
    add_names(sorted_title_list, character_dict)
    return sorted_title_list

def combine_titles(title_list, max_gap = 48):
    """ Combine subtitles when one character is talking continuously """
    combined_titles = []
    buffer = None
    for title in title_list:
        # If 'ST' is True, don't combine
        if title['ST']:
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

input_file = get_input_file()
tc_info = get_tc_info()

subtitle_list = dict_from_xml(input_file, tc_info['tc'], tc_info['hour'])
combined_list = combine_titles(subtitle_list)


for subtitle in combined_list:
    print(subtitle)
