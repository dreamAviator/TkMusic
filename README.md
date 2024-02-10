# TkMusic
### A music player written in python, that uses Tkinter and the vlc-python module

Normally the python-vlc module needs to have the VLC Media Player installed, but this program also works, when the VLC Media Player is not installed, because all the necessary files are in the project files.


### Supported file formats:
These have been tested and work:
- MP3		(MPEG-1 Audio Layer III or MPEG-2 Audio Layer III)
- m4a		(MPEG-4 Audio Layer)
- Ogg		(ogg vorbis)
- FLAC	(Free Lossless Audio Codec)
- WMA		(Windows Media Audio)
- WAV		(Waveform Audio File Format)
- WV		(WavPack Audio File)
- AIFF	(Audio Interchange File Format)
- AC3		(Adaptive Transform Coder 3 [Dolby Digital])
- Opus
- MP2		(MPEG-1 Audio Layer 2)

If the selected file isn't one of these formats, the program will say, the file is not supported.

These have been tested and do not work:
- AMR  (Adaptive Multi-Rate ACELP Codec file)
