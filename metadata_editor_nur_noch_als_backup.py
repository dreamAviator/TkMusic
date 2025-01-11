    #TkMetadata
    #This program can edit the metadata of audio files.
    #It is integrated in TkMusic, but can be used seperately.
    #Copyright (C) 2024 Lilly, dreamAviator, Nathan Baron
#gui
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from PyQt5.QtWidgets import QApplication, QFileDialog
#(song cover)
#metadata
import mutagen
from mutagen import File
from mutagen.mp4 import MP4, MP4Tags
from mutagen.id3 import ID3, TIT2, TPE1, TALB
#file tasks
import shutil
import os
#other
import webbrowser
from threading import *
import sys

def loadFiles():
    global filenamesME
    filenamesMEtemp = openFilesDialog()
    for filename in filenamesMEtemp:
        filenamesME.append(filename)
    fileCountTextBEME.config(text = str(len(filenamesME)) + " File/s")
    for filename in filenamesME:
        selectedFilesTreeBEME.insert('',tk.END,values = (filename))
        selectedFilesTreeSEME.insert('',tk.END,values = (filename))
        selectedFilesTreeREME.insert('',tk.END,values = (filename))

def deleteFiles():
    pass

def start():
    global saveDirectoryME
    global filenamesME
    filenamesMEtwo = []
    if saveDirectoryME == "":
        print("error")
        return
    if filenamesME == []:
        print("error")
        return
    for song in filenamesME:
        print("cpying " + song)
        lastslash = song.rfind("/")
        songName = song[lastslash + 1:]
        shutil.copy(song,saveDirectoryME + "/" + songName)
        filenamesMEtwo.append(saveDirectoryME + "/" + songName)
    selectedMode = modesME.index(modesME.select())
    if selectedMode == 1:
        pattern = namePattern.get()
        print(pattern)
        if "%" not in pattern:
            print("error")
            return
        pattern_data = []
        while len(pattern) != 1:
            pattern = pattern[1:]
            where = pattern.find("%")
            pattern_data.append(pattern[:where])
            pattern = pattern[where:]
        for song in filenamesMEtwo:
            lastslash = song.rfind("/")
            songName = song[lastslash + 1:]
            fileExtension = songName.rfind('.')
            title = ""
            interpreter = ""
            album = ""
            songNameToEdit = songName[:-4]
            for i in range(len(pattern_data)):
                element = pattern_data[i]
                print("element")
                print(element)
                print("songNameToEdit")
                print(songNameToEdit)
                print("title")
                print(title)
                print("interpreter")
                print(interpreter)
                if element != "t" and element != "i" and element != "a":
                    where = songNameToEdit.find(element)
                    songNameToEdit = songNameToEdit[where + len(element):]
                else:
                    if i != len(pattern_data) - 1:
                        elementtwo = pattern_data[i + 1]
                        wheretwo = songNameToEdit.find(elementtwo)
                        if element == "t":
                            title = songNameToEdit[:wheretwo]
                        elif element == "i":
                            interpreter = songNameToEdit[:wheretwo]
                        elif element == "a":
                            album = songNameToEdit[:wheretwo]
                    else:
                        if element == "t":
                            title = songNameToEdit
                        elif element == "i":
                            interpreter = songNameToEdit
                        elif element == "a":
                            album = songNameToEdit

            print("song " + song)
            print("title " + title)
            print("interpreter " + interpreter)
            print("album " + album)
            if title != "":
                if songName[fileExtension + 1:] == 'mp3' or songName[fileExtension + 1:] == 'MP3':
                    audioToEdit = ID3(song)
                    audioToEdit["TIT2"] = TIT2(encoding=3, text=title)
                    audioToEdit.save()
                elif songName[fileExtension + 1:] == 'm4a' or songName[fileExtension + 1:] == 'M4A':
                    audioToEdit = MP4(song)
                    tags = audioToEdit.tags
                    tags["\xa9nam"] = title
                    audioToEdit.save()
            if interpreter != "":
                if songName[fileExtension + 1:] == 'mp3' or songName[fileExtension + 1:] == 'MP3':
                    audioToEdit = ID3(song)
                    audioToEdit["TPE1"] = TPE1(encoding=3, text=interpreter)
                    audioToEdit.save()
                elif songName[fileExtension + 1:] == 'm4a' or songName[fileExtension + 1:] == 'M4A':
                    audioToEdit = MP4(song)
                    tags = audioToEdit.tags
                    tags["\xa9ART"] = interpreter
                    audioToEdit.save()
            if album != "":
                if songName[fileExtension + 1:] == 'mp3' or songName[fileExtension + 1:] == 'MP3':
                    audioToEdit = ID3(song)
                    audioToEdit["TALB"] = TALB(encoding=3, text=album)
                    audioToEdit.save()
                elif songName[fileExtension + 1:] == 'm4a' or songName[fileExtension + 1:] == 'M4A':
                    audioToEdit = MP4(song)
                    tags = audioToEdit.tags
                    tags["\xa9alb"] = album
                    audioToEdit.save()

