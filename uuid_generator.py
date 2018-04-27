#Generates a random probably unique UUID for FCP XML use.

from random import randrange

alphabet = "1234567890ABCDEF"

def generate_hexa(number, slash = False):
    hexa = ""
    for i in range(number):
        hexa += alphabet[randrange(0,15)]
    if slash:
        hexa += "-"
    return hexa

def generate_uuid():
    uuid = generate_hexa(8, slash = True)
    uuid += generate_hexa(4, slash = True)
    uuid += generate_hexa(4, slash = True)
    uuid += generate_hexa(4, slash = True)
    uuid += generate_hexa(12)
    return uuid
    
