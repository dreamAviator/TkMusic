    #TkMetaEditor
    #This program can edit the metadata of audio files.
    #It is integrated in TkMusic, but can be used seperately.
    #Copyright (C) 2024 Lilly, dreamAviator, Nathan Baron
#g
#gui
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from PyQt5.QtWidgets import QApplication, QFileDialog
#(song cover)
#metadata
import mutagen
from mutagen import File
from mutagen.mp4 import MP4
from mutagen.id3 import ID3, TIT2, TPE1, TALB
#file tasks
import shutil
import os
#other
import webbrowser
from threading import *
import sys

def loadFiles():
    global filenames
    filenamestemp = openFilesDialog()
    for filename in filenamestemp:
        filenames.append(filename)
    fileCountTextBE.config(text = str(len(filenames)) + " File/s")
    for filename in filenames:
        selectedFilesTreeBE.insert('',tk.END,values = (filename))
        selectedFilesTreeSE.insert('',tk.END,values = (filename))
        selectedFilesTreeRE.insert('',tk.END,values = (filename))

def deleteFiles():
    pass

def start():
    global saveDirectory
    global filenames
    filenamestwo = []
    if saveDirectory == "":
        print("error")
        return
    if filenames == []:
        print("error")
        return
    for song in filenames:
        print("cpying " + song)
        lastslash = song.rfind("/")
        songName = song[lastslash + 1:]
        shutil.copy(song,saveDirectory + "/" + songName)
        filenamestwo.append(saveDirectory + "/" + songName)
    selectedMode = modes.index(modes.select())
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
        for song in filenamestwo:
            lastslash = song.rfind("/")
            songName = song[lastslash + 1:]
            fileExtension = songName.rfind('.')
            title = ""
            interpreter = ""
            album = ""
            for element in pattern_data:
                if len(element) != 1:
                    #halt irgendwie element entzfernen sodass du bnur noch den songnamen als titel,interpret,album hast oder so, idk, dafür wäre getrennt maybe euinfacher actually ;-;
                else:
                    songName.replace(element,"%"",1)
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
                    audioToEdit["\xa9nam"] = title
                    audioToEdit.save()
            if interpreter != "":
                if songName[fileExtension + 1:] == 'mp3' or songName[fileExtension + 1:] == 'MP3':
                    audioToEdit = ID3(song)
                    audioToEdit["TPE1"] = TPE1(encoding=3, text=interpreter)
                    audioToEdit.save()
                elif songName[fileExtension + 1:] == 'm4a' or songName[fileExtension + 1:] == 'M4A':
                    audioToEdit = MP4(song)
                    audioToEdit["\xa9art"] = interpreter
                    audioToEdit.save()
            if album != "":
                if songName[fileExtension + 1:] == 'mp3' or songName[fileExtension + 1:] == 'MP3':
                    audioToEdit = ID3(song)
                    audioToEdit["TALB"] = TALB(encoding=3, text=album)
                    audioToEdit.save()
                elif songName[fileExtension + 1:] == 'm4a' or songName[fileExtension + 1:] == 'M4A':
                    audioToEdit = MP4(song)
                    audioToEdit["\xa9alb"] = album
                    audioToEdit.save()

def startEvent(event):
    start()

def namePatternHelp():#einf eine help message sache machen.
    pass


#system
def whereSave():
    global saveDirectory
    saveDirectory = openDirectoryDialog()
    selectedMode = modes.index(modes.select())
    if selectedMode == 1:
        whereSaveButton.config(text = saveDirectory)

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

def notebookTabChange(event):
    selectedTab = modes.index(modes.select())
    if selectedTab == 0:
        modes.select(1)#hier halt den vorher ausgewählten
        start()
    elif selectedTab == 5:
        exit()
    else:#write in settings yk
        pass

#tkinter
root = tk.Tk()
root.title("TkMetaEditor")
root.geometry('500x360+100+100')
root.resizable(False,False)
#icon hier
#root.bind('<Return>',startEvent)
#root.bind('<Escape>',exitEvent)

#variables
filenames = []
notebookTab = 1#das halt durch die settings auslesen. der letzte geöffnete tab
#du kannst maybe die gleiche settings datei verwenden wie für den music player
namePattern = tk.StringVar()
saveDirectory = ""

modes = ttk.Notebook(root)
modes.pack(side = tk.TOP,fill = tk.BOTH)
startTab = ttk.Frame(modes)
batchEdit = ttk.Frame(modes)
singleEdit = ttk.Frame(modes)
rename = ttk.Frame(modes)
settings = ttk.Frame(modes)
quitTab = ttk.Frame(modes)

modes.add(startTab,text = "Start")
modes.add(batchEdit,text = "Batch edit")
modes.add(singleEdit,text = "Single edit")
modes.add(rename,text = "Rename")
modes.add(settings,text = "Settings")
modes.add(quitTab,text = "Quit")
modes.select(notebookTab)
modes.bind('<<NotebookTabChanged>>',notebookTabChange)

columns = ('File')

progressbarBE = ttk.Progressbar(root,orient = 'horizontal',mode = 'determinate',length = 500)
progressbarBE.pack(side = tk.BOTTOM)
separatorBE1 = ttk.Separator(root,orient = 'horizontal')
separatorBE1.pack(side = tk.BOTTOM,fill = tk.X,pady = 10)

#batchEdit - be
selectFilesFrameBE = ttk.Frame(batchEdit)
selectFilesFrameBE.pack(side = tk.TOP,fill = tk.X)
selectFilesFrameInnerBE = ttk.Frame(selectFilesFrameBE)
selectFilesFrameInnerBE.pack(side = tk.LEFT)
namePatternFrame = ttk.Frame(batchEdit)
namePatternFrame.pack(side = tk.TOP,fill = tk.X)

fileCountTextBE = ttk.Label(selectFilesFrameInnerBE,text = "0 File/s")
fileCountTextBE.pack(side = tk.BOTTOM)
deleteFilesButtonBE = ttk.Button(selectFilesFrameInnerBE,text = "Delete Files",command = deleteFiles)
deleteFilesButtonBE.pack(side = tk.BOTTOM)
selectFilesButtonBE = ttk.Button(selectFilesFrameInnerBE,text = "Select Files",command = loadFiles)
selectFilesButtonBE.pack(side = tk.BOTTOM,fill = tk.X)
scrollbarBE = ttk.Scrollbar(selectFilesFrameBE)
selectedFilesTreeBE = ttk.Treeview(selectFilesFrameBE,yscrollcommand = scrollbarBE.set,columns = columns,show = "headings",height = 4)
scrollbarBE.configure(command = selectedFilesTreeBE.yview)
scrollbarBE.pack(side = tk.RIGHT,fill = tk.Y)
selectedFilesTreeBE.pack(side = tk.LEFT,fill = tk.X,expand = True)

namePatternText = ttk.Label(namePatternFrame,text = "Naming pattern")
namePatternText.pack(side = tk.TOP,anchor = tk.NW)
namePatternHelpButton = ttk.Button(namePatternFrame,text = "What's that?",command = namePatternHelp)
namePatternHelpButton.pack(side = tk.RIGHT)
namePatternEntry = ttk.Entry(namePatternFrame,textvariable = namePattern)
namePatternEntry.pack(side = tk.LEFT,fill = tk.X,expand = True)

whereSaveText = ttk.Label(batchEdit,text = "Save location")
whereSaveText.pack(side = tk.TOP,anchor = tk.NW)
whereSaveButton = ttk.Button(batchEdit,text = "Select folder",command = whereSave)
whereSaveButton.pack(side = tk.TOP,anchor = tk.NW)


#singleEdit - se
selectFilesFrameSE = ttk.Frame(singleEdit)
selectFilesFrameSE.pack(side = tk.TOP,fill = tk.X)
selectFilesFrameInnerSE = ttk.Frame(selectFilesFrameSE)
selectFilesFrameInnerSE.pack(side = tk.LEFT)

fileCountTextSE = ttk.Label(selectFilesFrameInnerSE,text = "0 File/s")
fileCountTextSE.pack(side = tk.BOTTOM)
deleteFilesButtonSE = ttk.Button(selectFilesFrameInnerSE,text = "Delete Files",command = deleteFiles)
deleteFilesButtonSE.pack(side = tk.BOTTOM)

selectFilesButtonSE = ttk.Button(selectFilesFrameSE,text = "Select Files",command = loadFiles)
selectFilesButtonSE.pack(side = tk.LEFT,anchor = tk.W)
scrollbarSE = ttk.Scrollbar(selectFilesFrameSE)
selectedFilesTreeSE = ttk.Treeview(selectFilesFrameSE,yscrollcommand = scrollbarSE.set,columns = columns,show = "tree",height = 4)#find mal heraus wieso das hier nicht funktioniert
scrollbarSE.configure(command = selectedFilesTreeSE.yview)
scrollbarSE.pack(side = tk.RIGHT,fill = tk.Y)
selectedFilesTreeSE.pack(side = tk.RIGHT,fill = tk.X,expand = True)


#rename - RE
selectFilesFrameRE = ttk.Frame(rename)
selectFilesFrameRE.pack(side = tk.TOP,fill = tk.X)
selectFilesFrameInnerRE = ttk.Frame(selectFilesFrameRE)
selectFilesFrameInnerRE.pack(side = tk.LEFT)

fileCountTextRE = ttk.Label(selectFilesFrameInnerRE,text = "0 File/s")
fileCountTextRE.pack(side = tk.BOTTOM)
deleteFilesButtonRE = ttk.Button(selectFilesFrameInnerRE,text = "Delete Files",command = deleteFiles)
deleteFilesButtonRE.pack(side = tk.BOTTOM)
selectFilesButtonRE = ttk.Button(selectFilesFrameInnerRE,text = "Select Files",command = loadFiles)
selectFilesButtonRE.pack(side = tk.BOTTOM,fill = tk.X)
scrollbarRE = ttk.Scrollbar(selectFilesFrameRE)
selectedFilesTreeRE = ttk.Treeview(selectFilesFrameRE,yscrollcommand = scrollbarRE.set,columns = columns,show = "headings",height = 4)
scrollbarRE.configure(command = selectedFilesTreeRE.yview)
scrollbarRE.pack(side = tk.RIGHT,fill = tk.Y)
selectedFilesTreeRE.pack(side = tk.LEFT,fill = tk.X,expand = True)


root.mainloop()
