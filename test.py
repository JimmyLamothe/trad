import re

test_list = [{'start':1,'end':3, 'text':'1 blabla', 'ST':False},
             {'start':4, 'end':6, 'text':'bloblo', 'ST':False},
             {'start':7, 'end':8, 'text':'99 blublu', 'ST':True},
             {'start':9, 'end':11, 'text':'2 blibli', 'ST':False},
             {'start':12, 'end':14, 'text':'bleble', 'ST':False},
             {'start':15, 'end':16, 'text':'1 dodo', 'ST':False},
             {'start':17, 'end':19, 'text':'2 dudu', 'ST':False}]

def get_number(title_text):
    #Match the format: NUMBER SPACE TEXT (where NUMBER is 1-99)
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

character_dict = {}

add_names(test_list, character_dict)

print(test_list)
print(character_dict)
