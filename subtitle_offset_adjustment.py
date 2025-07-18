#!/usr/bin/env python

# Credits - generated
__author__ = "Julien Coquet"
__copyright__ = "Copyright 2025, Julien Coquet"
__credits__ = ["Julien Coquet"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Julien Coquet"
__email__ = "julien.coquet@gmail.com"
__status__ = "Production"

# Subtitle offest adjustment script
# This script adjusts the timing of subtitles in an SRT file by a specified number of seconds
# It can be used to delay or advance subtitles that are out of sync with the video.

# How to use:
# 1. Save this script as `subtitle_offset_adjustment.py` or something similar
# 2. Run it with Python, providing the input SRT file, output SRT file, and the offset in seconds.

# Example command:
# python subtitle_offset_adjustment.py input.srt output.srt 3

# TODO: Add error handling for file operations and invalid timecodes

# Lightweight library management
import re
from datetime import datetime, timedelta

# Function to parse SRT timecodes
def parse_timecode(timecode):
    """Parse SRT timecode format (HH:MM:SS,mmm) to datetime object"""
    # Replace comma with dot for microseconds
    timecode = timecode.replace(',', '.')
    return datetime.strptime(timecode, '%H:%M:%S.%f')


# Function to parse and format SRT timecodes
# SRT timecodes are in the format HH:MM:SS,mmm (hours, minutes, seconds, milliseconds)
# Example: 00:01:30,500 (1 minute and 30.5 seconds)
def format_timecode(dt):
    """Format datetime object back to SRT timecode format"""
    return dt.strftime('%H:%M:%S,%f')[:-3]  # Remove last 3 digits, keep milliseconds

# Main function to adjust subtitles
def adjust_srt_timing(input_file, output_file, seconds_offset):
    """
    Adjust all timecodes in an SRT file by a given offset in seconds.
    Positive offset delays subtitles, negative offset makes them earlier.
    """
    timecode_pattern = r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})'
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    def adjust_timecode_match(match):
        start_time = parse_timecode(match.group(1))
        end_time = parse_timecode(match.group(2))
        
        # Apply offset
        offset = timedelta(seconds=seconds_offset)
        new_start = start_time + offset
        new_end = end_time + offset
        
        # Handle negative times by setting to 00:00:00,000
        if new_start < datetime.strptime('00:00:00.000', '%H:%M:%S.%f'):
            new_start = datetime.strptime('00:00:00.000', '%H:%M:%S.%f')
        if new_end < datetime.strptime('00:00:00.000', '%H:%M:%S.%f'):
            new_end = datetime.strptime('00:00:00.000', '%H:%M:%S.%f')
        
        return f"{format_timecode(new_start)} --> {format_timecode(new_end)}"
    
    # Replace all timecodes
    adjusted_content = re.sub(timecode_pattern, adjust_timecode_match, content)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(adjusted_content)
    
    print(f"Adjusted subtitles saved to {output_file}")

# Usage example
if __name__ == "__main__":
    # To delay subtitles by 3 seconds (your case - subtitles are 3 seconds early)
    # adjust_srt_timing('input.srt', 'output.srt', 3)
    
    # Or use command line arguments
    import sys
    if len(sys.argv) == 4:
        input_file, output_file, offset = sys.argv[1], sys.argv[2], float(sys.argv[3])
        adjust_srt_timing(input_file, output_file, offset)
    else:
        print("Usage: python script.py input.srt output.srt offset_seconds")
        print("Example: python script.py movie.srt movie_fixed.srt 3")