def startEvent(event):
    start()

def namePatternHelp():#einf eine help message sache machen.
    pass


#system
def whereSave():
    global saveDirectoryME
    saveDirectoryME = openDirectoryDialog()
    selectedMode = modesME.index(modesME.select())
    if selectedMode == 1:
        whereSaveButtonME.config(text = saveDirectoryME)

def exit():
    sys.exit()

def exitEvent(event):
    exit()
#gui
def openFilesDialog():
    app = QApplication(sys.argv)
    options = QFileDialog.Options()
    options |= QFileDialog.ReadOnly
    files,_ = QFileDialog.getOpenFileNames(None,"Select Audio Files","","All Files (*)",options = options)#hier noch einmal nur supported oder tested oder so hinzufügen
    return files

def openDirectoryDialog():
    app = QApplication(sys.argv)
    options = QFileDialog.Options()
    options |= QFileDialog.ShowDirsOnly | QFileDialog.ReadOnly
    directory = QFileDialog.getExistingDirectory(None, "Select Directory", "", options=options)
    return directory

def notebookTabMEChange(event):
    selectedTab = modesME.index(modesME.select())
    if selectedTab == 0:
        modesME.select(1)#hier halt den vorher ausgewählten
        start()
    elif selectedTab == 5:
        exit()
    else:#write in settingsME yk
        pass

def buildUI():
    metadataWindow.deiconify()

#tkinter
metadataWindow = tk.Tk()
metadataWindow.title("TkMetaEditor")
metadataWindow.geometry('500x360+100+100')
metadataWindow.resizable(False,False)
#icon hier
#metadataWindow.bind('<Return>',startEvent)
#metadataWindow.bind('<Escape>',exitEvent)

#variables
filenamesME = []
notebookTabME = 1#das halt durch die settingsME auslesen. der letzte geöffnete tab
#du kannst maybe die gleiche settingsME datei verwenden wie für den music player
namePattern = tk.StringVar()
saveDirectoryME = ""

modesME = ttk.Notebook(metadataWindow)
modesME.pack(side = tk.TOP,fill = tk.BOTH)
startTabME = ttk.Frame(modesME)
batchEditME = ttk.Frame(modesME)
singleEditME = ttk.Frame(modesME)
renameME = ttk.Frame(modesME)
settingsME = ttk.Frame(modesME)
quitTabME = ttk.Frame(modesME)

modesME.add(startTabME,text = "Start")
modesME.add(batchEditME,text = "Batch edit")
modesME.add(singleEditME,text = "Single edit")
modesME.add(renameME,text = "Rename")
modesME.add(settingsME,text = "Settings")
modesME.add(quitTabME,text = "Quit")
modesME.select(notebookTabME)
modesME.bind('<<NotebookTabChanged>>',notebookTabMEChange)

columnsME = ('File')

progressbarBEME = ttk.Progressbar(metadataWindow,orient = 'horizontal',mode = 'determinate',length = 500)
progressbarBEME.pack(side = tk.BOTTOM)
separatorBE1ME = ttk.Separator(metadataWindow,orient = 'horizontal')
separatorBE1ME.pack(side = tk.BOTTOM,fill = tk.X,pady = 10)

#batchEditME - be
selectFilesFrameBEME = ttk.Frame(batchEditME)
selectFilesFrameBEME.pack(side = tk.TOP,fill = tk.X)
selectFilesFrameInnerBEME = ttk.Frame(selectFilesFrameBEME)
selectFilesFrameInnerBEME.pack(side = tk.LEFT)
namePatternFrameME = ttk.Frame(batchEditME)
namePatternFrameME.pack(side = tk.TOP,fill = tk.X)

