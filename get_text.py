"""
Convertit un fichier de sous-titres Adobe Premiere XML en fichier texte continu
pour obtenir le nombre de mots dans Antidote
"""

from analysis import get_input_file, get_title_dicts

input_file = get_input_file()
title_list = get_title_dicts(input_file, text_only=True)
output_txt = input_file.parent / f"{input_file.stem}_count.txt"

with open(output_txt, 'w') as output_file:
    for title in title_list:
        output_file.write(f"{title['text']}\n")  # Title text
        output_file.write("\n")  # Line break
