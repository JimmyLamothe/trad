"""
Convertit des fichiers de sous-titres Adobe Premiere XML en fichiers texte continu
pour obtenir le nombre de mots dans Antidote
"""

from analysis import get_input_files, get_title_dicts

input_files = get_input_files()

combine = False

if len(input_files) > 1:
    user_input = input("Multiple files selected. Enter Y to combine into one text file.")
    if user_input.lower() == 'y':
        combine = True

if combine:
    filepath = input_files[1]
    output_txt = filepath.parent / f"{filepath.stem}_multiple_count.txt"
        
for count, filepath in enumerate(input_files):
    title_list = get_title_dicts(filepath, text_only=True)
    if not combine:
        output_txt = filepath.parent / f"{filepath.stem}_count.txt"
    if count == 0:
        append = 'w'
    elif not combine:
        append = 'w'
    else:
        append = 'a'
    with open(output_txt, append) as output_file:
        for title in title_list:
            print(title['text'])
            output_file.write(f"{title['text']}\n")  # Title text
            output_file.write("\n")  # Line break
