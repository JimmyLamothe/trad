"""
Convert frames to a string in the correct TC format.

Input is always the number of frames (int).

Keyword arguments are:

coefficient - This is a constant (float) to correct for slower playback in 23,976 or 29,97 fps
              Value is 1,001
              Default is True
              True means that the input was in 23,976 or 29,97 fps.
tc_in: This is the fps of the input (int).
       Valid values are 24, 25, or 30
       Default is 24
tc_out - This is the required output format (str)
         Valid values are '23.976', '24', '25', or 'SRT'
         Default value is '23.976'
start_hour: This is the start hour (int).
            Valid values are 0, 1 or 10.
            Default value is 0.

Output is always a string representing a time code.

HH:MM:SS:fr formats (Hour - Minute - Second - Frame):

'23,976': This is a non-real time TC format.
          Don't apply the coefficient if True.
          If coefficient is False, apply a reverse coefficient
          (we reduce the number of frames to go with the slowed down playback).

'24', '25': Real time formats in 24 or 25 frames per second.
            Apply the coefficient if True
            (we add frames to go with the sped up playback)

HH:MM:SS:mls (Hour - Minute - Second - Millisecond):

'SRT': This is a real time representation of playback time.
       Apply the coefficient if True
       (we add frames to compensate for real-time playback)
"""

COEFFICIENT = 1.001

fps_map = {
        '23.976': 24,
        '24': 24,
        '25': 25,
        'SRT': None  #SRT uses same as input
    }

def apply_coefficient(frame, tc_out, coefficient):
    """ Corrects the frame number if needed """
    if tc_out == '23,976':
        if not coefficient:
            return round(frame / COEFFICIENT)
    else:
        if coefficient:
            return round(frame * COEFFICIENT)
    return frame

def frame_to_timecode(frame, fps):
        """Convert frame to HH:MM:SS:ff."""
        seconds = frame // fps
        frames = frame % fps
        minutes = seconds // 60
        seconds = seconds % 60
        hours = minutes // 60
        minutes = minutes % 60
        return hours, minutes, seconds, frames

def format_timecode(hours, minutes, seconds, frames, fps=None, srt_format=False):
        """Format timecode as HH:MM:SS:ff or HH:MM:SS,ms."""
        if srt_format:
            milliseconds = round((frames / fps) * 1000)
            return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"
        else:
            return f"{hours:02}:{minutes:02}:{seconds:02}:{frames:02}"

def get_tc(frame, coefficient=True, tc_in=24, tc_out='SRT', start_hour=0):
    """ Main function - converts frame (int) to output_TC (str) """
    #frame = frame - 1 #First frame must output all zeros - Removed for testing
    if not tc_out == 'SRT':  # SRT uses input FPS only
        output_fps = fps_map[tc_out]
        if not tc_in == output_fps:
            frame = round(frame * (fps_map[tc_out] / tc_in))
    frame = apply_coefficient(frame, tc_out, coefficient)
    # Convert frame to timecode
    if tc_out == 'SRT':
        # For SRT, calculate real time using input FPS only
        hours, minutes, seconds, frames = frame_to_timecode(frame, tc_in)
        return format_timecode(hours, minutes, seconds, frames, fps=tc_in, srt_format=True)
    else:
        # Other formats use output FPS (if applicable)
        hours, minutes, seconds, frames = frame_to_timecode(frame, round(fps_map[tc_out]))
        hours += start_hour  # Add start hour
        return format_timecode(hours, minutes, seconds, frames)
