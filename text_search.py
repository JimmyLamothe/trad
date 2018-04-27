import sys

search_terms = sys.argv[1:]

test_dict = {
    "for tonight" : "pour la nuit",
    "enjoy" : "bon appétit",
    "tonight's the night" : "ça se passe ce soir"
}

#print(test_dict)

#print(search_terms)

for key in test_dict:
    found = True
    for term in search_terms:
        if term not in key:
            found = False
            continue
    if found:
        print("EN: " + key + " - FR: " + test_dict[key])

