# TkMusic
### A music player written in python, that uses Tkinter and the vlc-python module



### Features:
- Play music
- Many supported formats (list below)
- Although using the python-vlc module, vlc does not have to be installed*
- Create and edit playlists, open them with any other media player**
- View and edit metadata (including the song cover)
- Works on Windows and Linux with the same code
- Straightforward not bad looking UI
- Open Source

*Normally when using the python-vlc module, the VLC Media Player has to be installed. Here, all the necessary files from the VLC Media Player are included, so you don't have to install it
**Playlists are saved in the m3u or m3u8 format, an open playlist format a lot of media players support



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