fileCountTextBEME = ttk.Label(selectFilesFrameInnerBEME,text = "0 File/s")
fileCountTextBEME.pack(side = tk.BOTTOM)
deleteFilesButtonBEME = ttk.Button(selectFilesFrameInnerBEME,text = "Delete Files",command = deleteFiles)
deleteFilesButtonBEME.pack(side = tk.BOTTOM)
deleteFilesButtonBEME = ttk.Button(selectFilesFrameInnerBEME,text = "Select Files",command = loadFiles)
deleteFilesButtonBEME.pack(side = tk.BOTTOM,fill = tk.X)
scrollbarBEME = ttk.Scrollbar(selectFilesFrameBEME)
selectedFilesTreeBEME = ttk.Treeview(selectFilesFrameBEME,yscrollcommand = scrollbarBEME.set,columnsME = columnsME,show = "headings",height = 4)
scrollbarBEME.configure(command = selectedFilesTreeBEME.yview)
scrollbarBEME.pack(side = tk.RIGHT,fill = tk.Y)
selectedFilesTreeBEME.pack(side = tk.LEFT,fill = tk.X,expand = True)

namePatternTextME = ttk.Label(namePatternFrameME,text = "Naming pattern")
namePatternTextME.pack(side = tk.TOP,anchor = tk.NW)
namePatternHelpButtonME = ttk.Button(namePatternFrameME,text = "What's that?",command = namePatternHelp)
namePatternHelpButtonME.pack(side = tk.RIGHT)
namePatternEntryME = ttk.Entry(namePatternFrameME,textvariable = namePattern)
namePatternEntryME.pack(side = tk.LEFT,fill = tk.X,expand = True)

whereSaveTextME = ttk.Label(batchEditME,text = "Save location")
whereSaveTextME.pack(side = tk.TOP,anchor = tk.NW)
whereSaveButtonME = ttk.Button(batchEditME,text = "Select folder",command = whereSave)
whereSaveButtonME.pack(side = tk.TOP,anchor = tk.NW)


#singleEditME - se
selectFilesFrameSEME = ttk.Frame(singleEditME)
selectFilesFrameSEME.pack(side = tk.TOP,fill = tk.X)
selectFilesFrameInnerSEME = ttk.Frame(selectFilesFrameSEME)
selectFilesFrameInnerSEME.pack(side = tk.LEFT)

fileCountTextSEME = ttk.Label(selectFilesFrameInnerSEME,text = "0 File/s")
fileCountTextSEME.pack(side = tk.BOTTOM)
deleteFilesButtonSEME = ttk.Button(selectFilesFrameInnerSEME,text = "Delete Files",command = deleteFiles)
deleteFilesButtonSEME.pack(side = tk.BOTTOM)

selectFilesButtonSEME = ttk.Button(selectFilesFrameSEME,text = "Select Files",command = loadFiles)
selectFilesButtonSEME.pack(side = tk.LEFT,anchor = tk.W)
scrollbarSEME = ttk.Scrollbar(selectFilesFrameSEME)
selectedFilesTreeSEME = ttk.Treeview(selectFilesFrameSEME,yscrollcommand = scrollbarSEME.set,columnsME = columnsME,show = "tree",height = 4)#find mal heraus wieso das hier nicht funktioniert
scrollbarSEME.configure(command = selectedFilesTreeSEME.yview)
scrollbarSEME.pack(side = tk.RIGHT,fill = tk.Y)
selectedFilesTreeSEME.pack(side = tk.RIGHT,fill = tk.X,expand = True)


#renameME - RE
selectFilesFrameREME = ttk.Frame(renameME)
selectFilesFrameREME.pack(side = tk.TOP,fill = tk.X)
selectFilesFrameInnerREME = ttk.Frame(selectFilesFrameREME)
selectFilesFrameInnerREME.pack(side = tk.LEFT)

fileCountTextREME = ttk.Label(selectFilesFrameInnerREME,text = "0 File/s")
fileCountTextREME.pack(side = tk.BOTTOM)
deleteFilesButtonREME = ttk.Button(selectFilesFrameInnerREME,text = "Delete Files",command = deleteFiles)
deleteFilesButtonREME.pack(side = tk.BOTTOM)
selectFilesButtonREME = ttk.Button(selectFilesFrameInnerREME,text = "Select Files",command = loadFiles)
selectFilesButtonREME.pack(side = tk.BOTTOM,fill = tk.X)
scrollbarREME = ttk.Scrollbar(selectFilesFrameREME)
selectedFilesTreeREME = ttk.Treeview(selectFilesFrameREME,yscrollcommand = scrollbarREME.set,columnsME = columnsME,show = "headings",height = 4)
scrollbarREME.configure(command = selectedFilesTreeREME.yview)
scrollbarREME.pack(side = tk.RIGHT,fill = tk.Y)
selectedFilesTreeREME.pack(side = tk.LEFT,fill = tk.X,expand = True)


metadataWindow.mainloop()