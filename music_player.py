    #TkMusic
    #This program can play music.
    #Copyright (C) 2024 Lilly, dreamAviator, Nathan Baron
print("loading...")
#gui
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from PyQt5.QtWidgets import QApplication, QFileDialog
#gui + music (song cover)
from PIL import Image
#music
import mutagen
from mutagen import File
from mutagen.id3 import ID3, TIT2, TPE1
from mutagen.mp3 import MP3
from mutagen.oggvorbis import OggVorbis
from mutagen.mp4 import MP4
#metadata editor
#import metadata_editor
#other
from threading import *
import webbrowser
import functools
import random
import datetime#auch music
import time
import platform
import os
import sys
#messages
if platform.system() == "Windows":
    from win10toast import ToastNotifier
    toast = ToastNotifier
elif platform.system() == "Linux":
    import notify2
    notify2.init('TkMusic')

    notify2.Notification("loading","loading...").show()
#um relative pfade zu absoluten pfaden umzuwandeln
dirname = os.path.dirname(__file__)
#vlcdll_path = os.path.join(dirname, 'vlc\libvlc.dll')
#print(vlcdll_path)
#gibt an wo vlc ist
vlc_path = os.path.join(dirname,'vlc-3.0.20')
#vlc_path = 'C:\\Users\\Nathan\\Documents\\Python\\Music Player Reworked\\vlc-3.0.20'
#setzt irgendwie den vlc pfad
os.environ['PATH'] += ';' + vlc_path
#os.add_dll_directory(r'C:/Users/Nathan/Documents/Python/Music Player Reworked/vlc-3.0.20')
#C:\Users\Nathan\Documents\Python\Music Player Reworked\VLCPortable\App\vlc
#os.chdir(r'C:/Users/Nathan/Documents/Python/Music Player Reworked/')
#vlc
import vlc
instance = vlc.Instance("--no-xlib")
player = instance.media_player_new()


#music control functions
def loadSong():
    global song
    global songCover
    global songCoverSmol
    global songCoverMini
    global song_cover_image
    global song_cover_image_smol
    global songLength
    global songLengthFEC
    global songName
    global songArtist
    global songFilename
    global musicSliderExtra
    global songLengthTextSmol
    global songNameTextSmol
    global songArtistTextSmol
    global miniModeWindow
    global musicSliderMini
    global songTitleLabelMini
    global songArtistLabelMini
    global songLengthTextMini
    global songArtImageSmol
    media = instance.media_new(song)
    media.get_mrl()
    player.set_media(media)
    songLength,songLengthSec = getSongLength(song)
    songLengthFEC = songLength#FEC = for end check
    songName = getSongName(song)
    songArtist = getSongArtist(song)
    songArt = getSongArt(song)
    songLS = song.rfind("/")#song last slash
    songFilename = song[songLS + 1:]
    print(songLength)
    print(songLengthSec)
    print(songName)
    print(songArtist)
    print(songArt)
    print(songLS)
    print(songFilename)
    try:
        musicSlider.config(to = songLengthSec)
        songLengthText.config(text = songLength)
        songArtistText.config(text = songArtist)
        songNameText.config(text = songName)
    except:
        pass
    try:
        musicSliderExtra.config(to = songLengthSec)
    except:
        pass
    try:
        musicSliderMini.config(to = songLengthSec)
    except:
        pass
    #songArt_pillow1 = Image.open(songArt)
    #songArt_pillow2 = ImageTk.PhotoImage(songArt)
    if songArt != "nothing":
        jpg_image = Image.open(songArt)
        new_size = (200,200)
        new_size_smol = (50,50)
        jpg_image_resized = jpg_image.resize(new_size)
        jpg_image_resized_smol = jpg_image.resize(new_size_smol)
        jpg_image_resized.save('song_cover.png',format = 'PNG')
        jpg_image_resized_smol.save('song_cover_smol.png',format = 'PNG')
        songArtImage = tk.PhotoImage(file = 'song_cover.png')
        songArtImageSmol = tk.PhotoImage(file = 'song_cover_smol.png')
        try:
            songCover.config(image = songArtImage)
            songCover.image = songArtImage
        except:
            pass
        try:
            songCoverSmol.config(image = songArtImageSmol)
            songCoverSmol.image = songArtImageSmol
        except:
            pass
        try:
            songCoverMini.config(image = songArtImageSmol)
            songCoverMini.image = songArtImageSmol
        except:
            pass
        jpg_image.close()
    else:
        try:
            songCover.config(image = song_cover_image)
        except:
            pass
        try:
            songCoverSmol.config(image = song_cover_image_smol)
        except:
            pass
        try:
            songCoverMini.config(image = song_cover_image_smol)
        except:
            pass
    try:
        songArtistTextSmol.config(text = songArtist)
        songNameTextSmol.config(text = songName)
    except:
        pass
    try:
        songArtistLabelMini.config(text = songArtist)
        songTitleLabelMini.config(text = songName)
    except:
        pass
    if songArtist == 'unknown':
        try:
            songArtistText.config(text = songFilename)
        except:
            pass
        try:
            songArtistTextSmol.config(text = songFilename)
        except:
            pass
        try:
            songArtistLabelMini.config(text = songFilename)
        except:
            pass
        if songName == 'unknown':
            try:
                songNameText.config(text = '')
            except:
                pass
            try:
                songNameTextSmol.config(text = '')
            except:
                pass
            try:
                songTitleLabelMini.config(text = '')
            except:
                pass
        else:

            try:
                songNameText.config(text = songName)
            except:
                pass
            try:
                songNameTextSmol.config(text = songName)
            except:
                pass
            try:
                songTitleLabelMini.config(text = songName)
            except:
                pass
    elif songName == 'unknown':
        try:
            songNameText.config(text = songFilename)
        except:
            pass
        try:
            songNameTextSmol.config(text = songFilename)
        except:
            pass
        try:
            songTitleLabelMini.config(text = songFilename)
        except:
            pass
    else:
        try:
            songArtistText.config(text = songArtist)
            songNameText.config(text = songName)
        except:
            pass
        try:
            songArtistTextSmol.config(text = songArtist)
            songNameTextSmol.config(text = songName)
        except:
            pass
        try:
            songArtistLabelMini.config(text = songArtist)
            songTitleLabelMini.config(text = songName)
        except:
            pass
    try:
        main_window.title(songFilename + " | TkMusic")
    except:
        pass
    try:
        miniModeWindow.title(songFilename + " | TkMusic")
    except:
        pass
    player.play()
    checkLogo()

def threading():
    t1 = Thread(target = loadSong)
    t1.start()
    t2 = Thread(target = songPos)
    t2.start()

def getSongLength(filepath):
    global songLengthFEC
    global songLengthSmol
    #print("hiiiiiiiii\n" + filepath)
    audio = mutagen.File(filepath)
    if audio != {}:
        if isinstance(audio,mutagen.mp3.MP3):
            songLengthSec = audio.info.length
        elif isinstance(audio,mutagen.mp4.MP4):
            songLengthSec = audio.info.length
        elif isinstance(audio,mutagen.oggvorbis.OggVorbis):
            songLengthSec = audio.info.length
        elif isinstance(audio,mutagen.wavpack.WavPack):
            songLengthSec = audio.info.length
        elif isinstance(audio,mutagen.flac.FLAC):
            songLengthSec = audio.info.length
        elif isinstance(audio,mutagen.aiff.AIFF):
            songLengthSec = audio.info.length
        elif isinstance(audio,mutagen.asf.ASF):#für wma files benutzt mutagen asf (advanced systems format) [chatgpt]
            songLengthSec = audio.info.length
    else:
        media = instance.media_new(filepath)
        media.get_mrl()
        media.parse_with_options(1,0)
        while media.get_duration() < 0:#brauche ich, da der den song erst vollständig laden muss
            continue
        songLengthMS = media.get_duration()
        media.release()
        songLengthSec = songLengthMS // 1000
    songLength = str(datetime.timedelta(seconds = songLengthSec))
    dot = songLength.rfind(".")
    doubledot = songLength.rfind(":")
    if songLength[:doubledot] != "00":
        if dot != -1:
            songLength = songLength[doubledot - 2:dot]
            return songLength,songLengthSec
        else:
            songLength = songLength[doubledot - 2:]
            return songLength,songLengthSec
    else:
        if dot != -1:
            songLength = songLength[:dot]
            return songLength,songLengthSec
        else:
            return songLength,songLengthSec

def getSongName(filepath):
    try:
        audio = File(filepath,easy = True)
        songName = audio['title']
    except:
        return "unknown"
    #if filepath.endswith('.mp3'):#hat nicht wirklich funktioniert... :/
    #    audio = ID3(filepath)
    #    try:
    #        audio["TIT2"] = TIT2(encoding = 3,text = songName)
    #    except:
    #        return "unknown"
    #if filepath.endswith('.ogg'):
    #    audio = OggVorbis(filepath)
    #    try:
    #        songName = audio['title']
    #    except:
    #        "unknown"
    #if filepath.endswith('.m4a'):
    #    audio = MP4(filepath)
    #    try:
    #        songName = audio['\xa9nam']
    #    except:
    #        return "unknown"
    #print(songName)
    return str(songName)[2:-2]

def getSongArtist(filepath):
    try:
        audio = File(filepath,easy = True)
        artist = audio['artist']
    except:
        return "unknown"
    #if filepath.endswith('.mp3'):
    #    audio = ID3(filepath)
    #    try:
    #        audio["TPE1"] = TPE1(encoding = 3,text = artist)
    #    except:
    #        return "unknown"
    #if filepath.endswith('.ogg'):
    #    audio = OggVorbis(filepath)
    #    try:
    #        artist = audio['artist']
    #    except:
    #        return "unknown"
    #if filepath.endswith('.m4a'):
    #    audio = MP4(filepath)
    #    try:
    #        artist = audio['\xa9ART']
    #    except:
    #        return "unknown"
    #print(artist)
    return str(artist)[2:-2]

def getSongArt(filepath):
    try:
        print("i'm")
        audio = File(filepath)
        if 'covr' in audio:
            print("genderfluid ig")
            # MP3, FLAC, and some other formats
            album_art_data = audio['covr'][0]
        elif 'APIC:Cover' in audio:
            print("and i hate that")
            # ID3v2 (commonly used in MP3)
            album_art_data = audio['APIC:Cover'].data
        elif 'metadata_block_picture' in audio:
            print("and it's just so hard")
            # FLAC (base64-encoded)
            album_art_data = audio['metadata_block_picture'][0].data
        elif 'covr' in audio:
            print("and i don't know how long")
            # MP4 (M4A)
            album_art_data = audio['covr'][0]
        elif 'WM/Picture' in audio:
            print("i can take this anymore")
            # Windows Media Audio (WMA)
            album_art_data = audio['WM/Picture'][0].data
        else:
            print(f"No cover art found in {filepath}")
            return "nothing"
        with open('song_cover.jpg','wb') as f:
            f.write(album_art_data)
        return "song_cover.jpg"
    except Exception as e:
        message(3,"Error","There was an error reading the song cover\n" + str(e))
        return "nothing"

