"""Converts a duration in frames into standard 30 frame TC, or standard
30 frame TC into frames.
"""

import sys, math

def tc_calc(input, integer = False, reverse = False, hour = 0, tc = 30,
            srt=False):
     """input is an integer (number of frames).
     Use reverse = True to go from TC to frames.
     If reverse, input is a 4-tuple (hours, mins, secs, frames).
     Use hour if TC start is e.g. 9:58:30:00 or 10:00:00:00.
     Use tc to specify tc rate if different than 30. Only 24 implemented.
     Use srt when exporting srt (real time)
     """ 
     if reverse:
          if(tc == 24):
               hour_frames = math.floor(input[0] * (60*60*23.976))
               min_frames = math.floor(input[1] * (60*23.976))
               sec_frames = math.floor(input[2] * (23.976))
               total_frames = input[3] + sec_frames + min_frames + hour_frames
          else:
               hour_frames = input[0] * (60*60*30)
               min_frames = input[1] * (60*30)
               sec_frames = input[2] * (30)
               total_frames = input[3] + sec_frames + min_frames + hour_frames

          return total_frames

     else:
          coefficient = 1
          if(tc == 24 and not srt):
               coefficient = 0.999
          offset = math.floor(input/960)     
          total = math.floor(coefficient*(input + offset))
          frames = math.floor(total % tc)
          seconds = math.floor(total / tc) % 60
          minutes = math.floor(total / (tc*60)) % 60
          hours = math.floor(total / (tc*60*60)) 
          frame_string = "0"
          if hour:
               hours = hour
          if frames < 10:
               frame_string += str(frames)
          else:
               frame_string = str(frames)
          second_string = "0"
          if seconds < 10:
               second_string += str(seconds)
          else:
               second_string = str(seconds)
          minute_string = "0"
          if minutes < 10:
               minute_string += str(minutes)
          else:
               minute_string = str(minutes)
          hour_string = "0"
          if hours < 10:
               hour_string += str(hours)
          else:
               hour_string = str(hours)
          if integer:
               return((hours, minutes, seconds, frames))
          else:
               return(hour_string + ":" + minute_string + ":" +
                      second_string + ":" + frame_string)
