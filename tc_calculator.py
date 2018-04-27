import sys, math

input = int(sys.argv[1])

frames = 0

seconds = 0

minutes = 0

hours = 0

frames = input % 30

seconds = math.floor(input / 30) % 60

minutes = math.floor(input / (30*60)) % 60

hours = math.floor(input / (30*60*60)) 

print("frames: " + str(frames))

print("seconds: " + str(seconds))

print("minutes: " + str(minutes))

print("hours:  " + str(hours))

def tc_calc(input, reverse = False):
     frames = input % 30
     seconds = math.floor(input / 30) % 60
     minutes = math.floor(input / (30*60)) % 60
     hours = math.floor(input / (30*60*60)) 
     return((hours, minutes, seconds, frames))