def songPos():
    global songMS
    global pPlaylist
    global sliderPressed
    global songLengthFEC
    global exiting
    global ThreadStopped
    while True:
        print("songpos working")
        print(exiting)
        if exiting == True:
            print("exiting")
            print(exiting)
            return
        time.sleep(1)
        songMS = player.get_time()
        songTime = str(datetime.timedelta(milliseconds = songMS + 500))
        dot = songTime.rfind(".")
        doubledot = songTime.rfind(":")
        songTimeFin = songTime[doubledot - 2:dot]
        if sliderPressed == False:
            try:
                songPositionText.config(text = songTimeFin)
            except:
                pass
            try:
                songPositionTextSmol.config(text = songTimeFin)
            except:
                pass
            try:
                songPositionTextMini.config(text = songTimeFin)
            except:
                pass
            sliderVar.set(songMS // 1000)
            sliderVarExtra.set(songMS // 1000)
            sliderVarMini.set(songMS // 1000)
        if player.get_state() == vlc.State.Ended:
            break
    #time.sleep(0.2)#damit der song wirklich zuende spielt#brauche ich nicht, weil ich player.get_state() benutze
    fastForward()

def togglePlay():
    if player.get_state() == vlc.State.Playing:
        player.set_pause(1)
    else:
        player.set_pause(0)
    checkLogo()

def togglePlayKey(event):
    togglePlay()

def checkLogo():
    global togglePlayButtonSmol
    global togglePlayButtonMini
    if player.get_state() == vlc.State.Playing:
        try:
           togglePlayButton.config(image = play_image)
        except:
            pass
        try:
            togglePlayButtonSmol.config(image = play_image_smol)
        except:
            pass
        try:
            togglePlayButtonMini.config(image = play_image_smol)
        except:
            pass
    else:
        try:
            togglePlayButton.config(image = pause_image)
        except:
            pass
        try:
            togglePlayButtonSmol.config(image = pause_image_smol)
        except:
            pass
        try:
            togglePlayButtonMini.config(image = pause_image_smol)
        except:
            pass

def checkLogoInverted():#beim fenster neuladen muss das irgendwie andersherum sein
    if player.get_state() == vlc.State.Playing:
        try:
            togglePlayButton.config(image = pause_image)
        except:
            pass
        try:
            togglePlayButtonSmol.config(image = pause_image_smol)
        except:
            pass
        try:
            togglePlayButtonMini.config(image = pause_image_smol)
        except:
            pass
    else:
        try:
            togglePlayButton.config(image = play_image)
        except:
            pass
        try:
            togglePlayButtonSmol.config(image = play_image_smol)
        except:
            pass
        try:
            togglePlayButtonMini.config(image = play_image_smol)
        except:
            pass

def nextSong(where):
    global playlist
    global pPlaylist
    global song
    global tree
    global treeMiniMode
    global miniModeActive
    try:
        song = playlist[0]
    except:
        togglePlay()
        return
    if song.endswith('.m3u'):
        del playlist[0]
        nextSong("nextSong")
    threading()
    if where == "skipF" or where == "skipB" or where == "fst" or where == "lst" or where == "end":
        if miniModeActive.get() == False:
            items = tree.get_children()
            for item_id in items:
                values = tree.item(item_id,"values")
                tree.item(item_id,tags = ("not_playing"))
                if values[3] == str(len(pPlaylist) + 1):
                    tree.see(item_id)
                    tree.item(item_id,tags = ("playing"))
                    if where == "skipF" or where == "end":
                        remainingLength("f")
                    elif where == "skipB":
                        remainingLength("b")
                    elif where == "fst":
                        remainingLength("fst")
                    elif where == "lst":
                        remainingLength("lst")
        elif miniModeActive.get() == True:
            items = treeMiniMode.get_children()
            for item_id in items:
                values = treeMiniMode.item(item_id,"values")
                treeMiniMode.item(item_id,tags = ("not_playing"))
                if values[3] == str(len(pPlaylist) + 1):
                    treeMiniMode.see(item_id)
                    treeMiniMode.item(item_id,tags = ("playing"))
                    if where == "skipF" or where == "end":
                        remainingLength("f")
                    elif where == "skipB":
                        remainingLength("b")
                    elif where == "fst":
                        remainingLength("fst")
                    elif where == "lst":
                        remainingLength("lst")
        plstSelSee(0,0)
        return
    updatePlaylist(0,0)

def fastForward():
    global loopPlaylist
    if playlist == [] and pPlaylist == []:
        return
    try:
        if len(playlist) == 1 and loopPlaylist.get() == False:
            message(1,fastForward_message1_title_langtext,fastForward_message1_text_langtext,"customSettings,settings;No,nope",5000)#eigentlich ok und ein anderer button der einen zu den einstellungen/der entsprechenden einstellung führt, noch hnzufügen
            return
        elif len(playlist) == 1 and loopPlaylist.get() == True:
            removeThem = []
            for element in pPlaylist:
                playlist.append(element)
            for element in pPlaylist:
                removeThem.append(element)
            for element in removeThem:
                pPlaylist.remove(element)
            playlist.append(playlist[0])
            del playlist[0]
            nextSong("fst")
        else:
            pPlaylist.append(playlist[0])
            del playlist[0]
            nextSong("skipF")
    except Exception as e:
        print(e)
        message(3,fastForward_message2_title_langtext,fastForward_message2_text_langtext + str(e),"ok",0)

def fastForwardKey(event):
    fastForward()

def stepFastForward():
    timeMS = player.get_time()
    timeMS = timeMS + 1000
    player.set_time(timeMS)

def stepFastForwardKey(event):
    stepFastForward()

def rewindSong():
    global loopPlaylist
    global pPlaylist
    global playlist
    lst = False
    if playlist == [] and pPlaylist == []:
        return
    if songMS > 3000:
        player.set_time(0)
    else:
        try:
            if len(pPlaylist) == 0 and loopPlaylist.get() == False:
                message(1,rewindSong_message1_title_langtext,rewindSong_message1_text_langtext,"customSettings,settings;No,nope",5000)#eigentlich ok und ein anderer button der einen zu den einstellungen/der entsprechenden einstellung führt, noch hnzufügen
                return
            elif len(pPlaylist) == 0 and loopPlaylist.get() == True:
                removeThem = []
                for element in playlist:
                    pPlaylist.append(element)
                for element in playlist:
                    removeThem.append(element)
                for element in removeThem:
                    playlist.remove(element)
                lst = True
            playlist.insert(0,pPlaylist[-1])
            del pPlaylist[-1]
            if lst== True:
                nextSong("lst")
            else:
                nextSong("skipB")
        except Exception as e:
            message(3,rewindSong_message2_title_langtext,rewindSong_message2_text_langtext + str(e),"ok",0)
            return

#def rewindSong():#behalten, damit du weißt wie du das mit dem index gemacht hast
#    global loopPlaylist
#    global tree
#    lst = False
#    if playlist == [] and pPlaylist == []:
#        return
#    selection = tree.selection()
#    index = tree.index(selection[0])
#    if songMS > 3000:
#        player.set_time(0)
#    else:
#        try:
#            if index == 0 and loopPlaylist.get() == False:
#                message(1,"No previous song","There is no previous song, you can't rewind.\n" + "If you want the last song of the playlist to play, turn the feature on in the settings.","customSettings,settings;No,nope",5000)#eigentlich ok und ein anderer button der einen zu den einstellungen/der entsprechenden einstellung führt, noch hnzufügen
#                return
#            elif index == 0 and loopPlaylist.get() == True:
#                removeThem = []
#                for element in playlist:
#                    pPlaylist.append(element)
#                for element in playlist:
#                    removeThem.append(element)
#                for element in removeThem:
#                    playlist.remove(element)
#                lst = True
#            playlist.insert(0,pPlaylist[-1])
#            del pPlaylist[-1]
#            if lst== True:
#                nextSong("lst")
#            else:
#                nextSong("skipB")
#        except Exception as e:
#            message(3,"Error","There was an error while trying to skip to the previous song.\n\n(To skip to the previous song you have to select the current song)\n\n\nError message:\n\n" + str(e),"ok",0)
#            return

def rewindSongKey(event):
    rewindSong()

def stepRewindSong():
    timeMS = player.get_time()
    timeMS = timeMS - 1000
    player.set_time(timeMS)

def stepRewindSongKey(event):
    stepRewindSong()

def sliderChange(event):
    global sliderPressed
    global extraWindow
    if sliderPressed == True:
        try:
            if extraWindow.winfo_exists():
                player.set_time(sliderVarExtra.get() * 1000)
            elif miniModeWindow.winfo_exists():
                player.set_time(sliderVarMini.get() * 1000)
            else:
                player.set_time(sliderVar.get() * 1000)
        except:
            player.set_time(sliderVar.get() * 1000)
    sliderPressed = False

def sliderPressedTrue(event):
    global sliderPressed
    sliderPressed = True

def sliderChangePos(event):
    global sliderPressed
    global songPositionTextSmol
    global songPositionTextMini
    global extraWindow
    global miniModeWindow
    if sliderPressed == True:
        try:
            if extraWindow.winfo_exists():
                sliderPos = sliderVarExtra.get()
                sliderPos = str(datetime.timedelta(seconds = sliderPos))
            elif miniModeWindow.winfo_exists():
                sliderPos = sliderVarMini.get()
                sliderPos = str(datetime.timedelta(seconds = songPos))
            else:
                sliderPos = sliderVar.get()
                sliderPos = str(datetime.timedelta(seconds = sliderPos))
        except:
            sliderPos = sliderVar.get()
            sliderPos = str(datetime.timedelta(seconds = sliderPos))
        dot = sliderPos.rfind(".")
        doubledot = sliderPos.rfind(":")
        if dot != -1:
            sliderPosFin = sliderPos[doubledot - 2:dot]
        else:
            sliderPosFin = sliderPos[doubledot - 2:]
        try:
            songPositionText.config(text = sliderPosFin)
        except:
            pass
        try:
            songPositionTextSmol.config(text = sliderPosFin)
        except:
            pass
        try:
            songPositionTextMini.config(text = sliderPosFin)
        except:
            pass

#playlist functions
def addToPlaylist(mbsong):#maybe song
    global playlist
    global plWtitleNameTrue
    global plWtitleName
    global recentFiles
    global recentSongs
    global recentPlaylists
    global filesToKeep
    songsToAdd = []
    howmany = filesToKeep.get()
    unsupportedFiles = ""
    print("addtofiles")
    print(mbsong)
    if playlist == []:
        rememberme = True
    else:
        rememberme = False
    plWtitleNameTrue = False
    if mbsong == "no":
        songsToAdd = openFilesDialog()
        print(songsToAdd)
    else:
        songsToAdd.append(mbsong)
    if songsToAdd == []:
        return
    loading_Threading()
    print("addtoplaylist")
    print("here loadingthreading addtoplaylist")
    for sOpllst in songsToAdd:#song or playlist
        del recentFiles[howmany - 1]
        print(recentFiles)
        recentFiles.insert(0,sOpllst + '\n')
        if sOpllst.endswith('.m3u') or sOpllst.endswith('.txt'):
            del recentPlaylists[howmany - 1]
            recentPlaylists.insert(0,sOpllst + '\n')
            if rememberme == True:
                plWtitleNameTrue = True
                lastSlash = sOpllst.rfind("/")
                plWtitleName = sOpllst[lastSlash + 1:]
            with open(sOpllst,'r') as file:
                lines = file.readlines()
            for songFplaylist in lines:#song from playlist
                songFplaylist = songFplaylist[:-1]
                playlist.append(songFplaylist)
        elif sOpllst.endswith('.m3u8'):
            del recentPlaylists[howmany - 1]
            recentPlaylists.insert(0,sOpllst + '\n')
            if rememberme == True:
                plWtitleNameTrue = True
                lastSlash = sOpllst.rfind("/")
                plWtitleName = sOpllst[lastSlash + 1:]
            with open(sOpllst,'r') as file:
                lines = file.readlines()
            for line in lines:
                if line != "#EXTM3U":
                    if line.startswith("#EXTINF:"):
                        comma = line.find(",")
                        separator = line.find(" - ")
                        line = line[8:]
                        lengthSec = line[:comma]
                        line = line[comma + 1:]
                        interpreter = line[:separator]
                        line = line[separator + 4:]
                        title = line
                    else:
                        playlist.append(line[:-1])
            del playlist[0]
        else:
            del recentSongs[howmany - 1]
            recentSongs.insert(0,sOpllst + '\n')
            #del songsToAdd[0]
    print(recentFiles)
    filepath = os.path.join(dirname,"texts/recent_files.txt")
    with open(filepath,'w') as file:
        file.writelines(recentFiles)
    filepath = os.path.join(dirname,"texts/recent_songs.txt")
    with open(filepath,'w') as file:
        file.writelines(recentSongs)
    filepath = os.path.join(dirname,"texts/recent_playlists.txt")
    with open(filepath,'w') as file:
        file.writelines(recentPlaylists)
    refreshRecentFiles()

    print("here we go again again lol")
    print(songsToAdd)
    for element in songsToAdd:
        if not element.lower().endswith('.mp3') and not element.lower().endswith('.ogg') and not element.lower().endswith('.flac') and not element.lower().endswith('.m4a') and not element.lower().endswith('.wma') and not element.lower().endswith('.wav') and not element.lower().endswith('.aiff') and not element.lower().endswith('.ac3') and not element.lower().endswith('.opus') and not element.lower().endswith('.mp2') and not element.lower().endswith('.wv') and not element.lower().endswith('.m3u') and not element.lower().endswith('.txt') and not element.lower().endswith('.m3u8'):#m3u, da wenn man eine playlist einlädt auch immer noch die playlist selbst dabei ist
            unsupportedFiles = unsupportedFiles + '\n' + element
            print("unsupported file format")
            continue
        if element.endswith(".m3u"):
            continue
        playlist.append(element)
    if unsupportedFiles != "":
        message(2,addToPlaylist_message1_title_langtext,addToPlaylist_message1_text_langtext + unsupportedFiles,"ok",0)
    if playlist == []:
        return
    if rememberme == True:
        nextSong("add")
        return
    loading_stop()
    print("i wanna be a girl")
    updatePlaylist(-1,-1)

def addToPlaylistKey(event):
    addToPlaylist("no")

def updatePlaylist(selectCount,seeCount):#für selectionAndSee
    global tree
    global loadingWindow
    global plstSelSeeLabel
    global playlistLengthLabel
    global remainingPlaylistLengthLabel
    global plW
    global miniModeActive
    global plWminiMode
    global treeMiniMode
    global remainingPlaylistLengthLabelMini
    print("update playlist")
    print("hree loading threading updateplaylist")
    loading_Threading()
    if miniModeActive.get() == False:
        plW.title(updatePlaylist_plW_title_langtext)
    elif miniModeActive.get() == True:
        plWminiMode.title(updatePlaylist_plWminiMode_title_langtext)
#    loadingThreading()
    row_number = 1
    print("why u not doing anything?!?")
    if miniModeActive.get() == False:
        print("okay here u should do smth")
        for item in tree.get_children():
            tree.delete(item)
        playlistLengthLabel.config(text = updatePlaylist_playlistLengthLabel_text_langtext)
        remainingPlaylistLengthLabel.config(text = updatePlaylist_remainingPlaylistLengthLabel_text_langtext)
        for pSong in pPlaylist:#played song
            print("here it should fill the treeee")
            Title = getSongName(pSong)
            Artist = getSongArtist(pSong)
            #length = getSongLength(pSong)
            tree.insert('',tk.END,values = (Title,Artist,tree_loading_text_langtext,row_number))
            row_number = row_number + 1
        for song in playlist:
            Title = getSongName(song)
            Artist = getSongArtist(song)
            #length = getSongLength(song)
            tree.insert('',tk.END,values = (Title,Artist,tree_loading_text_langtext,row_number))
            row_number = row_number + 1
    elif miniModeActive.get() == True:
        for item in treeMiniMode.get_children():
            treeMiniMode.delete(item)
        remainingPlaylistLengthLabelMini.config(text = updatePlaylist_remainingPlaylistLengthLabelMini_text_langtext)
        for pSong in pPlaylist:#played song
            Title = getSongName(pSong)
            Artist = getSongArtist(pSong)
            #length = getSongLength(pSong)
            treeMiniMode.insert('',tk.END,values = (Title,Artist,treeMiniMode_loading_text_langtext,row_number))
            row_number = row_number + 1
        for song in playlist:
            Title = getSongName(song)
            Artist = getSongArtist(song)
            #length = getSongLength(song)
            treeMiniMode.insert('',tk.END,values = (Title,Artist,treeMiniMode_loading_text_langtext,row_number))
            row_number = row_number + 1
    plstSelSee(selectCount,seeCount)
#    loadingWindow.destroy()
    #for item_id in items:
    #    tree.item(item_id,values = (row_number *tree.item(item_id,"values")[1:]))
    #    row_number = row_number + 1
    #for index, item_id in enumerate(items, start=1):
    #    tree.item(item_id, values=(index, tree.item(item_id, "values")[1]))
    #for item_id in items:
    #    values = tree.item(item_id,"values")
    #    if values and values[0] == str(len(pPlaylist) + 1):
    #        tree.selection_set(item_id)
    #        return
    loading_stop()
    updatePlaylistThread()

def plstSelSee(selectCount,seeCount):#plstSelSee = plstSelSeeAndSee;0 = none; -1 = last
    global tree
    global treeMiniMode
    global playlist
    global pPlaylist
    global miniModeActive
    global playlistSelectionLabelMini
    if miniModeActive.get() == False:
        items = tree.get_children()
        for item_id in items:
            tree.item(item_id,tags = ("not_playing"))
            values = tree.item(item_id,"values")
            if values[3] == str(len(pPlaylist) + 1):
                #tree.selection_set(item_id)
                #tree.see(item_id)
                tree.item(item_id,tags = ("playing"))
                playlistSelection = str(len(pPlaylist) + 1) + "/" + str(len(pPlaylist) + len(playlist))
                plstSelectionLabel.config(text = playlistSelection)
            if values[3] == str(selectCount):
                tree.selection_set(item_id)
            if values[3] == str(seeCount):
                tree.see(item_id)
            elif selectCount == -1:
                if values[3] == str(len(pPlaylist) + len(playlist)):
                    tree.selection_set(item_id)
            elif seeCount == -1:
                if values[3] == str(len(pPlaylist) + len(playlist)):
                    tree.see(item_id)
    elif miniModeActive.get() == True:
        items = treeMiniMode.get_children()
        for item_id in items:
            treeMiniMode.item(item_id,tags = ("not_playing"))
            values = treeMiniMode.item(item_id,"values")
            if values[3] == str(len(pPlaylist) + 1):
                #tree.selection_set(item_id)
                #tree.see(item_id)
                treeMiniMode.item(item_id,tags = ("playing"))
                playlistSelection = str(len(pPlaylist) + 1) + "/" + str(len(pPlaylist) + len(playlist))
                playlistSelectionLabelMini.config(text = playlistSelection)
            if values[3] == str(selectCount):
                treeMiniMode.selection_set(item_id)
            if values[3] == str(seeCount):
                treeMiniMode.see(item_id)
            elif selectCount == -1:
                if values[3] == str(len(pPlaylist) + len(playlist)):
                    treeMiniMode.selection_set(item_id)
            elif seeCount == -1:
                if values[3] == str(len(pPlaylist) + len(playlist)):
                    treeMiniMode.see(item_id)

def updatePlaylistThread():
    length_for_playlist_thread = Thread(target = length_for_playlist)
    length_for_playlist_thread.start()

def length_for_playlist():
    global tree
    global treeMiniMode
    global loadingWindow
    global playlistLengthLabel
    global remainingPlaylistLengthLabel
    global remainingPlaylistLengthLabelMini
    global plW
    global plWminiMode
    global plWtitleNameTrue
    global plWtitleName
    global miniModeActive
    print("length for playlist")
    print("here loading thre<ding length forplaylist")
    loading_Threading()
    if miniModeActive.get() == False:
        plW.title(length_for_playlist_plW_title_langtext)
    elif miniModeActive.get() == True:
        plWminiMode.title(length_for_playlist_plWminiMode_title_langtext)
    notFound = ""
    notFoundList1 = []
    notFoundList2 = []
    try:
        if miniModeActive.get() == False:
            items = tree.get_children()
            count = 0
            playlistLengthSec = 0#insgesamte länge der playlist
            remainingPlaylistLengthSec = 0
            for pSong in pPlaylist:
                #print("pPlaylist")
                if pSong.endswith('.m3u'):
                    break
                try:
                    length,songLengthSec = getSongLength(pSong)
                    playlistLengthSec = playlistLengthSec + songLengthSec
                except:
                    notFoundList1.append[pSong]
                    notFound = notFound + '\n' + pSong
                    #continue
                item_id = items[count]
                tree.item(item_id,values = (tree.item(item_id,"values")[0],tree.item(item_id,"values")[1],length,tree.item(item_id,"values")[3]))
                count = count + 1
            for song in playlist:
                #print("playlist")
                if song.endswith('.m3u'):
                    break
                try:
                    length,songLengthSec = getSongLength(song)
                    playlistLengthSec = playlistLengthSec + songLengthSec
                    remainingPlaylistLengthSec = remainingPlaylistLengthSec + songLengthSec
                except:
                    notFoundList2.append(song)
                    notFound = notFound + '\n' + song
                    #continue
                try:
                    item_id = items[count]#der letzte ist immer zu hoch, keine ahnung warum
                except:
                    pass
                tree.item(item_id,values = (tree.item(item_id,"values")[0],tree.item(item_id,"values")[1],length,tree.item(item_id,"values")[3]))
                count = count + 1
            playlistLength = str(datetime.timedelta(seconds = playlistLengthSec))
            remainingPlaylistLength = str(datetime.timedelta(seconds = remainingPlaylistLengthSec))
            dot = playlistLength.rfind(".")
            if dot != -1:
                playlistLength = playlistLength[:dot]
            playlistLengthLabel.config(text = playlistLength)
            dot = remainingPlaylistLength.rfind(".")
            if dot != -1:
                remainingPlaylistLength = remainingPlaylistLength[:dot]
            remainingPlaylistLengthLabel.config(text = remainingPlaylistLength)
            for song in notFoundList2[::-1]:
                #print(playlist[count])
                try:
                    playlist.remove(song)
                except:
                    pass
            for pSong in notFoundList1[::-1]:
                #print(pPlaylist[count])
                try:
                    pPlaylist.remove(pSong)
                except:
                    pass
            if notFoundList1 != [] or notFoundList2 != []:
                message(2,length_for_playlist_message1_title_langtext,length_for_playlist_message1_text_langtext + notFound,"ok",0)
                loading_stop()
                print("update playlust new started")
                updatePlaylist(0,0)
        if miniModeActive.get() == True:
            items = treeMiniMode.get_children()
            count = 0
            playlistLengthSec = 0#insgesamte länge der playlist
            remainingPlaylistLengthSec = 0
            for pSong in pPlaylist:
                #print("pPlaylist")
                if pSong.endswith('.m3u'):
                    break
                try:
                    length,songLengthSec = getSongLength(pSong)
                    playlistLengthSec = playlistLengthSec + songLengthSec
                except:
                    notFoundList1.append[pSong]
                    notFound = notFound + '\n' + pSong
                    #continue
                item_id = items[count]
                treeMiniMode.item(item_id,values = (treeMiniMode.item(item_id,"values")[0],treeMiniMode.item(item_id,"values")[1],length,treeMiniMode.item(item_id,"values")[3]))
                count = count + 1
            for song in playlist:
                #print("playlist")
                if song.endswith('.m3u'):
                    break
                try:
                    length,songLengthSec = getSongLength(song)
                    playlistLengthSec = playlistLengthSec + songLengthSec
                    remainingPlaylistLengthSec = remainingPlaylistLengthSec + songLengthSec
                except:
                    notFoundList2.append(song)
                    notFound = notFound + '\n' + song
                    #continue
                try:
                    item_id = items[count]#der letzte ist immer zu hoch, keine ahnung warum
                except:
                    pass
                treeMiniMode.item(item_id,values = (treeMiniMode.item(item_id,"values")[0],treeMiniMode.item(item_id,"values")[1],length,treeMiniMode.item(item_id,"values")[3]))
                count = count + 1
            playlistLength = str(datetime.timedelta(seconds = playlistLengthSec))
            remainingPlaylistLength = str(datetime.timedelta(seconds = remainingPlaylistLengthSec))
            dot = playlistLength.rfind(".")
            if dot != -1:
                playlistLength = playlistLength[:dot]
            dot = remainingPlaylistLength.rfind(".")
            if dot != -1:
                remainingPlaylistLength = remainingPlaylistLength[:dot]
            remainingPlaylistLengthLabelMini.config(text = remainingPlaylistLength)
            for song in notFoundList2[::-1]:
                #print(playlist[count])
                try:
                    playlist.remove(song)
                except:
                    pass
            for pSong in notFoundList1[::-1]:
                #print(pPlaylist[count])
                try:
                    pPlaylist.remove(pSong)
                except:
                    pass
            if notFoundList1 != [] or notFoundList2 != []:
                message(2,length_for_playlist_message2_title_langtext,length_for_playlist_message2_text_langtext + notFound,"ok",0)
                loading_stop()
                print("update playlist neuzustarten")
                updatePlaylist(0,0)
    except Exception as e:
        loading_stop()
        print(e)

    if miniModeActive.get() == False:
        if plWtitleNameTrue:
            plW.title(plWtitleName)
            loading_stop()
            return
        plW.title("Playlist")
    elif miniModeActive.get() == True:
        if plWtitleNameTrue:
            plWminiMode.title(plWtitleName)
            loading_stop()
            return
        plWminiMode.title("Playlist")
    print("length for playliust finished")
    loading_stop()

def remainingLength(ForB):#okay hier wird das noch ein problem wenn ich nicht die gesamte länge anzeige
    global remainingPlaylistLengthLabel
    global playlistLengthLabel
    remainingPlaylistLengthOld = remainingPlaylistLengthLabel["text"]
    playlistLength = playlistLengthLabel["text"]
    song = playlist[0]
    if ForB == "fst":
        remainingLength = playlistLength
        remainingPlaylistLengthLabel.config(text = remainingLength)
        return
    elif ForB == "lst":
        _,remainingLengthSec = getSongLength(song)
        remainingLength = str(datetime.timedelta(seconds = remainingLengthSec))
        dot = remainingLength.rfind(".")
        if dot != -1:
            remainingLength = remainingLength[:dot]
        remainingPlaylistLengthLabel.config(text = remainingLength)
        return
    try:
        print("excepting")
        whereSpace = remainingPlaylistLengthOld.find(" ")
        print("printing days now")
        print(whereSpace)
        days = remainingPlaylistLengthOld[:whereSpace - 1]
        print(days)
        hours, minutes, seconds = map(int, remainingPlaylistLengthOld[-8:].split(':'))
        remainingLengthSecOld = days * 86400 + hours * 3600 + minutes * 60 + seconds
    except:
        hours, minutes, seconds = map(int, remainingPlaylistLengthOld.split(':'))
        remainingLengthSecOld = hours * 3600 + minutes * 60 + seconds
    length,songLengthSec = getSongLength(song)
    if ForB == "f":
        remainingLengthSec = remainingLengthSecOld - songLengthSec
    if ForB == "b":
        remainingLengthSec = remainingLengthSecOld + songLengthSec
    remainingLength = str(datetime.timedelta(seconds = remainingLengthSec))
    dot = remainingLength.rfind(".")
    if dot != -1:
        remainingLength = remainingLength[:dot]
    remainingPlaylistLengthLabel.config(text = remainingLength)

def playFromPlaylist():
    global miniModeActive
    if miniModeActive.get() == False:
        selectedItems = tree.selection()
    elif miniModeActive.get() == True:
        selectedItems = tree.selection()
    if len(selectedItems) > 1 or len(selectedItems) == 0:
        return
    if miniModeActive.get() == False:
        selectedRow = tree.item(selectedItems)
    elif miniModeActive.get() == True:
        selectedRow = tree.item(selectedItems)
    values = selectedRow['values']
    count = values[3]
    if count - len(pPlaylist) - 1 == 0:
        return
    if count <= len(pPlaylist):
        pCount = len(pPlaylist) - count#playlist count
        while pCount + 1 > 0:
            playlist.insert(0,pPlaylist[-1])
            del pPlaylist[-1]
            pCount = pCount - 1
    else:
        pCount = count - len(pPlaylist)
        while pCount > 1:
            pPlaylist.append(playlist[0])
            del playlist[0]
            pCount = pCount - 1
    nextSong("play")

def playFromPlaylistEvent(event):
    playFromPlaylist()

def delFrompllst():#delete from playlist
    global miniModeActive
    if miniModeActive.get() == False:
        selectedItems = tree.selection()
    elif miniModeActive.get() == True:
        selectedItems = treeMiniMode.selection()
    if len(selectedItems) == 0:
        return
    counts = []
    for item in selectedItems:
        if miniModeActive.get() == False:
            selectedRow = tree.item(item)
        elif miniModeActive.get() == True:
            selectedRow = treeMiniMode.item(item)
        values = selectedRow['values']
        count = values[3]
        counts.append(count)
    counts.reverse()
    for count in counts:
        if count <= len(pPlaylist):
            del pPlaylist[count - 1]
        elif count - len(pPlaylist) - 1 == 0:
            del playlist[0]
            nextSong("del")
        else:
            del playlist[count - len(pPlaylist) - 1]
    updatePlaylist(0,0)
    #pS = 0
    #for item in selectedItems:
    #    selectedRow = tree.item(item)
    #    values = selectedRow['values']
    #    print(values)
    #    count = values[3]
    #    if count <= len(pPlaylist) - pS:#playlist shortener
    #        del pPlaylist[count - 1]
    #        rememberme = False
    #        pS = pS + 1
    #    else:
    #        if count - len(pPlaylist) - 1 == 0:
    #           rememberme = True
    #       else:
    #            rememberme = False
    #        del playlist[count - len(pPlaylist) - 1]
    #    updatePlaylist(selectCount)
    #if rememberme == True:
    #    nextSong()

def delFrompllstKey(event):
    delFrompllst()

def delDuplicates():#noch fixen
    global song
    global playlist
    global pPlaylist
#    bPlaylist = pPlaylist + playlist#big playlist
#    nPlaylist = []#new playlist
#    [nPlaylist.append(item) for item in bPlaylist if item not in nPlaylist]
#    where = nPlaylist.index(song)
#    pPlaylist = nPlaylist[:where]
#    playlist = nPlaylist[where:]
    checkElement = []
    newPp = []
    newP = []
    for element in pPlaylist:#musst dir was ausdenken, was passiert wenn ein song abgespielt wird der gerade gelöscht wurde
    #mb kann dann entweder zum ersten vorkommen dieses songs gespielt werden oder man muss sich irgendwie anders merken wo der dann hin soll
        try:
            place = checkElement.index(element)#vlt brauche ich place für die idee da unten irgendwann nochmal
        except:
            newPp.append(element)
            checkElement.append(element)
    for element in playlist:
        try:
            print("trying")
            place = checkElement.index(element)
        except:
            print("except")
            newP.append(element)
            checkElement.append(element)
    pPlaylist = []
    playlist = []
    for element in newPp:
        pPlaylist.append(element)
    for element in newP:
        playlist.append(element)
    updatePlaylist(0,0)#noch etwas hinzufügen, dass wenn ein duplikat gerade abgespielt wird, entweder zum nächsten song geskippt wird, oder das gecheckt wird und wenn das der fall ist, eine weitere option erscheint. generell könnte man aber auch eine option machen, die fragt, ob immer das erste vorkommnis oder ein anderes genommen werden soll

def deleteAllSongs():
    global playlist
    global pPlaylist
    playlist = []
    pPlaylist = []
    togglePlay()
    updatePlaylist(0,0)

def savePlaylist():
    global playlist
    global pPlaylist
    global miniModeActive
    #global progressPercent
    #progress()
    #progressPercent = 100 / (len(playlist) + len(pPlaylist) + 2)
    saveThere,selectedFilter = saveFileDialog()
    if saveThere == "":
        return
    elif "(*.m3u)" in selectedFilter:
        extension = ".m3u"
    elif "(*.m3u8)" in selectedFilter:
        extension = ".m3u8"
    elif "(*.txt)" in selectedFilter:
        extension = ".txt"
    if saveThere.endswith(extension) == False:
        saveThere = saveThere + extension
    lastSlash = saveThere.rfind("/")
    if saveThere.endswith(".m3u"):
        pllstformat = "m3u"
    elif saveThere.endswith(".m3u8"):
        pllstformat = "m3u8"
    playlistName = saveThere[lastSlash + 1:]
    try:#falls die playlist schon existiert, dass man sie ordentlich überschreiben kann
        with open(saveThere,"r") as file:
            lines = file.readlines()
    #    makeProgress()
        lines = []
        with open(saveThere,"w") as file:
            file.writelines(lines)
    #    makeProgress()
    except:
    #    makeProgress()
    #    makeProgress()
        pass
    for element in pPlaylist:
        with open(saveThere, "a") as f:
            f.write(element + '\n')
    for element in playlist:
        with open(saveThere, "a") as f:
            f.write(element + '\n')
    if miniModeActive.get() == False:
        plW.title(playlistName)
    elif miniModeActive.get() == True:
        plWminiMode.title(playlistName)
    recentFiles.insert(0,saveThere + '\n')
    recentPlaylists.insert(0,saveThere + '\n')
    message(1,savePlaylist_message1_title_langtext,savePlaylist_message1_text1_langtext + playlistName + savePlaylist_message1_text2_langtext,"nope",2000)

def upInPlaylist():
    global loopMove
    global playlist
    global pPlaylist
    global miniModeActive
    if miniModeActive.get() == False:
        selectedItems = tree.selection()
    elif miniModeActive.get() == True:
        selectedItems = treeMiniMode.selection()
    if len(selectedItems) == 0:
        return
    for item in selectedItems:
        if miniModeActive.get() == False:
            selectedRow = tree.item(item)
        elif miniModeActive.get() == True:
            selectedRow = treeMiniMode.item(item)
        values = selectedRow['values']
        count = values[3]
        if count == 1 and loopMove.get() == False:
            message(1,upInPlaylist_message1_title_langtext,upInPlaylist_message1_text_langtext,"customSettings,settings;No,nope",5000)
            continue
        elif count == 1 and loopMove.get() == True:
            if count == len(pPlaylist) + 1:
                for element in playlist:
                    pPlaylist.append(element)
                playlist = []
                playlist.append(pPlaylist[0])
                del pPlaylist[0]
                selectCount = len(pPlaylist) + len(playlist)
            else:
                playlist.append(pPlaylist[0])
                del pPlaylist[0]
                selectCount = len(pPlaylist) + len(playlist)
        elif count <= len(pPlaylist):
            pPlaylist.insert(count - 1 - 1,pPlaylist[count - 1])
            del pPlaylist[count]
            selectCount = count - 1
        elif count == len(pPlaylist) + 1:
            playlist.insert(1,pPlaylist[-1])
            del pPlaylist[-1]
            selectCount = len(pPlaylist) + 1
        elif count == len(pPlaylist) + 2:
            pPlaylist.append(playlist[1])
            del playlist[1]
            selectCount = len(pPlaylist)
        else:
            playlist.insert(count - 1 - 1 - len(pPlaylist),playlist[count - 1 - len(pPlaylist)])
            del playlist[count - len(pPlaylist)]
            selectCount = count - 1
    updatePlaylist(selectCount,selectCount)

def upInPlaylistKey(event):
    upInPlaylist()

def downInPlaylist():
    global loopMove
    global playlist
    global pPlaylist
    global miniModeActive
    if miniModeActive.get() == False:
        selectedItems = tree.selection()
    elif miniModeActive.get() == True:
        selectedItems = treeMiniMode.selection()
    if len(selectedItems) == 0:
        return
    for item in selectedItems:
        if miniModeActive.get() == False:
            selectedRow = tree.item(item)
        elif miniModeActive.get() == True:
            selectedRow = treeMiniMode.item(item)
        values = selectedRow['values']
        count = values[3]
        if count == len(pPlaylist) + len(playlist) and loopMove.get() == False:
            message(1,downInPlaylist_message1_title_langtext,downInPlaylist_message1_text_langtext,"customSettings,settings;No,nope",5000)#hier im uwu mode einen bottom witz machen xD, so wie: at the bottom (like me), idk, nur wenns funktioniert
            continue
        elif count == len(pPlaylist)  + len(playlist) and loopMove.get() == True:
            if count == len(pPlaylist) + 1:
                for element in pPlaylist:
                    playlist.append(element)
                pPlaylist = []
                selectCount = 1
            else:
                pPlaylist.insert(0,playlist[-1])
                del playlist[-1]
                selectCount = len(pPlaylist) + 1
        elif count < len(pPlaylist):
            pPlaylist.insert(count - 1,pPlaylist[count])
            del pPlaylist[count + 1]
            selectCount = count + 1
        elif count == len(pPlaylist):
            playlist.insert(1,pPlaylist[-1])
            del pPlaylist[-1]
            selectCount = len(pPlaylist) + 1 + 1
        elif count == len(pPlaylist) + 1:
            pPlaylist.append(playlist[1])
            del playlist[1]
            selectCount = len(pPlaylist)
        else:
            playlist.insert(count - len(pPlaylist) + 1,playlist[count - len(pPlaylist) - 1])
            del playlist[count - len(pPlaylist) - 1]
            selectCount = count + 1
    updatePlaylist(selectCount,selectCount)

def downInPlaylistKey(event):
    downInPlaylist()

def topInPlaylist():
    global playlist
    global pPlaylist
    global miniModeActive
    if miniModeActive.get() == False:
        selectedItems = tree.selection()
    elif miniModeActive.get() == True:
        selectedItems = treeMiniMode.selection()
    if len(selectedItems) == 0 or len(selectedItems) < 1:#nur vorläufig so machen, später einen fix dafür rausbringen, dass man mehrere selecten kann. vielleicht irgendwie mit einem counter track behalten, wie viele items nach unten die anderen items gerutscht sind.
        return
    for item in selectedItems:
        if miniModeActive.get() == False:
            selectedRow = tree.item(item)
        elif miniModeActive.get() == True:
            selectedRow = treeMiniMode.item(item)
        values = selectedRow['values']
        count = values[3]
        if count == 1:
            continue
        if count == len(pPlaylist) + 1:
            rCount = len(pPlaylist) - 1
            for song in pPlaylist:
                playlist.insert(1,pPlaylist[rCount])
                rCount = rCount - 1
            pPlaylist = []
        elif count <= len(pPlaylist):
            pPlaylist.insert(0,pPlaylist[count - 1])
            del pPlaylist[count]
        else:
            pPlaylist.insert(0,playlist[count - len(pPlaylist) - 1])
            del playlist[count - len(pPlaylist) - 1]
    updatePlaylist(1,1)

def topInPlaylistKey(event):
    topInPlaylist()

def bottomInPlaylist():
    global playlist
    global pPlaylist
    global miniModeActive
    if miniModeActive.get() == False:
        selectedItems = tree.selection()
    elif miniModeActive.get() == True:
        selectedItems = treeMiniMode.selection()
    if len(selectedItems) == 0 or len(selectedItems) < 1:#nur vorläufig so machen, später einen fix dafür rausbringen, dass man mehrere selecten kann. vielleicht irgendwie mit einem counter track behalten, wie viele items nach oben die anderen items gerutscht sind.
        return
    for item in selectedItems:
        if miniModeActive.get() == False:
            selectedRow = tree.item(item)
        elif miniModeActive.get() == True:
            selectedRow == treeMiniMode.item(item)
        values = selectedRow['values']
        count = values[3]
        if count == len(playlist) + len(pPlaylist):
            continue
        if count == len(pPlaylist) + 1:
            for song in playlist:
                pPlaylist.append(song)
            playlist = []
            playlist.append(pPlaylist[count - 1])
            del pPlaylist[count - 1]
        elif count <= len(pPlaylist):
            playlist.append(pPlaylist[count - 1])
            del pPlaylist[count - 1]
        else:
            playlist.append(playlist[count - len(pPlaylist) - 1])
            del playlist[count - len(pPlaylist) - 1]
    updatePlaylist(len(pPlaylist) + len(playlist),len(pPlaylist) + len(playlist))

def bottomInPlaylistKey(event):
    bottomInPlaylist()

def shufflePlaylist():
    global playlist
    global pPlaylist
    global shuffleReset
    if playlist == [] and pPlaylist == []:
        return
    pSong = []
    pSong.append(playlist[0])
    del playlist[0]
    if shuffleReset.get() == True:
        count = len(pPlaylist)
        while count > 0:
            playlist.append(pPlaylist[0])
            del pPlaylist[0]#nicht einfach del pPlaylist, weil sonst die variable selbst gelöscht wird
            count = count - 1
        random.shuffle(playlist)
        playlist.insert(0,pSong[0])
        updatePlaylist(1,1)
    else:
        random.shuffle(playlist)
        random.shuffle(pPlaylist)
        playlist.insert(0,pSong[0])
        updatePlaylist(len(pPlaylist) + 1,len(pPlaylist) + 1)

def changeVolume(event):
    global volumePressed
    global volumeText
    if volumePressed == True:
        volumeText = volume.get()
        volumeText = 100 - volumeText
        player.audio_set_volume(volumeText)
        try:
            volumeInfo.config(text = volumeText)
        except:
            pass
        try:
            volumeInfoExtra.config(text = volumeText)
        except:
            pass

def changeVolumeUpKey(event):
    volumeText = volume.get()
    if volumeText > 0:
        volume.set(volumeText - 1)
        volumeText = 100 - volumeText
        player.audio_set_volume(volumeText + 1)
        #volumeSlider.set(volumeText)#geht automatisch
        volumeInfo.config(text = volumeText + 1)

def changeVolumeDownKey(event):
    volumeText = volume.get()
    if volumeText < 100:
        volume.set(volumeText + 1)
        volumeText = 100 - volumeText
        player.audio_set_volume(volumeText - 1)
        #volumeSlider.set(volumeText)#geht automatisch
        volumeInfo.config(text = volumeText - 1)

def volumePressedTrue(event):
    global volumePressed
    volumePressed = True

def volumePressedFalse(event):
    global volumePressed
    volumePressed = False
    filepath = os.path.join(dirname,"texts/settings.txt")
    with open(filepath,'r') as file:
        lines = file.readlines()
    volumeText = volume.get()
    lines[0] = str(100 - volumeText) + '\n'
    with open(filepath,'w') as file:
        file.writelines(lines)

#for extra window space
#def makeWindowBigger():
#    global main_windowWidth
#    while main_windowWidth < 100:
#        main_windowWidth = main_windowWidth + 1
#        main_windowWidthStr = str(main_windowWidth)
#        main_window.geometry(main_windowWidthStr + 'x360+100+100')

#system functions
def infoWE():
    extraWindow.title(infoWE_extraWindow_title_langtext)
    versionFrame = ttk.Frame(extraWindow)
    versionFrame.pack(side = tk.BOTTOM,fill = tk.X)
    licenseAttributionFrame = ttk.Frame(extraWindow)
    licenseAttributionFrame.pack(side = tk.TOP,fill = tk.X)
    changelogButton = ttk.Button(versionFrame,text = infoWE_changelogButton_text_langtext,command = lambda: (windowExtra("Changelog")))
    changelogButton.pack(side = tk.RIGHT)
    version = ttk.Label(versionFrame,text = "Version 1.0_1 BETA 11_1")
    version.pack(fill = tk.X)
    attributions = ttk.Button(licenseAttributionFrame,text = infoWE_attributions_text_langtext,command = lambda: (windowExtra("attributions")))
    attributions.pack(side = tk.RIGHT)
    licenseButton = ttk.Button(licenseAttributionFrame,text = infoWE_licenseButton_text_langtext,command = lambda: (windowExtra("License")))
    licenseButton.pack(side = tk.LEFT)#,fill = tk.X)
    licenseText = ttk.Label(licenseAttributionFrame,text = "GLP Version 2")
    licenseText.pack()#fill = tk.X,anchor = tk.CENTER)
    bSeparator = ttk.Separator(extraWindow,orient = 'horizontal')#bottom separator
    bSeparator.pack(side = tk.BOTTOM,fill = tk.X)
    filepath = os.path.join(dirname,"texts/info.txt")
    with open(filepath,'r') as file:
        lines = file.readlines()
    infoTextText = ""
    for line in lines:
        infoTextText = infoTextText + line
    infoText = ScrolledText(extraWindow,wrap = "word")#padding war vorher (10,0,0,0)
    infoText.pack(fill = tk.BOTH,side = tk.BOTTOM,anchor = tk.NW)
    infoText.insert(tk.INSERT,infoTextText)
    infoText.config(state = 'disabled',font = 'Helvetica 9')

def settingsWE():
    extraWindow.title(settingsWE_extraWindow_title_langtext)
    twoWindowsCheckbutton = ttk.Checkbutton(extraWindow,text = settingsWE_twoWindowsCheckbutton_text_langtext,command = lambda: (settings("twoWindows")),variable = twoWindows,onvalue = True,offvalue = False)
    twoWindowsCheckbutton.pack(side = tk.TOP,anchor = tk.NW)
    showVolumeInfoCheckbutton = ttk.Checkbutton(extraWindow,text = settingsWE_showVolumeInfoCheckbutton_text_langtext,command = lambda: (settings("volumeSliderText")),variable = volumeSliderTextOnOff,onvalue = True,offvalue = False)
    showVolumeInfoCheckbutton.pack(side = tk.TOP,anchor = tk.NW)
    loopPlaylistCheckbutton = ttk.Checkbutton(extraWindow,text= settingsWE_loopPlaylistCheckbutton_text_langtext,command = lambda: (settings("loopPlaylist")),variable = loopPlaylist,onvalue = True,offvalue = False)
    loopPlaylistCheckbutton.pack(side = tk.TOP,anchor = tk.NW)
    loopMoveCheckbutton = ttk.Checkbutton(extraWindow,text = settingsWE_loopMoveCheckbutton_text_langtext,command = lambda: (settings("loopMove")),variable = loopMove,onvalue = True,offvalue = False)
    loopMoveCheckbutton.pack(side = tk.TOP,anchor = tk.NW)
    filesToKeepSpinbox = ttk.Spinbox(extraWindow,from_ = 0, to = 20,textvariable = filesToKeep,command = filesToKeepChanged)
    filesToKeepSpinbox.pack(side = tk.TOP,anchor = tk.NW)
    shufflePositionResetCheckbutton = ttk.Checkbutton(extraWindow,text = settingsWE_shufflePositionResetCheckbutton_text_langtext,command = lambda: (settings("shuffleReset")),variable = shuffleReset,onvalue = True,offvalue = False)
    shufflePositionResetCheckbutton.pack(side = tk.TOP,anchor = tk.NW)
    languageSelectOptionMenu = ttk.OptionMenu(extraWindow,languageStringVar,None,*languageListOptionMenu,direction = 'above',command = languageChange)#container,variable,default,values
    languageSelectOptionMenu.pack(side = tk.TOP,anchor = tk.NW)
    messageLogsButton = ttk.Button(extraWindow,text = settingsWE_messageLogsButton_text_langtext,command = lambda: (windowExtra("messageLogs")))
    messageLogsButton.pack(side = tk.BOTTOM,anchor = tk.W)

def messageLogsWE():
    global logs
    global selectedLog
    global messageInfoLog
    global messageWarningLog
    global messageErrorLog
    global tree1
    global tree2
    global tree3
    extraWindow.title(messageLogsWE_extraWindow_title_langtext)
    logs = ttk.Notebook(extraWindow)
    logs.pack(fill = tk.BOTH)
    info = ttk.Frame(logs)
    warning = ttk.Frame(logs)
    error = ttk.Frame(logs)
    logs.add(info,text = messageLogsWE_logs_add1_text_langtext)
    logs.add(warning,text = messageLogsWE_logs_add2_text_langtext)
    logs.add(error,text = messageLogsWE_logs_add3_text_langtext)
    logs.bind('<<NotebookTabChanged>>',notebookTabChange)
    logs.select(selectedLog)
    columns = ('Title','Message','Buttons','Time','count')
    tree1 = ttk.Treeview(info,columns = columns,show = 'headings')
    tree2 = ttk.Treeview(warning,columns = columns,show = 'headings')
    tree3 = ttk.Treeview(error,columns = columns,show = 'headings')
    tree1.heading('Title',text = messageLogsWE_tree1_2_3_heading1_text_langtext)
    tree1.heading('Message',text = messageLogsWE_tree1_2_3_heading2_text_langtext)
    tree1.heading('Buttons',text = messageLogsWE_tree1_2_3_heading3_text_langtext)
    tree1.heading('Time',text = messageLogsWE_tree1_2_3_heading4_text_langtext)
    tree1.heading('count',text = messageLogsWE_tree1_2_3_heading5_text_langtext)
    tree1.column('Title',width = 100)
    tree1.column('Message',width = 200)
    tree1.column('Buttons',width = 50)
    tree1.column('Time',width = 50)
    tree1.column('count',width = 25)
    tree1.pack(side = tk.LEFT,fill = tk.BOTH)
    tree1.bind('<Motion>','break')
    tree1.bind('<Double-1>',messageLogClicked)
    #tree1.bind('<Enter>',messageLogClicked)
    tree2.heading('Title',text = messageLogsWE_tree1_2_3_heading1_text_langtext)
    tree2.heading('Message',text = messageLogsWE_tree1_2_3_heading2_text_langtext)
    tree2.heading('Buttons',text = messageLogsWE_tree1_2_3_heading3_text_langtext)
    tree2.heading('Time',text = messageLogsWE_tree1_2_3_heading4_text_langtext)
    tree2.heading('count',text = messageLogsWE_tree1_2_3_heading5_text_langtext)
    tree2.column('Title',width = 100)
    tree2.column('Message',width = 200)
    tree2.column('Buttons',width = 50)
    tree2.column('Time',width = 50)
    tree2.column('count',width = 25)
    tree2.pack(side = tk.LEFT,fill = tk.BOTH)
    tree2.bind('<Motion>','break')
    tree2.bind('<Double-1>',messageLogClicked)
    #tree2.bind('<Enter>',messageLogClicked)
    tree3.heading('Title',text = messageLogsWE_tree1_2_3_heading1_text_langtext)
    tree3.heading('Message',text = messageLogsWE_tree1_2_3_heading2_text_langtext)
    tree3.heading('Buttons',text = messageLogsWE_tree1_2_3_heading3_text_langtext)
    tree3.heading('Time',text = messageLogsWE_tree1_2_3_heading4_text_langtext)
    tree3.heading('count',text = messageLogsWE_tree1_2_3_heading5_text_langtext)
    tree3.column('Title',width = 100)
    tree3.column('Message',width = 200)
    tree3.column('Buttons',width = 50)
    tree3.column('Time',width = 50)
    tree3.column('count',width = 25)
    tree3.pack(side = tk.LEFT,fill = tk.BOTH)
    tree3.bind('<Motion>','break')
    tree3.bind('<Double-1>',messageLogClicked)
    #tree3.bind('<Enter>',messageLogClicked)
    scrollbar1_1 = ttk.Scrollbar(info,orient = tk.VERTICAL,command = tree1.yview)
    tree1.configure(yscroll = scrollbar1_1.set)
    scrollbar1_1.pack(side = tk.RIGHT,fill = tk.Y)
    scrollbar2_1 = ttk.Scrollbar(warning,orient = tk.VERTICAL,command = tree2.yview)
    tree2.configure(yscroll = scrollbar2_1.set)
    scrollbar2_1.pack(side = tk.RIGHT,fill = tk.Y)
    scrollbar3_1 = ttk.Scrollbar(error,orient = tk.VERTICAL,command = tree3.yview)
    tree3.configure(yscroll = scrollbar3_1.set)
    scrollbar3_1.pack(side = tk.RIGHT,fill = tk.Y)
    count = 1
    for element in range(0, len(messageInfoLog), 4):#von chatgpt (hatte anstelle von element i)
        elements = messageInfoLog[element:element + 4]
        tree1.insert('',tk.END,values = (elements[0],elements[1],elements[2],str(elements[3]) + "ms",count))
        count = count + 1
    count = 1
    for element in range(0,len(messageWarningLog),4):#(und hatte leerzeichen)
        elements = messageWarningLog[element:element + 4]
        tree2.insert('',tk.END,values = (elements[0],elements[1],elements[2],str(elements[3]) + "ms",count))
        count = count + 1
    count = 1
    for element in range(0,len(messageErrorLog),4):
        elements = messageErrorLog[element:element + 4]
        tree3.insert('',tk.END,values = (elements[0],elements[1],elements[2],str(elements[3]) + "ms",count))
        count = count + 1
    #wenn man nds ausgewählt hat (halt bei der song-/playlistauswahl sollte ich denke ich das logo von der warnung zur info machen
    #außerdem sollte ich gucken, ob ich nd aus infos, warnings und erros info messages warning messages und error messages amche, oder nur bei infos/info das messages ranhänge naja gute nacht, vergiss nd das morgen mitzunehmen

def attributionsWE():
    filepath = os.path.join(dirname,"texts/attributions.txt")
    with open(filepath,"r") as file:
        text = file.read()
    extraWindow.title(attributionsWE_extraWindow_title_langtext)
    attributionLinksButton = ttk.Button(extraWindow,text = attributionsWE_attributionLinksButton_text_langtext,command = lambda: (windowExtra("attributionButtons")))
    attributionLinksButton.pack(side = tk.BOTTOM,fill = tk.X)
    attributionsText = ScrolledText(extraWindow,wrap = "word")
    attributionsText.pack(fill = tk.BOTH,side = tk.BOTTOM,anchor = tk.NW)
    attributionsText.insert(tk.INSERT,text)
    attributionsText.config(state = 'disabled',font = 'Helvetica 9')

def attributionButtonsWE():#irgendwie mehrere seiten oder so machen (7 links passen auf eine seite)
    extraWindow.title(attributionButtonsWE_extraWindow_title_langtext)
    pageFrame = ttk.Frame(extraWindow)
    pageFrame.pack(side = tk.BOTTOM,fill = tk.X)
    buttonFrame = ttk.Frame(extraWindow)
    buttonFrame.pack(fill = tk.BOTH)
    buttons = ["https://icon-icons.com/","Icon-Icons","https://icon-icons.com/users/z1gHIAw5WHSQk4RJ0exyV/icon-sets/","Dirtyworks on Icon-Icons","https://www.flaticon.com","Flaticon","https://www.flaticon.com/authors/william-richon","William Richon on Flaticon","https://www.flaticon.com/authors/pixel-perfect","Pixel perfect","https://www.flaticon.com/authors/freepik","Freepik on Flaticon","https://www.flaticon.com/authors/karthiks-18","karthiks_18 on Flaticon","https://www.flaticon.com/authors/iconjam","Iconjam on Flaticon","https://www.flaticon.com/authors/iconjam","Iconjam","https://openclipart.org/artist/JoelM","JoelM","https://www.flaticon.com/authors/smashicons","Smashicons on FLaticon","https://www.videolan.org/","VideoLAN","https://github.com/dreamAviator","Me (dreamAviator) on GitHub"]
    bCount = len(buttons) // 2#buttons count
    while bCount > 0:
        bText = buttons[-1]
        del buttons[-1]
        url = buttons[-1]#button text
        del buttons[-1]
        bCount = bCount - 1
        attributionsButton = ttk.Button(buttonFrame,text = bText,command = functools.partial(openurl,url))
        attributionsButton.pack(side = tk.BOTTOM,fill = tk.X)

def changelogWE():
    extraWindow.title(changelogWE_extraWindow_title_langtext)
    text = ""
    filepath = os.path.join(dirname,"texts/changelog.txt")
    with open(filepath,'r') as file:
        lines = file.readlines()
    for line in lines:
        text = text + str(line)
    textLabel = ScrolledText(extraWindow,wrap = "word")
    textLabel.pack(fill = tk.BOTH,side = tk.BOTTOM,anchor = tk.NW)
    textLabel.insert(tk.INSERT,text)
    textLabel.config(state = 'disabled',font = 'Helvetica 9')

def licenseWE():
    extraWindow.title(licenseWE_extraWindow_title_langtext)
    text = ""
    filepath = os.path.join(dirname,"texts/license.txt")
    with open(filepath,'r') as file:
        lines = file.readlines()
    for line in lines:
        text = text + str(line)
    textLabel = ScrolledText(extraWindow,wrap = "word")
    textLabel.pack(fill = tk.BOTH,side = tk.BOTTOM,anchor = tk.NW)
    textLabel.insert(tk.INSERT,text)
    textLabel.config(state = 'disabled',font = 'Helvetica 9')

def openurl(url):
    webbrowser.open(url)

def windowExtra(extraType):
    global playlist
    global extraWindow
    global songCoverSmol
    global song_cover_image_smol
    global songLengthTextSmol
    global songNameTextSmol
    global songArtistTextSmol
    global togglePlayButtonSmol
    global songPositionTextSmol
    global left_image
    global Filename
    global toolbarFrameExtra
    global volumeInfoExtra
    global volumeSliderExtra
    global musicSliderExtra
    global songArtImageSmol
    #window
    try:
        song = playlist[0]
    except:
        pass
    songLength = "00:00"
    songArtist = songArtist_variable_langtext
    songName = songName_variable_langtext
    try:
        extraWindow.destroy()
    except:
        pass
    main_window.attributes('-alpha',0)
    extraWindow = tk.Toplevel()
    if extraType == "info" or extraType == "attributions" or extraType == "attributionButtons" or extraType == "Changelog" or extraType == "License":
        icon = info_icon
    elif extraType == "settings":
        icon = settings_icon
    elif extraType == "messageLogs":
        icon = message_icon
    main_window_size_etc = main_window.geometry()
    if platform.system() == "Windows":
        extraWindow.iconbitmap(icon)
    elif platform.system() == "Linux":
        extraWindow.iconphoto(False,icon)
    extraWindow.geometry(main_window_size_etc)
    extraWindow.bind('<Escape>',closeExtraEvent)
    extraWindow.bind('<space>',togglePlayKey)
    extraWindow.focus()
    extraWindow.protocol("WM_DELETE_WINDOW", closeExtra)
        #menus
    menubar3 = tk.Menu(extraWindow)
    extraWindow.config(menu = menubar3)
            #file_menu
    file_menu3 = tk.Menu(menubar3,tearoff = False)
    file_menu3.add_command(label = windowExtra_file_menu3_command1_label_langtext,command = lambda: (addToPlaylist("no")))
    sub_menu3 = tk.Menu(file_menu3,tearoff = False)
    file_menu3.add_cascade(label = windowExtra_file_menu3_cascade1_label_langtext,menu = sub_menu3)
    file_menu3.add_command(label = windowExtra_file_menu3_command2_label_langtext,command = savePlaylist)
    file_menu3.add_command(label = windowExtra_file_menu3_command3_label_langtext,command = deleteAllSongs)
    file_menu3.add_separator()
    file_menu3.add_command(label = windowExtra_file_menu3_command4_label_langtext,command = lambda: (windowExtra("settings")))
    file_menu3.add_separator()
    file_menu3.add_command(label=windowExtra_file_menu3_command5_label_langtext,command=exitProgram)
    menubar3.add_cascade(label=windowExtra_menubar3_cascade1_label_langtext,menu=file_menu3,underline=0)
            #view_menu
    view_menu3 = tk.Menu(menubar3,tearoff = False)
    view_menu3.add_command(label = windowExtra_view_menu3_command1_label_langtext,command = lambda: (settingsFmenu("volumeSliderText")))
    view_menu3.add_command(label = windowExtra_view_menu3_command2_label_langtext,command = lambda: (settingsFmenu("twoWindows")))
    view_menu3.add_command(label = windowExtra_view_menu3_command3_label_langtext,command = lambda: (settingsFmenu("miniMode")))
    menubar3.add_cascade(label = windowExtra_menubar3_cascade2_label_langtext,menu = view_menu3,underline = 0)
            #help_menu
    help_menu3 = tk.Menu(menubar3,tearoff = False)
    help_menu3.add_command(label = windowExtra_help_menu3_command1_label_langtext,command = lambda:(windowExtra("info")))
    help_menu3.add_command(label = windowExtra_help_menu3_command2_label_langtext,command = lambda:(windowExtra("Changelog")))
    help_menu3.add_command(label = windowExtra_help_menu3_command3_label_langtext,command = lambda:(windowExtra("License")))
    help_menu3.add_separator()
    help_menu3.add_command(label = windowExtra_help_menu3_command4_label_langtext,command = lambda:(windowExtra("settings")))
    help_menu3.add_command(label = windowExtra_help_menu3_command5_label_langtext,command = lambda:(windowExtra("messageLogs")))
    menubar3.add_cascade(label = "Help",menu = help_menu3,underline = 0)
    #
    refreshRecentFiles()
    #frames
    toolbarFrameExtra = ttk.Frame(extraWindow,width = 50)
    toolbarFrameExtra.pack(side = tk.LEFT,fill = tk.Y)
    musicControlFrameExtra = ttk.Frame(extraWindow,height = 50)
    musicControlFrameExtra.pack(side = tk.BOTTOM,fill = tk.X)
    musicInfoFrameExtra = ttk.Frame(extraWindow)
    musicInfoFrameExtra.pack(side = tk.BOTTOM,fill = tk.X)
    separator = ttk.Separator(extraWindow,orient = 'horizontal')
    separator.pack(side = tk.BOTTOM,fill = tk.X)
        #toolbar frame
    exitButton = tk.Button(toolbarFrameExtra,image = exit_button_image,command = exitProgram,borderwidth = 0)
    exitButton.pack(side = tk.BOTTOM,anchor = tk.S)
    if extraType == "settings" or extraType == "messageLogs":
        closeExtraButton = tk.Button(toolbarFrameExtra,image = left_image,command = closeExtra,borderwidth = 0)
        closeExtraButton.pack(side = tk.BOTTOM)
        infoButton = tk.Button(toolbarFrameExtra,image = info_button_image,command = lambda: (windowExtra("info")),borderwidth = 0)
        infoButton.pack(side = tk.BOTTOM)
    elif extraType == "info" or extraType == "attributions" or extraType == "attributionButtons" or extraType == "Changelog" or extraType == "License":
        settingsButton = tk.Button(toolbarFrameExtra,image = settings_button_image,command = lambda: (windowExtra("settings")),borderwidth = 0)
        settingsButton.pack(side = tk.BOTTOM)
        closeExtraButton = tk.Button(toolbarFrameExtra,image = left_image,command = closeExtra,borderwidth = 0)
        closeExtraButton.pack(side = tk.BOTTOM)
    if volumeSliderText == "True":
        volumeInfoExtra = ttk.Label(toolbarFrameExtra,text = volumeText)
        volumeInfoExtra.pack(side = tk.TOP)
    volumeSliderExtra = ttk.Scale(toolbarFrameExtra,variable = volume,from_ = 0,to = 100,orient = 'vertical')
    volumeSliderExtra.bind("<ButtonRelease-1>",volumePressedFalse)
    volumeSliderExtra.bind("<ButtonPress-1>",volumePressedTrue)
    volumeSliderExtra.bind("<Motion>",changeVolume)
    volumeSliderExtra.pack(side = tk.BOTTOM,fill = tk.Y,expand = True,pady = 10)
        #music control frame
    forwardButton = tk.Button(musicControlFrameExtra,image = forward_button_image_smol,command = fastForward,borderwidth = 0)
    forwardButton.pack(side = tk.RIGHT)
    togglePlayButtonSmol = tk.Button(musicControlFrameExtra,image = stop_image_smol,command = togglePlay,borderwidth = 0)
    togglePlayButtonSmol.pack(side = tk.RIGHT)
    rewindButton = tk.Button(musicControlFrameExtra,image = rewind_button_image_smol,command = rewindSong,borderwidth = 0)
    rewindButton.pack(side = tk.RIGHT)
    songCoverSmol = ttk.Label(musicControlFrameExtra,image = song_cover_image_smol)
    songCoverSmol.pack(side = tk.LEFT)
    musicSliderExtra = ttk.Scale(musicControlFrameExtra,variable = sliderVarExtra,from_ = 0,to = songLengthSeconds,orient = 'horizontal')
    musicSliderExtra.bind("<Motion>",sliderChangePos)
    musicSliderExtra.bind("<ButtonRelease-1>",sliderChange)
    musicSliderExtra.bind("<ButtonPress-1>",sliderPressedTrue)
    musicSliderExtra.pack(side = tk.BOTTOM,fill = tk.X,expand = True)
    songPositionTextSmol = ttk.Label(musicControlFrameExtra,text = songPosition)
    songPositionTextSmol.pack(side = tk.LEFT,anchor = tk.NW)
    songLengthTextSmol = ttk.Label(musicControlFrameExtra,text = songLength)
    songLengthTextSmol.pack(side = tk.RIGHT,anchor = tk.NE)
        #music info frame
    songArtistTextSmol = ttk.Label(musicInfoFrameExtra,text = songArtist)
    songArtistTextSmol.pack(side = tk.LEFT)
    songNameTextSmol = ttk.Label(musicInfoFrameExtra,text = songName)
    songNameTextSmol.pack(side = tk.RIGHT)
    try:
        songLength,songLengthSec = getSongLength(song)
        songArtist = getSongArtist(song)
        songName = getSongName(song)
        songArt = getSongArt(song)
        musicSliderExtra.config(to = songLengthSec)
        songLengthTextSmol.config(text = songLength)
        songLS = song.rfind("/")#song last slash
        songFilename = song[songLS + 1:]
        songArtistTextSmol.config(text = songArtist)
        songNameTextSmol.config(text = songName)
        if songArt != "nothing":
            songArtImage = tk.PhotoImage(file = 'song_cover_smol.png')
            songCoverSmol.config(image = songArtImage)
            songCoverSmol.image = songArtImage
        if songArtist == 'unknown':
            songArtistTextSmol.config(text = songFilename)
            if songName == 'unknown':
                songNameTextSmol.config(text = '')
            else:
                songNameTextSmol.config(text = songName)
        elif songName == 'unknown':
            songNameTextSmol.config(text = songFilename)
    except:
        pass
    checkLogoInverted()
    headline = ttk.Label(extraWindow,text = "",font = (14))
    headline.pack(side = tk.TOP)
    headlineSeparator = ttk.Separator(extraWindow,orient = 'horizontal')
    headlineSeparator.pack(side = tk.TOP,fill = tk.X)
    if extraType == "info":
        headline.config(text = windowExtra_extraType_info_headline_text_langtext)
        infoWE()
    elif extraType == "settings":
        headline.config(text = windowExtra_extraType_settings_headline_text_langtext)
        settingsWE()
    elif extraType == "messageLogs":
        headline.config(text = windowExtra_extraType_messageLogs_headline_text_langtext)
        backButton = ttk.Button(extraWindow,text = windowExtra_extraType_messageLogs_backButton_text_langtext,command = lambda: (windowExtra("settings")))
        backButton.pack(side = tk.TOP,fill = tk.X)
        messageLogsWE()
    elif extraType == "attributions":
        headline.config(text = windowExtra_extraType_attributions_headline_text_langtext)
        backButton = ttk.Button(extraWindow,text = windowExtra_extraType_attributions_backButton_text_langtext,command = lambda: (windowExtra("info")))
        backButton.pack(side = tk.TOP,fill = tk.X)
        backSeparator = ttk.Separator(extraWindow,orient = 'horizontal')
        backSeparator.pack(side = tk.TOP,fill = tk.X)
        attributionsWE()
    elif extraType == "attributionButtons":
        headline.config(text = windowExtra_extraType_attributionButtons_headline_text_langtext)
        backButton = ttk.Button(extraWindow,text = windowExtra_extraType_attributionButtons_backbutton_text_langtext,command = lambda: (windowExtra("attributions")))
        backButton.pack(side = tk.TOP,fill = tk.X)
        backSeparator = ttk.Separator(extraWindow,orient = 'horizontal')
        backSeparator.pack(side = tk.TOP,fill = tk.X)
        attributionButtonsWE()
    elif extraType == "Changelog":
        headline.config(text = windowExtra_extraType_Changelog_headline_text_langtext)
        backButton = ttk.Button(extraWindow,text = windowExtra_extraType_Changelog_backButton_text_langtext,command = lambda: (windowExtra("info")))
        backButton.pack(side = tk.TOP,fill = tk.X)
        backSeparator = ttk.Separator(extraWindow,orient = 'horizontal')
        backSeparator.pack(side = tk.TOP,fill = tk.X)
        changelogWE()
    elif extraType == "License":
        headline.config(text = "GNU GENERAL PUBLIC LICENSE Version 2")
        backButton = ttk.Button(extraWindow,text = "Info & help",command = lambda: (windowExtra("info")))
        backButton.pack(side = tk.TOP,fill = tk.X)
        backSeparator = ttk.Separator(extraWindow,orient = 'horizontal')
        backSeparator.pack(side = tk.TOP,fill = tk.X)
        licenseWE()

def closeExtra():
    global extraWindow
    extraWindow.destroy()
    main_window.attributes('-alpha',1)
    main_window.lift()
    checkLogoInverted()
    #hier wird einfach nur restore main_window aufgerufen und oben wird main_window einmal destroyt (sieht so cursed aus mit diesem t xD)

def closeExtraEvent(event):
    closeExtra()

def message(image,title,message,button,time):#image bekommt: 1, 2, 3 (info, warnung, error); button bekommt: nope, ok ,yn;time bekommt: [Zeit] (0 bei einem knopf bedeutet, dass es sich nicht automatisch schließt)
    global info_icon
    global warning_icon
    global error_icon
    global messageWindow
    global messageInfoLog
    global messageWarningLog
    global messageErrorLog

    if image == 1:
        messageInfoLog.append(title)
        messageInfoLog.append(message)
        messageInfoLog.append(button)
        messageInfoLog.append(time)
    elif image == 2:
        messageWarningLog.append(title)
        messageWarningLog.append(message)
        messageWarningLog.append(button)
        messageWarningLog.append(time)
    elif image == 3:
        messageErrorLog.append(title)
        messageErrorLog.append(message)
        messageErrorLog.append(button)
        messageErrorLog.append(time)
    if image == 1:
        icon = info_icon
        messageType = "Info"
    elif image == 2:
        icon = warning_icon
        messageType = "Warning"
    elif image == 3:
        icon = error_icon
        messageType = "Error"
    else:
        print("Yo the programmer made a mistake I'm sorry")
        if platform.system() == "Windows":
            toast.show_toast(title,message,duration = time,icon_path = icon,threaded = True)
        elif platform.system() == "Linux":
            m = notify2.Notification(title,message).show()#funktion hinzufügen, mti der man die anzeige der programmeigenen benachrichtigungen/der betriebssystem benachrichtigungen ausschalten kann. zumindest die ohne buttons
    messageWindow = tk.Toplevel()
    if platform.system() == "Windows":
        messageWindow.iconbitmap(icon)
    elif platform.system() == "Linux":
        messageWindow.iconphoto(False,icon)
    messageWindow.title(messageType + " | " + title)
    messageWindow.resizable(False,False)
    messageWindow.focus()
    messageFrame = ttk.Frame(messageWindow)
    messageFrame.pack(side = tk.TOP)
    if time != 0:
        messageWindow.after(time,messageWindow.destroy)
    if button == "nope":
        if time == 0:
            print("fuck a mistake")
            return
    elif button == "ok":
        buttonFrame = ttk.Frame(messageWindow)
        buttonFrame.pack(side = tk.TOP)
        messageButton = ttk.Button(buttonFrame,text = "OK",command = messageWindow.destroy)
        messageButton.pack()
    elif button == "yn":
        buttonFrame = ttk.Frame(messageWindow)
        buttonFrame.pack(side = tk.TOP)
        yesButton = ttk.Button(buttonFrame,text = "Yes",command = messageWindow.destroy)
        yesButton.pack(side = tk.LEFT)
        noButton = ttk.Button(buttonFrame,text = "No",command = messageWindow.destroy)
        noButton.pack(side = tk.RIGHT)
    elif button[:6] == "custom":
        buttonFrame = ttk.Frame(messageWindow)
        buttonFrame.pack(side = tk.TOP)
        semicolon = button.find(";")
        comma = button.find(",")
        title = button[6:comma]
        wTd = button[comma + 1:semicolon]#what to do
        #print(wTd)#ich kann leider nicht einfach den command einfügen, weil da kein string renkommt.
        if wTd == "nope":
            button1 = ttk.Button(buttonFrame,text = "No",command = messageWindow.destroy)
            button1.pack(side = tk.LEFT)
        elif wTd == "settings":
            button1 = ttk.Button(buttonFrame,text = title,command = lambda: (windowExtra("settings"),messageWindow.destroy()))
            button1.pack(side = tk.LEFT)
        button = button[semicolon + 1:]
        comma = button.find(",")
        title = button[6:comma]
        wTd = button[comma + 1:semicolon]#what to do
        #print(wTd)#ich kann leider nicht einfach den command einfügen, weil da kein string renkommt.
        if wTd == "nope":
            button2 = ttk.Button(buttonFrame,text = "No",command = messageWindow.destroy)
            button2.pack(side = tk.RIGHT)
        elif wTd == "settings":
            button2 = ttk.Button(buttonFrame,text = title,command = lambda: (windowExtra("settings"),messageWindow.destroy()))
            button2.pack(side = tk.RIGHT)
    else:
        print("Yup I made a mistake")
    messageLabel = ttk.Label(messageFrame,text = message)
    messageLabel.pack()

def rcmenuCheck(event):
    selection = tree.selection()
    if selection == ():
        rcmenu1.post(event.x_root,event.y_root)
    else:
        rcmenu2.post(event.x_root,event.y_root)

def progress():
    global progressbar
    try:
        progressWindow.destroy()
    except:
        pass
    progressWindow = tk.Toplevel()
    progressWindow.resizable(False,False)
    progressWindow.title(progress_progressWindow_title_langtext)
    progressbar = ttk.Progressbar(progressWindow,orient = 'horizontal',mode = 'determinate',length = 500)
    progressbar.pack()

def makeProgress():
    global progressPercent
    if progressbar['value'] < 100:
        progressbar['value'] = progressbar['value'] + progressPercent

def loading_Threading():
    print("loading_threading started")
    loading_thread = Thread(target = loading)
    loading_thread.start()

def loading():
    print("now ir should be loading")
    global main_window
    global plW
    global cursor_state
    print(cursor_state)
    while cursor_state == "normal" and exiting != True:
        if platform.system() == "Linux":
            main_window.config(cursor = "watch")
            main_window.update_idletasks()
            plW.config(cursor = "watch")
            print("lets trieeeeee")
            plW.update_idletasks()
            cursor_state = "loading"
        else:
            main_window.config(cursor = "wait")
            main_window.update_idletasks()
            plW.config(cursor = "wait")
            plW.update_idletasks()
            cursor_state = "loading"
    print(cursor_state)
    print("loading start done")

def loading_stop():
    global cursor_state
    print("now it shiuold not be loading")
    print(cursor_state)
    while cursor_state == "loading":
        main_window.config(cursor = "")
        main_window.update_idletasks()
        plW.config(cursor = "")
        plW.update_idletasks()
        cursor_state = "normal"
    print("loading stop done")


#def loadingThreading():
#    loadingThread = Thread(target = loading)
#    loadingThread.start()

def reverseTuple(tuple):
    newTuple = tuple[::-1]
    return newTuple

def refreshRecentFiles():
    global sub_menu1
    global sub_menu21
    global sub_menu22
    global sub_menu3
    global recentFiles
    global recentSongs
    global recentPlaylists
    global playlist
    global pPlaylist
    for filename in  recentFiles:
        sub_menu1.delete(0,tk.END)
    for filename in  recentSongs:
        sub_menu21.delete(0,tk.END)
    for filename in  recentPlaylists:
        sub_menu22.delete(0,tk.END)
    try:
        for filename in  recentFiles:
            sub_menu3.delete(0,tk.END)
    except:
        pass
    count = 0
    print("recent files")
    print(recentFiles)
    for filename in recentFiles:
        sub_menu1.add_command(label=filename[:-1], command=lambda f=filename[:-1]: addToPlaylist(str(f)))#von duckduckgo gpt3.5
        #sub_menu1.add_command(label = filename[:-2],command = lambda:(addToPlaylist(str(filename))))
        #sub_menu1.add_command(label = filename[:-1],command = addToPlaylist(str(filename)))
        print("fuck this")
    for filename in recentSongs:
        sub_menu21.add_command(label = filename[:-1],command = lambda f=filename[:-1]: addToPlaylist(str(f)))
        print("fuckening this")
    for filename in recentPlaylists:
        sub_menu22.add_command(label = filename[:-1],command = lambda f=filename[:-1]: addToPlaylist(str(f)))
        print("fuckeningening this")
    try:
        print("i'm trying now lol")
        for filename in recentFiles:
            sub_menu3.add_command(label = filename[:-1],command = lambda f=filename[:-1]: addToPlaylist(str(f)))
            print("fuckeningeningening this")
    except:
        pass

def buildTwoWindows(ToF):
    message(1,buildTwoWindows_message1_title_langtext,buildTwoWindows_message1_text_langtext,"ok",5000)

def buildVolumeSliderText(ToF):
    global volumeSlider
    global volumeSliderExtra
    global volumeInfo
    global volumeInfoExtra
    global toolbarFrameExtra
    volumeSlider.destroy()
    try:
        volumeSliderExtra.destroy()
    except:
        pass
    try:
        volumeInfo.destroy()
    except:
        pass
    try:
        volumeInfoExtra.destroy()
    except:
        pass
    if ToF == True:
        volumeInfo = ttk.Label(toolbarFrame,text = volumeText)
        volumeInfo.pack(side = tk.TOP)
        try:
            volumeInfoExtra = ttk.Label(toolbarFrameExtra,text = volumeText)
            volumeInfoExtra.pack(side = tk.TOP)
        except:
            pass
    volumeSlider = ttk.Scale(toolbarFrame,variable = volume,from_ = 0,to = 100,orient = 'vertical')
    volumeSlider.bind("<Motion>",changeVolume)
    volumeSlider.bind("<ButtonRelease-1>",volumePressedFalse)
    volumeSlider.bind("<ButtonPress-1>",volumePressedTrue)
    volumeSlider.pack(side = tk.BOTTOM,fill = tk.Y,expand = True,pady = 10)
    try:
        volumeSliderExtra = ttk.Scale(toolbarFrameExtra,variable = volume,from_ = 0,to = 100,orient = 'vertical')
        volumeSliderExtra.bind("<Motion>",changeVolume)
        volumeSliderExtra.bind("<ButtonRelease-1>",volumePressedFalse)
        volumeSliderExtra.bind("<ButtonPress-1>",volumePressedTrue)
        volumeSliderExtra.pack(side = tk.BOTTOM,fill = tk.Y,expand = True,pady = 10)
    except:
        pass

def buildMiniMode_main_window(event):
    global numberforminimode_main_window
    print(numberforminimode_main_window)
    numberforminimode_main_window = numberforminimode_main_window + 1
    if numberforminimode_main_window == 21:
        numberforminimode_main_window = 1
        buildMiniMode()

def buildMiniMode_plW(event):
    global numberforminimode_plW
    print(numberforminimode_plW)
    numberforminimode_plW = numberforminimode_plW + 1
    if numberforminimode_plW == 26:
        numberforminimode_plW = 1
        buildMiniMode()

def buildMiniMode():
    message(1,buildMiniMode_message1_title_langtext,buildMiniMode_message1_text_langtext,"ok",5000)
    return
    global main_window
    global plW
    global main_window_size
    global plW_size
    global exit_button_image
    global rewind_button_image_smol
    global forward_button_image_smol
    global play_image_smol
    global pause_image_smol
    global song_cover_image_smol
    global remainingPlaylistLength
    global songName
    global songArtist
    global songLength
    global songPosition
    global songLengthSeconds
    global plstSelection
    global songCoverMini
    global songLengthTextMini
    global songTitleLabelMini
    global songArtistLabelMini
    global songPositionTextMini
    global musicSliderMini
    global plWminiMode
    global treeMiniMode
    global miniModeActive
    global remainingPlaylistLengthLabelMini
    global playlistSelectionLabelMini
    global togglePlayButtonMini
    global songArtImageSmol
    miniModeActive = True
    main_window_size = main_window.geometry()
    plW_size = plW.geometry()
    print("trying")
    main_window.destroy()
    plW.destroy()
    print("done")
    x_pos = main_window_size.find('x')
    firstplus_pos = main_window_size.find('+')
    secondplus_pos = main_window_size.rfind('+')
    main_window_size_1 = main_window_size[:x_pos + 1]
    main_window_size_2 = main_window_size[firstplus_pos + 1:secondplus_pos]
    miniModeSize = main_window_size_1 + "82+" + main_window_size_2 + "+380"
    print(miniModeSize)
    miniModeWindow = tk.Toplevel()
    miniModeWindow.geometry(miniModeSize)
    miniModeWindow.title(buildMiniMode_miniModeWindow_title_langtext)
    #iconshit
    miniModeWindow.protocol("WM_DELETE_WINDOW",exitProgram)
    #Frames
    musicControlFrameMini = ttk.Frame(miniModeWindow,height = 50)
    musicControlFrameMini.pack(side = tk.BOTTOM,fill = tk.X)
        #musicControlFrame
    musicControlFrameMiniL = ttk.Frame(musicControlFrameMini,width = 50)
    musicControlFrameMiniL.pack(side = tk.LEFT)
    musicControlFrameMiniR = ttk.Frame(musicControlFrameMini,width = 300)
    musicControlFrameMiniR.pack(side = tk.RIGHT)
    musicInfoFrameMini2_1 = ttk.Frame(musicControlFrameMini)
    musicInfoFrameMini2_1.pack(side = tk.TOP,fill = tk.X)
    musicInfoFrameMini2_2 = ttk.Frame(musicControlFrameMini)
    musicInfoFrameMini2_2.pack(side = tk.BOTTOM,fill = tk.X)
    musicInfoFrameMini1 = ttk.Frame(miniModeWindow)
    musicInfoFrameMini1.pack(side = tk.BOTTOM,fill = tk.X)
    #not frames xD
        #musicControlFrameMiniL
    songCoverMini = ttk.Label(musicControlFrameMiniL,image = song_cover_image_smol)
    songCoverMini.pack()
        #musicControlFrameMiniR
    exitButtonMini = ttk.Button(musicControlFrameMiniR,image = exit_button_image,command = restorenormal_mode)
    exitButtonMini.pack(side = tk.RIGHT)
    forwardButtonMini = ttk.Button(musicControlFrameMiniR,image = forward_button_image_smol,command = fastForward)
    forwardButtonMini.pack(side = tk.RIGHT)
    togglePlayButtonMini = ttk.Button(musicControlFrameMiniR,image = play_image_smol,command = togglePlay)
    togglePlayButtonMini.pack(side = tk.RIGHT)
    rewindButtonMini = ttk.Button(musicControlFrameMiniR,image = rewind_button_image_smol,command = rewindSong)
    rewindButtonMini.pack(side = tk.RIGHT)
    checkLogoInverted()
        #musicInfoFrameMini1
    songPositionTextMini = ttk.Label(musicInfoFrameMini1,text = songPosition)
    songPositionTextMini.pack(side = tk.LEFT)
    songLengthTextMini = ttk.Label(musicInfoFrameMini1,text = songLength)
    songLengthTextMini.pack(side = tk.RIGHT)
    musicSliderMini = ttk.Scale(musicInfoFrameMini1,variable = sliderVarMini,from_ = 0,to = songLengthSeconds,orient = 'horizontal')
    musicSliderMini.bind("<Motion>",sliderChangePos)
    musicSliderMini.bind("<ButtonRelease-1>",sliderChange)
    musicSliderMini.bind("<ButtonPress-1>",sliderPressedTrue)
    musicSliderMini.pack(side = tk.BOTTOM,fill = tk.X,expand = True)
        #musicInfoFrameMini2_1
    songTitleLabelMini = ttk.Label(musicInfoFrameMini2_1,text = songName)
    songTitleLabelMini.pack(side = tk.LEFT)
    songArtistLabelMini = ttk.Label(musicInfoFrameMini2_1,text = songArtist)
    songArtistLabelMini.pack(sid = tk.RIGHT)
        #musicInfoFrameMini2-2
    playlistSelectionLabelMini = ttk.Label(musicInfoFrameMini2_2,text = plstSelection)
    playlistSelectionLabelMini.pack(side = tk.LEFT)
    remainingPlaylistLengthLabelMini = ttk.Label(musicInfoFrameMini2_2,text = remainingPlaylistLength)
    remainingPlaylistLengthLabelMini.pack(side = tk.RIGHT)
    try:
        songLength,songLengthSec = getSongLength(song)
        songArtist = getSongArtist(song)
        songName = getSongName(song)
        songArt = getSongArt(song)
        musicSliderExtra.config(to = songLengthSec)
        songLengthTextSmol.config(text = songLength)
        songLS = song.rfind("/")#song last slash
        songFilename = song[songLS + 1:]
        songArtistTextSmol.config(text = songArtist)
        songNameTextSmol.config(text = songName)
        if songArt != "nothing":
            songArtImage = tk.PhotoImage(file = 'song_cover_smol.png')#warum klappt das hier nicht!?!?!
            songCoverMini.config(image = songArtImageSmol)
            songCoverMini.image = songArtImageSmol
        if songArtist == 'unknown':
            songArtistLabelMini.config(text = songFilename)
            if songName == 'unknown':
                songTitleLabelMini.config(text = '')
            else:
                songTitleLabelMini.config(text = songName)
        elif songName == 'unknown':
            songNameTitleLabelMini.config(text = songFilename)
    except:
        pass
    plWminiMode = tk.Toplevel()
    main_window_size_2_int = int(main_window_size_2)
    main_window_size_2_int = main_window_size_2_int + 500
    main_window_size_2_str = str(main_window_size_2_int)
    plWminiMode.geometry(main_window_size_1 + "82+" + main_window_size_2_str + "+380")
    plWminiMode.title(buildMiniMode_plWminiMode_title_langtext)
    #iconshit
    plWminiMode.protocol("WM_DELETE_WINDOW",exitProgram)
    plWminiMode.bind("<Delete>",delFrompllstKey)
    plWminiMode.bind("<Up>",upInPlaylistKey)
    plWminiMode.bind("<Down>",downInPlaylistKey)
    plWminiMode.bind("<Left>",topInPlaylistKey)
    plWminiMode.bind("<Right>",bottomInPlaylistKey)
    #playlist
    columns = ('Title','Artist','length','count')
    treeMiniMode = ttk.Treeview(plWminiMode,columns = columns,show = 'headings')
    treeMiniMode.heading('Title',text = buildMiniMode_treeMiniMode_heading1_text_langtext)
    treeMiniMode.heading('Artist',text = buildMiniMode_treeMiniMode_heading2_text_langtext)
    treeMiniMode.heading('length',text = buildMiniMode_treeMiniMode_heading3_text_langtext)
    treeMiniMode.column('Title',width = 217)
    treeMiniMode.column('Artist',width = 217)
    treeMiniMode.column('length',width = 50)
    treeMiniMode.column('count',width = 0,stretch = False)
    treeMiniMode.tag_configure("playing", foreground="green")
    treeMiniMode.tag_configure("not_playing",foreground = "black")
    treeMiniMode.pack(side = tk.LEFT,fill = tk.Y)
    treeMiniMode.bind('<Motion>','break')
    treeMiniMode.bind('<Double-1>',playFromPlaylistEvent)
    scrollbarMiniMode = ttk.Scrollbar(plWminiMode,orient = tk.VERTICAL,command = treeMiniMode.yview)
    treeMiniMode.configure(yscroll = scrollbarMiniMode.set)
    scrollbarMiniMode.pack(side = tk.RIGHT,fill = tk.Y)
    updatePlaylist(0,0)

def restorenormal_mode():
    pass

def restoremain_window():
    pass

def restorePlW():
    pass

def messageLogClicked(event):
    global tree1
    global tree2
    global tree3
    global selectedLog
    global message_icon
    global info_icon
    global warning_icon
    global error_icon
    if selectedLog == "0":
        selection = tree1.selection()
    elif selectedLog == "1":
        selection = tree2.selection()
    elif selectedLog == "2":
        selection = tree3.selection()
    for item in selection:
        if selectedLog == "0":
            selectedRow = tree1.item(item)
            messageType = "Info"
            icon = "Info icon"
            iconNR = 1
        if selectedLog == "1":
            selectedRow = tree2.item(item)
            messageType = "Warning"
            icon = "Warning icon"
            iconNR = 2
        if selectedLog == "2":
            selectedRow = tree3.item(item)
            messageType = "Error"
            icon = "Error icon"
            iconNR = 3
        values = selectedRow['values']
        title = values[0]
        messageText = values[1]#kann nicht nur message sein, weil sonst beim rufen der message funktion der den fehler gibt, dass er kein string objekt rufen kann
        buttons = values[2]
        time = values[3]
        count = values[4]
        if time == "0ms":
            timeText = messageLogClicked_time0_timeText_langtext
        else:
            timeText = time
        time = int(time[:-2])
        messageInfo = tk.Toplevel()
        messageInfo.title(messageLogClicked_messageInfo_title_langtext + messageType + " " + str(count))
        messageInfo.resizable(False,False)#message_icon
        if platform.system() == "Windows":
            messageInfo.iconbitmap(message_icon)
        elif platform.system() == "Linux":
            messageInfo.iconphoto(False,message_icon)
        messageInfo.focus()
        buttonFrame = ttk.Frame(messageInfo)
        buttonFrame.pack(side = tk.BOTTOM,fill = tk.X)
        messageDetails = ttk.Label(messageInfo,text = messageLogClicked_messageDetails_text_langtext)
        messageDetails.pack(side = tk.TOP,anchor = tk.NW)
        separator1 = ttk.Separator(messageInfo,orient = 'horizontal')
        separator1.pack(side = tk.TOP,fill = tk.X)
        messageImageText = ttk.Label(messageInfo,text = messageLogClicked_messageImageText_text_langtext + icon)
        messageImageText.pack(side = tk.TOP,anchor = tk.NW)#maybe das wieder messageimage nennen, wenn du dich entscheiden hast, kein bild anzuezeigen
        #messageImage = ttk.Label(messageInfo,image = icon)
        #messageImage.pack(side = tk.TOP,anchor = tk.NW)
        messageTitle = ttk.Label(messageInfo,text = messageLogClicked_messageTitle_text_langtext + title)
        messageTitle.pack(side = tk.TOP,anchor = tk.NW)
        messageMessage = ttk.Label(messageInfo,text = messageLogClicked_messageMessage_text_langtext + messageText)
        messageMessage.pack(side = tk.TOP,anchor = tk.NW)
        messageButtons = ttk.Label(messageInfo,text = messageLogClicked_messageButtons_text_langtext + buttons)
        messageButtons.pack(side = tk.TOP,anchor = tk.NW)
        messageTime = ttk.Label(messageInfo,text = messageLogClicked_messageTime_text_langtext + timeText)
        messageTime.pack(side = tk.TOP,anchor = tk.NW)
        separator2 = ttk.Separator(messageInfo,orient = 'horizontal')
        separator2.pack(side = tk.TOP,fill = tk.X)
        previewButton = ttk.Button(buttonFrame,text = messageLogClicked_previewButton_text_langtext,command = lambda: (message(iconNR,title,messageText,buttons,time)))
        previewButton.pack(side = tk.RIGHT,anchor = tk.NW)#vielleicht als text nur Preview und nd preview message
        closeButton = ttk.Button(buttonFrame,text = messageLogClicked_closeButton_text_langtext,command = messageInfo.destroy)
        closeButton.pack(side = tk.LEFT,anchor = tk.NW)

def notebookTabChange(event):
    global logs
    global selectedLog
    selectedLog = str(logs.index("current"))

def filesToKeepChanged():
    global filesToKeep
    global recentFiles
    global recentSongs
    global recentPlaylists
    howmany = filesToKeep.get()
    filepath = os.path.join(dirname,"texts/settings.txt")
    with open(filepath,'r') as file:
        lines = file.readlines()
    lines[5] = str(howmany) + '\n'
    with open(filepath,'w') as file:
        file.writelines(lines)
    temp_list = []
    count = howmany
    while count > 0:
        try:
            temp_list.insert(0,recentFiles[count - 1])
        except:
            temp_list.insert(0,empty_file_text_list)
        count = count - 1
    recentFiles = []
    recentFiles = temp_list
    temp_list = []
    count = howmany
    while count > 0:
        try:
            temp_list.insert(0,recentSongs[count - 1])
        except:
            temp_list.insert(0,empty_file_text_list)
        count = count - 1
    recentSongs = []
    recentSongs = temp_list
    temp_list = []
    count = howmany
    while count > 0:
        try:
            temp_list.insert(0,recentPlaylists[count - 1])
        except:
            temp_list.insert(0,empty_file_text_list)
        count = count - 1
    recentPlaylists = []
    recentPlaylists = temp_list
    filepath = os.path.join(dirname,"texts/recent_files.txt")
    with open(filepath,'r') as file:
        lines = file.readlines()
    del lines
    lines = recentFiles
    with open(filepath,'w') as file:
        file.writelines(lines)
    filepath = os.path.join(dirname,"texts/recent_songs.txt")
    with open(filepath,'r') as file:
        lines = file.readlines()
    del lines
    lines = recentSongs
    with open(filepath,'w') as file:
        file.writelines(lines)
    filepath = os.path.join(dirname,"texts/recent_playlists.txt")
    with open(filepath,'r') as file:
        lines = file.readlines()
    del lines
    lines = recentPlaylists
    with open(filepath,'w') as file:
        file.writelines(lines)
    refreshRecentFiles()

def settingsFmenu(setting):
    if setting == "volumeSliderText":
        volumeSliderText = volumeSliderTextOnOff.get()
        if volumeSliderText == False:
            volumeSliderTextOnOff.set("True")
        else:
            volumeSliderTextOnOff.set("False")
    elif setting == "twoWindows":
        twoWindowsText = twoWindows.get()
        if twoWindowsText == False:
            twoWindows.set("True")
        else:
            twoWindows.set("False")
    elif setting == "miniMode":
        miniModeActiveText = miniModeActive.get()
        if miniModeActiveText == False:
            miniModeActive.set("True")
        else:
            miniModeActive.set("False")
    settings(setting)

def settings(setting):
    global loopPlaylist
    global loopMove
    filepath = os.path.join(dirname,"texts/settings.txt")
    with open(filepath,'r') as file:
        lines = file.readlines()
    if setting == "volumeSliderText":
        volumeSliderText = volumeSliderTextOnOff.get()
        if volumeSliderText == False:
            volumeSliderText = ""
            buildVolumeSliderText(False)
        else:
            volumeSliderText = "True"
            buildVolumeSliderText(True)
        lines[1] = ""
        lines[1] = volumeSliderText + '\n'
    elif setting == "loopPlaylist":
        loopPlaylistText = loopPlaylist.get()
        if loopPlaylistText == False:
            loopPlaylistText = ""
        else:
            loopPlaylistText = "True"
        lines[2] = ""
        lines[2] = loopPlaylistText + '\n'
    elif setting == "loopMove":
        loopMoveText = loopMove.get()
        if loopMoveText == False:
            loopMoveText = ""
        else:
            loopMoveText = "True"
        lines[3] = ""
        lines[3] = loopMoveText + '\n'#mb kannst du hier das "" davor wegmachen, genauso auch bei move playlist
    elif setting == "twoWindows":
        twoWindowsText = twoWindows.get()
        if twoWindowsText == False:
            twoWindowsText = ""
            buildTwoWindows(False)
        else:
            twoWindowsText = "True"
            buildTwoWindows(True)
        lines[4] = ""
        lines[4] = twoWindowsText + '\n'
    elif setting == "miniMode":
        miniModeActiveText = miniModeActive.get()
        if miniModeActiveText == False:
            miniModeActiveText = ""
            buildMiniMode(False)
        else:
            miniModeActiveText = "True"
            buildMiniMode(True)
        lines[6] = ""
        lines[6] = miniModeActiveText + '\n'
    elif setting == "shuffleReset":
        shuffleResetText = shuffleReset.get()
        if shuffleResetText == False:
            shuffleResetText = ""
        else:
            shuffleResetText = "True"
        lines[7] = ""
        lines[7] = shuffleResetText + '\n'
    with open(filepath,'w') as file:
        file.writelines(lines)


def openFilesDialog():
    app = QApplication(sys.argv)
    options = QFileDialog.Options()
    options |= QFileDialog.ReadOnly
    files, _ = QFileDialog.getOpenFileNames(None, "Open Songs or Playlists", "", "All Files (*)",options = options)
    return files

def saveFileDialog():
    app = QApplication(sys.argv)
    options = QFileDialog.Options()
    fileName,selectedFilter = QFileDialog.getSaveFileName(None,saveFileDialog_QFileDialog_SaveFilterName1_langtext,"",saveFileDialog_QFileDialog_SaveFilterName2_langtext,options = options)
    return fileName,selectedFilter

def loadLanguages():
    languageList = []
    languageListOptionMenu = []
    for filename in os.listdir(os.path.join(dirname,'texts/language')):
        if filename.startswith("language_"):
            filepath = os.path.join(os.path.join(dirname,'texts/language'),filename)
            underscore = filename.find("_")
            languageList.append([filename[underscore + 1:-4],filepath])
            languageListOptionMenu.append(filename[underscore + 1:-4])
    print(languageList)
    return languageList,languageListOptionMenu

def languageChange(event):
    language = languageStringVar.get()
    loadLanguage(language,languageList)
    with open(os.path.join(dirname,'texts/language/selection.txt'),'w') as languageFile:
        languageFile.writelines([language])
    message(1,languageChange_message1_title_langtext,languageChange_message1_text_langtext,"ok",0)

def loadLanguage(language,languageList):
    global main_window_title_langtext, file_menu1_command1_label_langtext, file_menu1_cascade1_label_langtext, file_menu1_command2_label_langtext, file_menu1_command3_label_langtext, file_menu1_command4_label_langtext, file_menu1_command5_label_langtext, menubar1_cascade1_label_langtext, view_menu1_command1_label_langtext, view_menu1_command2_label_langtext, view_menu1_command3_label_langtext, menubar1_cascade2_label_langtext, help_menu1_command1_label_langtext, help_menu1_command2_label_langtext, help_menu1_command3_label_langtext, help_menu1_command4_label_langtext, help_menu1_command5_label_langtext, menubar1_cascade3_label_langtext, plW_title_langtext, file_menu2_command1_label_langtext, file_menu2_cascade1_label_langtext, file_menu2_cascade2_label_langtext, file_menu2_command2_label_langtext, file_menu2_command3_label_langtext, file_menu2_command4_label_langtext, file_menu2_command5_label_langtext, file_menu2_cascade3_label_langtext, edit_menu2_command1_label_langtext, edit_menu2_command2_label_langtext, edit_menu2_command3_label_langtext, edit_menu2_command4_label_langtext, edit_menu2_command5_label_langtext, edit_menu2_command6_label_langtext, edit_menu2_command7_label_langtext, menubar2_cascade1_label_langtext, songName_variable_langtext, songArtist_variable_langtext, songFilename_variable_langtext, tree_heading1_text_langtext, tree_heading2_text_langtext, tree_heading3_text_langtext, rcmenu1_command1_label_langtext, rcmenu1_command2_label_langtext, rcmenu2_command1_label_langtext, rcmenu2_command2_label_langtext, rcmenu2_command3_label_langtext, rcmenu2_command4_label_langtext, rcmenu2_command5_label_langtext, playlistSelectedLabel_text_langtext, playlistDurationLabel_text_langtext, remainingPlaylistDurationLabel_text_langtext, fastForward_message1_title_langtext, fastForward_message1_text_langtext, fastForward_message2_title_langtext, fastForward_message2_text_langtext, rewindSong_message1_title_langtext, rewindSong_message1_text_langtext, rewindSong_message2_title_langtext, rewindSong_message2_text_langtext, addToPlaylist_message1_title_langtext, addToPlaylist_message1_text_langtext, updatePlaylist_plW_title_langtext, updatePlaylist_plWminiMode_title_langtext, updatePlaylist_playlistLengthLabel_text_langtext, updatePlaylist_remainingPlaylistLengthLabel_text_langtext, tree_loading_text_langtext, updatePlaylist_remainingPlaylistLengthLabelMini_text_langtext, treeMiniMode_loading_text_langtext, length_for_playlist_plW_title_langtext, length_for_playlist_plWminiMode_title_langtext, length_for_playlist_message1_title_langtext, length_for_playlist_message1_text_langtext, length_for_playlist_message2_title_langtext, length_for_playlist_message2_text_langtext, savePlaylist_message1_title_langtext, savePlaylist_message1_text1_langtext, savePlaylist_message1_text2_langtext, upInPlaylist_message1_title_langtext, upInPlaylist_message1_text_langtext, downInPlaylist_message1_title_langtext, downInPlaylist_message1_text_langtext, infoWE_extraWindow_title_langtext, infoWE_changelogButton_text_langtext, infoWE_attributions_text_langtext, infoWE_licenseButton_text_langtext, settingsWE_extraWindow_title_langtext, settingsWE_twoWindowsCheckbutton_text_langtext, settingsWE_showVolumeInfoCheckbutton_text_langtext, settingsWE_loopPlaylistCheckbutton_text_langtext, settingsWE_loopMoveCheckbutton_text_langtext, settingsWE_shufflePositionResetCheckbutton_text_langtext, settingsWE_messageLogsButton_text_langtext, messageLogsWE_extraWindow_title_langtext, messageLogsWE_logs_add1_text_langtext, messageLogsWE_logs_add2_text_langtext, messageLogsWE_logs_add3_text_langtext, messageLogsWE_tree1_2_3_heading1_text_langtext, messageLogsWE_tree1_2_3_heading2_text_langtext, messageLogsWE_tree1_2_3_heading3_text_langtext, messageLogsWE_tree1_2_3_heading4_text_langtext, messageLogsWE_tree1_2_3_heading5_text_langtext, attributionsWE_extraWindow_title_langtext, attributionsWE_attributionLinksButton_text_langtext, attributionButtonsWE_extraWindow_title_langtext, changelogWE_extraWindow_title_langtext, licenseWE_extraWindow_title_langtext, windowExtra_file_menu3_command1_label_langtext, windowExtra_file_menu3_cascade1_label_langtext, windowExtra_file_menu3_command2_label_langtext, windowExtra_file_menu3_command3_label_langtext, windowExtra_file_menu3_command4_label_langtext, windowExtra_file_menu3_command5_label_langtext, windowExtra_menubar3_cascade1_label_langtext, windowExtra_view_menu3_command1_label_langtext, windowExtra_view_menu3_command2_label_langtext, windowExtra_view_menu3_command3_label_langtext, windowExtra_menubar3_cascade2_label_langtext, windowExtra_help_menu3_command1_label_langtext, windowExtra_help_menu3_command2_label_langtext, windowExtra_help_menu3_command3_label_langtext, windowExtra_help_menu3_command4_label_langtext, windowExtra_help_menu3_command5_label_langtext, windowExtra_menubar3_cascade3_label_langtext, windowExtra_extraType_info_headline_text_langtext, windowExtra_extraType_settings_headline_text_langtext, windowExtra_extraType_messageLogs_headline_text_langtext, windowExtra_extraType_messageLogs_backButton_text_langtext, windowExtra_extraType_attributions_headline_text_langtext, windowExtra_extraType_attributions_backButton_text_langtext, windowExtra_extraType_attributionButtons_headline_text_langtext, windowExtra_extraType_attributionButtons_backbutton_text_langtext, windowExtra_extraType_Changelog_headline_text_langtext, windowExtra_extraType_Changelog_backButton_text_langtext, progress_progressWindow_title_langtext, buildTwoWindows_message1_title_langtext, buildTwoWindows_message1_text_langtext, buildMiniMode_message1_title_langtext, buildMiniMode_message1_text_langtext, buildMiniMode_miniModeWindow_title_langtext, buildMiniMode_plWminiMode_title_langtext, buildMiniMode_treeMiniMode_heading1_text_langtext, buildMiniMode_treeMiniMode_heading2_text_langtext, buildMiniMode_treeMiniMode_heading3_text_langtext, messageLogClicked_time0_timeText_langtext, messageLogClicked_messageInfo_title_langtext, messageLogClicked_messageDetails_text_langtext, messageLogClicked_messageImageText_text_langtext, messageLogClicked_messageTitle_text_langtext, messageLogClicked_messageMessage_text_langtext, messageLogClicked_messageButtons_text_langtext, messageLogClicked_messageTime_text_langtext, messageLogClicked_previewButton_text_langtext, messageLogClicked_closeButton_text_langtext, empty_file_text_list, saveFileDialog_QFileDialog_SaveFilterName1_langtext, saveFileDialog_QFileDialog_SaveFilterName2_langtext, exitProgram_message1_title_langtext, exitProgram_message1_text_langtext, exitProgram_main_window_title_langtext, exitProgram_plW_title_langtext, languageChange_message1_title_langtext, languageChange_message1_text_langtext
    #ohjemine
    print(languageList)
    print(language)
    for languageListList in languageList:
        if languageListList[0] == language:
            languagePath = languageListList[1]
            break
    with open(languagePath,'r') as languageFile:
        oldLines = languageFile.readlines()
    lines = []
    for line in oldLines:
        line = line[:-1]
        lines.append(line)
    main_window_title_langtext = lines[0]
    file_menu1_command1_label_langtext = lines[1]
    file_menu1_cascade1_label_langtext = lines[2]
    file_menu1_command2_label_langtext = lines[3]
    file_menu1_command3_label_langtext = lines[4]
    file_menu1_command4_label_langtext = lines[5]
    file_menu1_command5_label_langtext = lines[6]
    menubar1_cascade1_label_langtext = lines[7]
    view_menu1_command1_label_langtext = lines[8]
    view_menu1_command2_label_langtext = lines[9]
    view_menu1_command3_label_langtext = lines[10]
    menubar1_cascade2_label_langtext = lines[11]
    help_menu1_command1_label_langtext = lines[12]
    help_menu1_command2_label_langtext = lines[13]
    help_menu1_command3_label_langtext = lines[14]
    help_menu1_command4_label_langtext = lines[15]
    help_menu1_command5_label_langtext = lines[16]
    menubar1_cascade3_label_langtext = lines[17]
    plW_title_langtext = lines[18]
    file_menu2_command1_label_langtext = lines[19]
    file_menu2_cascade1_label_langtext = lines[20]
    file_menu2_cascade2_label_langtext = lines[21]
    file_menu2_command2_label_langtext = lines[22]
    file_menu2_command3_label_langtext = lines[23]
    file_menu2_command4_label_langtext = lines[24]
    file_menu2_command5_label_langtext = lines[25]
    file_menu2_cascade3_label_langtext = lines[26]
    edit_menu2_command1_label_langtext = lines[27]
    edit_menu2_command2_label_langtext = lines[28]
    edit_menu2_command3_label_langtext = lines[29]
    edit_menu2_command4_label_langtext = lines[30]
    edit_menu2_command5_label_langtext = lines[31]
    edit_menu2_command6_label_langtext = lines[32]
    edit_menu2_command7_label_langtext = lines[33]
    menubar2_cascade1_label_langtext = lines[34]
    songName_variable_langtext = lines[35]
    songArtist_variable_langtext = lines[36]
    songFilename_variable_langtext = lines[37]
    tree_heading1_text_langtext = lines[38]
    tree_heading2_text_langtext = lines[39]
    tree_heading3_text_langtext = lines[40]
    rcmenu1_command1_label_langtext = lines[41]
    rcmenu1_command2_label_langtext = lines[42]
    rcmenu2_command1_label_langtext = lines[43]
    rcmenu2_command2_label_langtext = lines[44]
    rcmenu2_command3_label_langtext = lines[45]
    rcmenu2_command4_label_langtext = lines[46]
    rcmenu2_command5_label_langtext = lines[47]
    playlistSelectedLabel_text_langtext = lines[48]
    playlistDurationLabel_text_langtext = lines[49]
    remainingPlaylistDurationLabel_text_langtext = lines[50]
    fastForward_message1_title_langtext = lines[51]
    fastForward_message1_text_langtext = lines[52]
    fastForward_message2_title_langtext = lines[53]
    fastForward_message2_text_langtext = lines[54]
    rewindSong_message1_title_langtext = lines[55]
    rewindSong_message1_text_langtext = lines[56]
    rewindSong_message2_title_langtext = lines[57]
    rewindSong_message2_text_langtext = lines[58]
    addToPlaylist_message1_title_langtext = lines[59]
    addToPlaylist_message1_text_langtext = lines[60]
    updatePlaylist_plW_title_langtext = lines[61]
    updatePlaylist_plWminiMode_title_langtext = lines[62]
    updatePlaylist_playlistLengthLabel_text_langtext = lines[63]
    updatePlaylist_remainingPlaylistLengthLabel_text_langtext = lines[64]
    tree_loading_text_langtext = lines[65]
    updatePlaylist_remainingPlaylistLengthLabelMini_text_langtext = lines[66]
    treeMiniMode_loading_text_langtext = lines[67]
    length_for_playlist_plW_title_langtext = lines[68]
    length_for_playlist_plWminiMode_title_langtext = lines[69]
    length_for_playlist_message1_title_langtext = lines[70]
    length_for_playlist_message1_text_langtext = lines[71]
    length_for_playlist_message2_title_langtext = lines[72]
    length_for_playlist_message2_text_langtext = lines[73]
    savePlaylist_message1_title_langtext = lines[74]
    savePlaylist_message1_text1_langtext = lines[75]
    savePlaylist_message1_text2_langtext = lines[76]
    upInPlaylist_message1_title_langtext = lines[77]
    upInPlaylist_message1_text_langtext = lines[78]
    downInPlaylist_message1_title_langtext = lines[79]
    downInPlaylist_message1_text_langtext = lines[80]
    infoWE_extraWindow_title_langtext = lines[81]
    infoWE_changelogButton_text_langtext = lines[82]
    infoWE_attributions_text_langtext = lines[83]
    infoWE_licenseButton_text_langtext = lines[84]
    settingsWE_extraWindow_title_langtext = lines[85]
    settingsWE_twoWindowsCheckbutton_text_langtext = lines[86]
    settingsWE_showVolumeInfoCheckbutton_text_langtext = lines[87]
    settingsWE_loopPlaylistCheckbutton_text_langtext = lines[88]
    settingsWE_loopMoveCheckbutton_text_langtext = lines[89]
    settingsWE_shufflePositionResetCheckbutton_text_langtext = lines[90]
    settingsWE_messageLogsButton_text_langtext = lines[91]
    messageLogsWE_extraWindow_title_langtext = lines[92]
    messageLogsWE_logs_add1_text_langtext = lines[93]
    messageLogsWE_logs_add2_text_langtext = lines[94]
    messageLogsWE_logs_add3_text_langtext = lines[95]
    messageLogsWE_tree1_2_3_heading1_text_langtext = lines[96]
    messageLogsWE_tree1_2_3_heading2_text_langtext = lines[97]
    messageLogsWE_tree1_2_3_heading3_text_langtext = lines[98]
    messageLogsWE_tree1_2_3_heading4_text_langtext = lines[99]
    messageLogsWE_tree1_2_3_heading5_text_langtext = lines[100]
    attributionsWE_extraWindow_title_langtext = lines[101]
    attributionsWE_attributionLinksButton_text_langtext = lines[102]
    attributionButtonsWE_extraWindow_title_langtext = lines[103]
    changelogWE_extraWindow_title_langtext = lines[104]
    licenseWE_extraWindow_title_langtext = lines[105]
    windowExtra_file_menu3_command1_label_langtext = lines[106]
    windowExtra_file_menu3_cascade1_label_langtext = lines[107]
    windowExtra_file_menu3_command2_label_langtext = lines[108]
    windowExtra_file_menu3_command3_label_langtext = lines[109]
    windowExtra_file_menu3_command4_label_langtext = lines[110]
    windowExtra_file_menu3_command5_label_langtext = lines[111]
    windowExtra_menubar3_cascade1_label_langtext = lines[112]
    windowExtra_view_menu3_command1_label_langtext = lines[113]
    windowExtra_view_menu3_command2_label_langtext = lines[114]
    windowExtra_view_menu3_command3_label_langtext = lines[115]
    windowExtra_menubar3_cascade2_label_langtext = lines[116]
    windowExtra_help_menu3_command1_label_langtext = lines[117]
    windowExtra_help_menu3_command2_label_langtext = lines[118]
    windowExtra_help_menu3_command3_label_langtext = lines[119]
    windowExtra_help_menu3_command4_label_langtext = lines[120]
    windowExtra_help_menu3_command5_label_langtext = lines[121]
    windowExtra_menubar3_cascade3_label_langtext = lines[122]
    windowExtra_extraType_info_headline_text_langtext = lines[123]
    windowExtra_extraType_settings_headline_text_langtext = lines[124]
    windowExtra_extraType_messageLogs_headline_text_langtext = lines[125]
    windowExtra_extraType_messageLogs_backButton_text_langtext = lines[126]
    windowExtra_extraType_attributions_headline_text_langtext = lines[127]
    windowExtra_extraType_attributions_backButton_text_langtext = lines[128]
    windowExtra_extraType_attributionButtons_headline_text_langtext = lines[129]
    windowExtra_extraType_attributionButtons_backbutton_text_langtext = lines[130]
    windowExtra_extraType_Changelog_headline_text_langtext = lines[131]
    windowExtra_extraType_Changelog_backButton_text_langtext = lines[132]
    progress_progressWindow_title_langtext = lines[133]
    buildTwoWindows_message1_title_langtext = lines[134]
    buildTwoWindows_message1_text_langtext = lines[135]
    buildMiniMode_message1_title_langtext = lines[136]
    buildMiniMode_message1_text_langtext = lines[137]
    buildMiniMode_miniModeWindow_title_langtext = lines[138]
    buildMiniMode_plWminiMode_title_langtext = lines[139]
    buildMiniMode_treeMiniMode_heading1_text_langtext = lines[140]
    buildMiniMode_treeMiniMode_heading2_text_langtext = lines[141]
    buildMiniMode_treeMiniMode_heading3_text_langtext = lines[142]
    messageLogClicked_time0_timeText_langtext = lines[143]
    messageLogClicked_messageInfo_title_langtext = lines[144]
    messageLogClicked_messageDetails_text_langtext = lines[145]
    messageLogClicked_messageImageText_text_langtext = lines[146]
    messageLogClicked_messageTitle_text_langtext = lines[147]
    messageLogClicked_messageMessage_text_langtext = lines[148]
    messageLogClicked_messageButtons_text_langtext = lines[149]
    messageLogClicked_messageTime_text_langtext = lines[150]
    messageLogClicked_previewButton_text_langtext = lines[151]
    messageLogClicked_closeButton_text_langtext = lines[152]
    empty_file_text_list = lines[153]
    saveFileDialog_QFileDialog_SaveFilterName1_langtext = lines[154]
    saveFileDialog_QFileDialog_SaveFilterName2_langtext = lines[155]
    exitProgram_message1_title_langtext = lines[156]
    exitProgram_message1_text_langtext = lines[157]
    exitProgram_main_window_title_langtext = lines[158]
    exitProgram_plW_title_langtext = lines[159]
    languageChange_message1_title_langtext = lines[160]
    languageChange_message1_text_langtext = lines[161]
    return

def exitProgram():
    global exiting
    global ThreadStopped
    global plW
    global main_window
    loading_stop()
    message(1,exitProgram_message1_title_langtext,exitProgram_message1_text_langtext,"ok",0)
    main_window.title(exitProgram_main_window_title_langtext)
    plW.title(exitProgram_plW_title_langtext)
    exiting = True
    #time.sleep(2)
    sys.exit()

#gui
#bindings
def hideInBackground(event):#auch playlistWindow in hintergrund bringen
    pass

with open(os.path.join(dirname,'texts/language/selection.txt'),'r') as languageFile:
    language = languageFile.readlines()[0]
languageList,languageListOptionMenu = loadLanguages()
loadLanguage(language,languageList)

#root_window
root = tk.Tk()
root.withdraw()

#main window
global main_window
global main_windowWidth
main_windowWidth = 500
main_windowWidthStr = str(main_windowWidth)
main_window = tk.Toplevel()
main_window.title(main_window_title_langtext)
main_window.geometry(main_windowWidthStr + 'x360+100+100')
main_window.bind('<Escape>',hideInBackground)
    #menus
menubar1 = tk.Menu(main_window)
main_window.config(menu = menubar1)
        #file_menu
file_menu1 = tk.Menu(menubar1,tearoff = False)
file_menu1.add_command(label = file_menu1_command1_label_langtext,command = lambda: (addToPlaylist("no")))
sub_menu1 = tk.Menu(file_menu1,tearoff = False)
file_menu1.add_cascade(label = file_menu1_cascade1_label_langtext,menu = sub_menu1)
file_menu1.add_command(label = file_menu1_command2_label_langtext,command = savePlaylist)
file_menu1.add_command(label = file_menu1_command3_label_langtext,command = deleteAllSongs)
file_menu1.add_separator()
file_menu1.add_command(label = file_menu1_command4_label_langtext,command = lambda: (windowExtra("settings")))
file_menu1.add_separator()
file_menu1.add_command(label=file_menu1_command5_label_langtext,command=exitProgram)
menubar1.add_cascade(label=menubar1_cascade1_label_langtext,menu=file_menu1,underline=0)
        #view_menu
view_menu1 = tk.Menu(menubar1,tearoff = False)
view_menu1.add_command(label = view_menu1_command1_label_langtext,command = lambda: (settingsFmenu("volumeSliderText")))
view_menu1.add_command(label = view_menu1_command2_label_langtext,command = lambda: (settingsFmenu("twoWindows")))
view_menu1.add_command(label = view_menu1_command3_label_langtext,command = lambda: (settingsFmenu("miniMode")))
menubar1.add_cascade(label = menubar1_cascade2_label_langtext,menu = view_menu1,underline = 0)
        #help_menu
#keyboard shortcuts
#license
#changelog
#halt alle sachen die im help menu standardmäßig sind und/oder die im info window sind
help_menu1 = tk.Menu(menubar1,tearoff = False)
help_menu1.add_command(label = help_menu1_command1_label_langtext,command = lambda:(windowExtra("info")))
help_menu1.add_command(label = help_menu1_command2_label_langtext,command = lambda:(windowExtra("Changelog")))
help_menu1.add_command(label = help_menu1_command3_label_langtext,command = lambda:(windowExtra("License")))
help_menu1.add_separator()
help_menu1.add_command(label = help_menu1_command4_label_langtext,command = lambda:(windowExtra("settings")))
help_menu1.add_command(label = help_menu1_command5_label_langtext,command = lambda:(windowExtra("messageLogs")))
menubar1.add_cascade(label = "Help",menu = help_menu1,underline = 0)

#playlist window
global plW #playlistWindow
global playlistWidth
playlistWidth = 430
playlistWidthStr = str(playlistWidth)
plW = tk.Toplevel()
plW.title("Playlist")
plW.geometry(playlistWidthStr + 'x360+600+100')
plW.resizable(False,False)
    #menus
menubar2 = tk.Menu(plW)
plW.config(menu = menubar2)
        #file_menu
file_menu2 = tk.Menu(menubar2,tearoff = False)
file_menu2.add_command(label = file_menu2_command1_label_langtext,command = lambda: (addToPlaylist("no")))
sub_menu21 = tk.Menu(file_menu2,tearoff = False)
file_menu2.add_cascade(label = file_menu2_cascade1_label_langtext,menu = sub_menu21)
sub_menu22 = tk.Menu(file_menu2,tearoff = False)
# sub_menu3.add_command(label = 'Recent playlist 1')
file_menu2.add_cascade(label = file_menu2_cascade2_label_langtext,menu = sub_menu22)
file_menu2.add_command(label = file_menu2_command2_label_langtext,command = savePlaylist)
file_menu2.add_command(label = file_menu2_command3_label_langtext,command = deleteAllSongs)
file_menu2.add_separator()
file_menu2.add_command(label = file_menu2_command4_label_langtext,command = lambda: (windowExtra("settings")))
file_menu2.add_separator()
file_menu2.add_command(label=file_menu2_command5_label_langtext,command=exitProgram)
menubar2.add_cascade(label=file_menu2_cascade3_label_langtext,menu=file_menu2,underline=0)
        #edit_menu
edit_menu2 = tk.Menu(menubar2,tearoff = False)#das erste edit menu, aber ist in menubar 2, der übersicht halber ist das nummer 2
edit_menu2.add_command(label = edit_menu2_command1_label_langtext,command = topInPlaylist)
edit_menu2.add_command(label = edit_menu2_command2_label_langtext,command = upInPlaylist)
edit_menu2.add_command(label = edit_menu2_command3_label_langtext,command = downInPlaylist)
edit_menu2.add_command(label = edit_menu2_command4_label_langtext,command = bottomInPlaylist)
edit_menu2.add_command(label = edit_menu2_command5_label_langtext,command = delFrompllst)
edit_menu2.add_command(label = edit_menu2_command6_label_langtext,command = delDuplicates)
edit_menu2.add_command(label = edit_menu2_command7_label_langtext,command = deleteAllSongs)
menubar2.add_cascade(label = menubar2_cascade1_label_langtext,menu = edit_menu2,underline = 0)

#variables
sliderVar = tk.IntVar()
sliderVarExtra = tk.IntVar()
sliderVarMini = tk.IntVar()
volume = tk.IntVar()
filesToKeep = tk.IntVar()
volumeSliderTextOnOff = tk.BooleanVar()
loopPlaylist = tk.BooleanVar()
loopMove = tk.BooleanVar()
twoWindows = tk.BooleanVar()
miniModeActive = tk.BooleanVar()
shuffleReset = tk.BooleanVar()
languageStringVar = tk.StringVar()
languageStringVar.set(language)
#variables from settings
    #settings.txt
filepath_settings = os.path.join(dirname,"texts/settings.txt")
with open(filepath_settings,'r') as file:
    lines = file.readlines()
volumeText = lines[0]
volume.set(100 - int(volumeText[:-1]))
player.audio_set_volume(int(volumeText))
volumeSliderString = lines[1]
volumeSliderText = volumeSliderString[:-1]
volumeSliderTextOnOff.set(bool(volumeSliderText))
loopPlaylistString = lines[2]
loopPlaylistText = loopPlaylistString[:-1]
loopPlaylist.set(bool(loopPlaylistText))
loopMoveString = lines[3]
loopMoveText = loopMoveString[:-1]
loopMove.set(bool(loopMoveText))
twoWindowsString = lines[4]
twoWindowsText = twoWindowsString[:-1]
twoWindows.set(bool(twoWindowsText))
filesToKeepText = lines[5]
filesToKeep.set(int(filesToKeepText))
shuffleResetString = lines[7]
shuffleResetText = shuffleResetString[:-1]
shuffleReset.set(bool(shuffleResetText))
    #recent_files.txt
filepath_recent_files = os.path.join(dirname,"texts/recent_files.txt")
with open(filepath_recent_files,'r') as file:
    lines = file.readlines()
recentFiles = [] + lines
    #recent_files.txt
filepath_recent_songs = os.path.join(dirname,"texts/recent_songs.txt")
with open(filepath_recent_songs,'r') as file:
    lines = file.readlines()
recentSongs = [] + lines
    #recent_playlists.txt
filepath_recent_playlists = os.path.join(dirname,"texts/recent_playlists.txt")
with open(filepath_recent_playlists,'r') as file:
    lines = file.readlines()
recentPlaylists = [] + lines
print(recentFiles)
print(recentPlaylists)
print(recentSongs)
#variables for start
playlist = []
pPlaylist = []#played playlist
messageInfoLog = []
messageWarningLog = []
messageErrorLog = []
selectedLog = "0"
songLengthSeconds = 100
songPosition = "00:00"
songLength = "00:00"
playlistLength = "00:00:00"
remainingPlaylistLength = "00:00:00"
plstSelection = "0/0"
songName = songName_variable_langtext
songArtist = songArtist_variable_langtext
songFilename = songFilename_variable_langtext
cursor_state = "normal"
sliderPressed = False
volumePressed = False
exiting = False
ThreadStopped = False
plWtitleNameTrue = False
numberforminimode_main_window = 1
numberforminimode_plW = 1

#images
#print(os.path.join(dirname,'vlc\libvlc.dll'))
if platform.system() == "Windows":
    default_icon = os.path.join(dirname,'icons/default_icon.ico')
    playlist_icon = os.path.join(dirname,'icons/playlist_icon.ico')
    info_icon = os.path.join(dirname,'icons/info.ico')
    settings_icon = os.path.join(dirname,'icons/settings.ico')
    warning_icon = os.path.join(dirname,'icons/warning.ico')
    error_icon = os.path.join(dirname,'icons/error.ico')
    message_icon = os.path.join(dirname,'icons/message.ico')
    #loading_icon_1 = os.path.join(dirname,'icons/loading_1.ico')
    #loading_icon_2 = os.path.join(dirname,'icons/loading_2.ico')
    #loading_icon_3 = os.path.join(dirname,'icons/loading_3.ico')
elif platform.system() == "Linux":
    default_icon = tk.PhotoImage(file = os.path.join(dirname,'icons/default_icon.png'))
    playlist_icon = tk.PhotoImage(file = os.path.join(dirname,'icons/playlist_icon.png'))
    info_icon = tk.PhotoImage(file = os.path.join(dirname,'icons/info_icon.png'))
    settings_icon = tk.PhotoImage(file = os.path.join(dirname,'icons/settings_icon.png'))
    warning_icon = tk.PhotoImage(file = os.path.join(dirname,'icons/warning_icon.png'))
    error_icon = tk.PhotoImage(file = os.path.join(dirname,'icons/error_icon.png'))
    message_icon = tk.PhotoImage(file = os.path.join(dirname,'icons/message_icon.png'))
app_logo_image = tk.PhotoImage(file = os.path.join(dirname,'icons/default_icon_no_text_smol.png'))
app_logo_image_smol = tk.PhotoImage(file = os.path.join(dirname,'icons/default_icon_no_text_vewy_smol.png'))
exit_button_image = tk.PhotoImage(file = os.path.join(dirname,'icons/quit_smol.png'))
settings_button_image = tk.PhotoImage(file = os.path.join(dirname,'icons/settings_smol.png'))
info_button_image = tk.PhotoImage(file = os.path.join(dirname,'icons/info_smol.png'))
forward_button_image = tk.PhotoImage(file = os.path.join(dirname,'icons/forward_smol.png'))
forward_button_image_smol = tk.PhotoImage(file = os.path.join(dirname,'icons/forward_vewy_smol.png'))
rewind_button_image = tk.PhotoImage(file = os.path.join(dirname,'icons/rewind_smol.png'))
rewind_button_image_smol = tk.PhotoImage(file = os.path.join(dirname,'icons/rewind_vewy_smol.png'))
stop_image = tk.PhotoImage(file = os.path.join(dirname,'icons/stop_smol.png'))
stop_image_smol = tk.PhotoImage(file = os.path.join(dirname,'icons/stop_vewy_smol.png'))
play_image = tk.PhotoImage(file = os.path.join(dirname,'icons/play_smol.png'))
play_image_smol = tk.PhotoImage(file = os.path.join(dirname,'icons/play_vewy_smol.png'))
pause_image = tk.PhotoImage(file = os.path.join(dirname,'icons/pause_smol.png'))
pause_image_smol = tk.PhotoImage(file = os.path.join(dirname,'icons/pause_vewy_smol.png'))
#song_cover_image = tk.PhotoImage(file = os.path.join(dirname,'icons/cover_black_smol.png'))
#song_cover_image = tk.PhotoImage(file = os.path.join(dirname,'icons/cover_white_smol.png'))
#song_cover_image = tk.PhotoImage(file = os.path.join(dirname,'icons/cover_smol.png'))
#song_cover_image = tk.PhotoImage(file = os.path.join(dirname,'icons/cover_grey_smol.png'))
song_cover_image = tk.PhotoImage(file = os.path.join(dirname,'icons/default_icon_no_text_smol.png'))
#song_cover_image_smol = tk.PhotoImage(file = os.path.join(dirname,'icons/cover_black_vewy_smol.png'))
#song_cover_image_smol = tk.PhotoImage(file = os.path.join(dirname,'icons/cover_white_vewy_smol.png'))
#song_cover_image_smol = tk.PhotoImage(file = os.path.join(dirname,'icons/cover_vewy_smol.png'))
#song_cover_image_smol = tk.PhotoImage(file = 'os.path.join(dirname,icons/cover_grey_vewy_smol.png'))
song_cover_image_smol = tk.PhotoImage(file = os.path.join(dirname,'icons/default_icon_no_text_vewy_smol.png'))
#song_cover_image_temp = tk.PhotoImage(file = os.path.join(dirname, 'temporary_song_cover.png'))
#song_cover_image_temp_smol = tk.PhotoImage(file = os.path.join(dirname, 'temporary_song_cover_smol.png'))
delete_from_playlist_button_image = tk.PhotoImage(file = os.path.join(dirname,'icons/delete_from_playlist_smol.png'))
up_in_playlist_image = tk.PhotoImage(file = os.path.join(dirname,'icons/up_smol.png'))
down_in_playlist_image = tk.PhotoImage(file = os.path.join(dirname,'icons/down_smol.png'))
top_in_playlist_image = tk.PhotoImage(file = os.path.join(dirname,'icons/to_top_smol.png'))
bottom_in_playlist_image = tk.PhotoImage(file = os.path.join(dirname,'icons/to_bottom_smol.png'))
add_to_playlist_image = tk.PhotoImage(file = os.path.join(dirname,'icons/add_smol.png'))
save_playlist_image = tk.PhotoImage(file = os.path.join(dirname,'icons/save_playlist_smol.png'))
#shuffle_playlist_image = tk.PhotoImage(file = os.path.join(dirname,'icons/shuffle_pixel_perfect_smol.png'))
#shuffle_playlist_image = tk.PhotoImage(file = os.path.join(dirname,'icons/shuffle_freepik_1_smol.png'))
#shuffle_playlist_image = tk.PhotoImage(file = os.path.join(dirname,'icons/shuffle_freepik_2_smol.png'))
shuffle_playlist_image = tk.PhotoImage(file = os.path.join(dirname,'icons/shuffle_freepik_3_smol.png'))
left_image = tk.PhotoImage(file = os.path.join(dirname,'icons/left_smol.png'))
loading_image_1 = tk.PhotoImage(file = os.path.join(dirname,'icons/loading_1_smol.png'))
loading_image_2 = tk.PhotoImage(file = os.path.join(dirname,'icons/loading_2_smol.png'))
loading_image_3 = tk.PhotoImage(file = os.path.join(dirname,'icons/loading_3_smol.png'))

#window_icons
#nachricht löschen (text auf default icon größer machen)
main_window.resizable(False,False)
if platform.system() == "Windows":
    main_window.iconbitmap(default_icon)
    plW.iconbitmap(playlist_icon)
elif platform.system() == "Linux":
    main_window.iconphoto(False,default_icon)
    plW.iconphoto(False,playlist_icon)

#frames
    #main_window
toolbarFrame = ttk.Frame(main_window,width = 50)
toolbarFrame.pack(side = tk.LEFT,fill = tk.Y)
musicControlFrame = ttk.Frame(main_window,height = 100)
musicControlFrame.pack(side = tk.BOTTOM,fill = tk.X)
sliderFrame = ttk.Frame(main_window)
sliderFrame.pack(side = tk.BOTTOM,fill = tk.X,padx = 10)
songInfoFrame = ttk.Frame(main_window)
songInfoFrame.pack(side = tk.BOTTOM,fill = tk.X,padx = 10)
songCoverFrame = ttk.Frame(main_window,width = 200,height = 200)
songCoverFrame.pack(anchor = tk.CENTER,pady = 5)
    #playlist window
btmBtnsFrame = ttk.Frame(plW,height = 50)#bottom buttons
btmBtnsFrame.pack(side = tk.BOTTOM,fill = tk.X)
sdBtnsFrame = ttk.Frame(plW,width = 50)#side buttons
sdBtnsFrame.pack(side = tk.RIGHT,fill = tk.Y)
playlistFrame = ttk.Frame(plW)
playlistFrame.pack(side = tk.TOP,expand = True,fill = tk.BOTH)

#main_window
    #toolbarFrame
exitButton = tk.Button(toolbarFrame,image = exit_button_image,command = exitProgram,borderwidth = 0)
exitButton.pack(side = tk.BOTTOM,anchor = tk.S)
settingsButton = tk.Button(toolbarFrame,image = settings_button_image,command = lambda: (windowExtra("settings")),borderwidth = 0)
settingsButton.pack(side = tk.BOTTOM)
infoButton = tk.Button(toolbarFrame,image = info_button_image,command = lambda: (windowExtra("info")),borderwidth = 0)
infoButton.pack(side = tk.BOTTOM)
if volumeSliderText == "True":
    volumeInfo = ttk.Label(toolbarFrame,text = volumeText)
    volumeInfo.pack(side = tk.TOP)
volumeSlider = ttk.Scale(toolbarFrame,variable = volume,from_ = 0,to = 100,orient = 'vertical')
volumeSlider.bind("<Motion>",changeVolume)
volumeSlider.bind("<ButtonRelease-1>",volumePressedFalse)
volumeSlider.bind("<ButtonPress-1>",volumePressedTrue)
volumeSlider.pack(side = tk.BOTTOM,fill = tk.Y,expand = True,pady = 10)

    #musicControlFrame
forwardButton = tk.Button(musicControlFrame,image = forward_button_image,command = fastForward,borderwidth = 0)
forwardButton.pack(side = tk.RIGHT)
rewindButton = tk.Button(musicControlFrame,image = rewind_button_image,command = rewindSong,borderwidth = 0)
rewindButton.pack(side = tk.LEFT)
togglePlayButton = tk.Button(musicControlFrame,image = stop_image,command = togglePlay,borderwidth = 0)
togglePlayButton.pack()

    #sliderFrame (slider etc frame [maybe numbers {halt die länge des songs und wie lange er schon geht/noch geht} too, maybe extra frame for these]
songPositionText = ttk.Label(sliderFrame,text = songPosition)
songPositionText.pack(side = tk.LEFT)
songLengthText = ttk.Label(sliderFrame,text = songLength)
songLengthText.pack(side = tk.RIGHT)
musicSlider = ttk.Scale(sliderFrame,variable = sliderVar,from_ = 0,to = songLengthSeconds,orient = 'horizontal')
musicSlider.bind("<Motion>",sliderChangePos)
    #benutzen
#    songTime = str(datetime.timedelta(seconds = sliderVar.get()))
#    print(songTime)
#    print(songMS)
#    dot = songTime.rfind(".")
#    doubledot = songTime.rfind(":")
#    songTimeFin = songTime[doubledot - 2:dot]
#    print(songTimeFin)
#    songPositionText.config(text = songTimeFin)
musicSlider.bind("<ButtonRelease-1>",sliderChange)
musicSlider.bind("<ButtonPress-1>",sliderPressedTrue)
musicSlider.pack(side = tk.LEFT,fill = tk.X,expand = True)

    #songInfoFrame
songArtistText = ttk.Label(songInfoFrame,text = songArtist)
songArtistText.pack(side = tk.LEFT)
songNameText = ttk.Label(songInfoFrame,text = songName)
songNameText.pack(side = tk.RIGHT)

    #songCoverFrame
songCover = ttk.Label(songCoverFrame,image = song_cover_image)
songCover.pack(ipady = 20)

#playlist window
    #btmBtnsFrame
addToPlaylistButton = ttk.Button(btmBtnsFrame,image = add_to_playlist_image,command = lambda: (addToPlaylist("no")))
addToPlaylistButton.pack(side = tk.LEFT)
savePlaylistButton = ttk.Button(btmBtnsFrame,image = save_playlist_image,command = savePlaylist)
savePlaylistButton.pack(side = tk.LEFT)
playSelectedSongButton = ttk.Button(btmBtnsFrame,image = play_image_smol,command = playFromPlaylist)
playSelectedSongButton.pack(side = tk.RIGHT)
shufflePlaylistButton = ttk.Button(btmBtnsFrame,image = shuffle_playlist_image,command = shufflePlaylist)
shufflePlaylistButton.pack(side = tk.RIGHT)

    #sdBtnsFrame
toTopInPlaylistButton = ttk.Button(sdBtnsFrame,image = top_in_playlist_image,command = topInPlaylist)
toTopInPlaylistButton.pack(side = tk.TOP)
upInPlaylistButton = ttk.Button(sdBtnsFrame,image = up_in_playlist_image,command = upInPlaylist)
upInPlaylistButton.pack(side = tk.TOP)
deleteButton = ttk.Button(sdBtnsFrame,image = delete_from_playlist_button_image,command = delFrompllst)
deleteButton.pack(side = tk.TOP)
downInPlaylistButton = ttk.Button(sdBtnsFrame,image = down_in_playlist_image,command = downInPlaylist)
downInPlaylistButton.pack(side = tk.TOP)
toBottomInPlaylistButton = ttk.Button(sdBtnsFrame,image = bottom_in_playlist_image,command = bottomInPlaylist)
toBottomInPlaylistButton.pack(side = tk.TOP)

    #playlistFrame
        #treeview
columns = ('Title','Artist','length','count')

tree = ttk.Treeview(playlistFrame,columns = columns,show = 'headings')

tree.heading('Title',text = tree_heading1_text_langtext)
tree.heading('Artist',text = tree_heading2_text_langtext)
tree.heading('length',text = tree_heading3_text_langtext)
tree.column('Title',width = 150)
tree.column('Artist',width = 150)
tree.column('length',width = 50)
tree.column('count',width = 0,stretch = False)

tree.tag_configure("playing", foreground="green")
tree.tag_configure("not_playing",foreground = "black")

tree.pack(side = tk.LEFT,fill = tk.Y)
tree.bind('<Motion>','break')

tree.bind('<Double-1>',playFromPlaylistEvent)

#right click menu
rcmenu1 = tk.Menu(tree,tearoff = 0)#right click menu
rcmenu1.add_command(label = rcmenu1_command1_label_langtext,command = deleteAllSongs)
rcmenu1.add_command(label = rcmenu1_command2_label_langtext,command = delDuplicates)

rcmenu2 = tk.Menu(tree,tearoff = 0)
rcmenu2.add_command(label = rcmenu2_command1_label_langtext,command = topInPlaylist)
rcmenu2.add_command(label = rcmenu2_command2_label_langtext,command = upInPlaylist)
rcmenu2.add_command(label = rcmenu2_command3_label_langtext,command = downInPlaylist)
rcmenu2.add_command(label = rcmenu2_command4_label_langtext,command = bottomInPlaylist)
rcmenu2.add_command(label = rcmenu2_command5_label_langtext,command = delFrompllst)
rcmenu2.add_separator()
tree.bind("<Button-3>",rcmenuCheck)# event:rcmenu1.post(event.x_root,event.y_root))

#FRAMES
btmBtnsFFrame = ttk.Frame(btmBtnsFrame)#bottom buttons frame frame
btmBtnsFFrame.pack(fill = tk.X)

selectedSongFrame = ttk.Frame(btmBtnsFFrame)
selectedSongFrame.pack(side = tk.TOP,fill = tk.X)
lengthFrame = ttk.Frame(btmBtnsFFrame)
lengthFrame.pack(side = tk.TOP,fill = tk.X)
remainingLengthFrame = ttk.Frame(btmBtnsFFrame)
remainingLengthFrame.pack(side = tk.TOP,fill = tk.X)

    #selectedSongFrame
playlistSelectedLabel = ttk.Label(selectedSongFrame,text = playlistSelectedLabel_text_langtext)#vlt hier überall das "label" wegnehmen
playlistSelectedLabel.pack(side = tk.LEFT)
plstSelectionLabel = ttk.Label(selectedSongFrame,text = plstSelection)
plstSelectionLabel.pack(side = tk.RIGHT)

    #lengthFrame
playlistDurationLabel = ttk.Label(lengthFrame,text = playlistDurationLabel_text_langtext)
playlistDurationLabel.pack(side = tk.LEFT)
playlistLengthLabel = ttk.Label(lengthFrame,text = playlistLength)
playlistLengthLabel.pack(side = tk.RIGHT)

    #remainingLengthFrame
remainingPlaylistDurationLabel = ttk.Label(remainingLengthFrame,text = remainingPlaylistDurationLabel_text_langtext)
remainingPlaylistDurationLabel.pack(side = tk.LEFT)
remainingPlaylistLengthLabel = ttk.Label(remainingLengthFrame,text = remainingPlaylistLength)
remainingPlaylistLengthLabel.pack(side = tk.RIGHT)

        #scrollbar
scrollbar = ttk.Scrollbar(playlistFrame,orient = tk.VERTICAL,command = tree.yview)
tree.configure(yscroll = scrollbar.set)
scrollbar.pack(side = tk.RIGHT,fill = tk.Y)

#window bindings
    #toggle play
main_window.bind_all('<space>',togglePlayKey)
main_window.bind_all('<Pause>',togglePlayKey)
    #add to playlist
main_window.bind_all('<Control-o>',addToPlaylistKey)
    #delete from playlist
#main_window.bind("<Delete>",delFrompllstKey)#probably nicht
plW.bind("<Delete>",delFrompllstKey)
    #move in playlist
plW.bind("<Up>",upInPlaylistKey)
plW.bind("<Down>",downInPlaylistKey)
plW.bind("<Left>",topInPlaylistKey)
plW.bind("<Right>",bottomInPlaylistKey)
    #volume
main_window.bind_all("<plus>",changeVolumeUpKey)
main_window.bind_all("<minus>",changeVolumeDownKey)
    #skip/rewind
main_window.bind("<Right>",fastForwardKey)
main_window.bind("<Left>",rewindSongKey)
    #step skip/rewind
main_window.bind("<Shift-Right>",stepFastForwardKey)
main_window.bind("<Shift-Left>",stepRewindSongKey)
    #open settings
#main_window.bind_all('i',windowExtra("info"))
#main_window.bind_all('I',windowExtra("info"))
    #open info page/window
#main_window.bind_all('s',windowExtra("settings"))
#main_window.bind_all('S',windowExtra("settings"))
main_window.protocol("WM_DELETE_WINDOW", exitProgram)
plW.protocol("WM_DELETE_WINDOW", exitProgram)

#end
refreshRecentFiles()
plW.mainloop()
main_window.mainloop()

#verschiedene sprachen, du brauchst eine textdatei wo alle dinge drinstehen, und die nennst du dann "language_Deutsch.txt", und die englische wird dann eben "language_United States.txt". das programm guckt dann eben in einem ornder (maybe in einem eigenen maysbe in dem texts ornder) nach allen ("language_...") dateien, und zeigt in eionem dropdown menü alle optionen an, sodass man dann da eine auswählen kann. vlt schaffst du den wechsel sogar ohne das programm neuzustarten
#vlt eine option zum verändern des styles/themes, der farben/(zumindest) der farbe des ausgewählten elements in der playlist
#auf meinem linux pc (der kleine) wird nicht der gesamte text von length im playlist fenster angezeigt
#entweder das extra window (wieder ig) nicht größenverstellbar machen, oder gucken, ob das programm vlt doch größenverstellbar sein kann
#option machen, mit der man anschalten kann, dass songs aus playlisten auch in den recent songs angezeigt werden
#wenn man zu einem anderen song skipped bevor er fertig geladen hat, gibt es einen fehler
#ein rechtsklick menü für jeden song und eine option im menu. metadata_editor() beim menü und beim rechtsklick metadata_editor.loadFiles(ausgewählter songs)
#anstelle von show the value of the volume slider mb display the value...
#die attribution und info dateien und so übersetzen
