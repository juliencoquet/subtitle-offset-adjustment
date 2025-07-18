# Subtitle offest adjustment script
This script adjusts the timing of subtitles in an SRT file by a specified number of seconds.

It can be used to delay or advance subtitles that are out of sync with the video.

## How to use:
1. Save this script as `subtitle_offset_adjustment.py` or something similar
2. Run it with Python, providing the input SRT file, output SRT file, and the offset in seconds.

## Example command:
`python subtitle_offset_adjustment.py input.srt output.srt 3`

## TODO
Add error handling for file operations and invalid timecodes
