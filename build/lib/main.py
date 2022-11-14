import os
import threading
import time
from tkinter import *
from tkinter import filedialog

from tkinter import ttk
from ttkthemes import ThemedTk

from mutagen.mp3 import MP3
import tkinter.messagebox
from pygame import mixer

root = ThemedTk(theme="breeze")

statusbar = ttk.Label(root, text="Welcome to Melody", relief=SUNKEN, anchor="w", font='Times 10 italic')
statusbar.pack(side=BOTTOM, fill=X)
# Create the menubar
menubar = Menu(root)
root.config(menu=menubar)

# Create the Submenu
subMenu = Menu(menubar, tearoff=0)

playlist = []


# playlist - contains the full path + filename
# playlistbox - contains just the filename
# Fullpath + filename is required to play the music inside play_music load function

def browse_file():
    global filename_path
    filetypes_supportd = [("mp3", "*.mp3"), ("mp4", "*.mp4"), ("wav", "*.wav"), ("aac", "*.aac")]
    filename_path = filedialog.askopenfilename(filetypes=filetypes_supportd)
    add_to_playlist(filename_path)


playlistIndex = 0


def add_to_playlist(filename):
    global playlistIndex
    filename = os.path.basename(filename)
    playlistBox.insert(playlistIndex, filename)
    playlist.insert(playlistIndex, filename_path)
    playlistIndex += 1


menubar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open", command=browse_file)
subMenu.add_command(label="Exit", command=root.destroy)


def about_us():
    tkinter.messagebox.showinfo('About Melody', 'This is a music player build using python Tkinter by @bodharemayur')


subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About Us", command=about_us)

mixer.init()  # initializing the mixer

# root.geometry('300x300')
root.title("Melody")
root.iconbitmap(r'images/melody.ico')

# Root Window - statusbar, leftFrame, rightFrame
# leftFrame - The listbox (playlist)
# rightFrame - TopFrame, MiddleFrame and the BottomFrame

leftFrame = ttk.Frame(root)
leftFrame.pack(side=LEFT, padx=30, pady=30)

playlistBox = Listbox(leftFrame)
playlistBox.pack()

addBtn = ttk.Button(leftFrame, text="+ Add", command=browse_file)
addBtn.pack(side=LEFT)


def del_song():
    selected_song = playlistBox.curselection()
    selected_song = int(selected_song[0])
    playlistBox.delete(selected_song)
    playlist.pop(selected_song)
    print(playlist)


delBtn = ttk.Button(leftFrame, text="- Del", command=del_song)
delBtn.pack(side=LEFT)

rightFrame = ttk.Frame(root)
rightFrame.pack()

topFrame = ttk.Frame(rightFrame)
topFrame.pack()

lengthlable1 = ttk.Label(topFrame, text="Total Length: --:--")
lengthlable1.pack(pady=5)

current_time_lable1 = ttk.Label(topFrame, text="Current Length: --:--", relief=GROOVE)
current_time_lable1.pack()


def show_details(play_song):
    file_data = os.path.splitext(play_song)

    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()

    # div - total_length/60, mod - total_length%60
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    length_msg = "Total Length - " + timeformat
    lengthlable1['text'] = length_msg
    t1 = threading.Thread(target=start_count, args=(total_length,), daemon=True)
    t1.start()


def start_count(t):
    global paused
    # mixer.music.get_busy() - Returns False when we press the stop button (music stop playing)
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused == False:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            current_time_lable1['text'] = "Current Length - " + timeformat
            time.sleep(1)
            current_time += 1
        else:
            continue


def play_music():
    global paused
    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music Resumed"
        paused = False
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = playlistBox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "Playing music" + " " + os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror('File not found', 'Melody could not find the file. Please check again.')


def stop_music():
    mixer.music.stop()
    statusbar['text'] = "Music stopped"


def set_volume(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)
    # set_volume of mixer takes only from 0 to 1. Example = 0, 0.1, 0.55, 0.99,1


paused = False


def pause_music():
    global paused
    paused = True
    mixer.music.pause()
    statusbar['text'] = "Music paused"


def rewind_music():
    play_music()
    statusbar['text'] = "Music rewinded"


flag = False


def mute_music():
    global flag
    global vol
    if flag == False:  # mute the music
        global vol
        VolumeBtn.configure(image=mutePhoto)
        vol = mixer.music.get_volume()
        mixer.music.set_volume(0)
        scale.set(0)
        flag = True
    else:  # unmute the music
        VolumeBtn.configure(image=VolumePhoto)
        mixer.music.set_volume(vol)
        scale.set(vol * 100)
        flag = False


middleframe = ttk.Frame(rightFrame)
middleframe.pack(pady=30, padx=30)

PlayPhoto = PhotoImage(file='images/play.png')
PlayBtn = ttk.Button(middleframe, image=PlayPhoto, command=play_music)
PlayBtn.grid(row=0, column=0, padx=20)

StopPhoto = PhotoImage(file='images/stop.png')
StopBtn = ttk.Button(middleframe, image=StopPhoto, command=stop_music)
StopBtn.grid(row=0, column=1, padx=20)

PausePhoto = PhotoImage(file='images/pause.png')
PauseBtn = ttk.Button(middleframe, image=PausePhoto, command=pause_music)
PauseBtn.grid(row=0, column=2, padx=20)

bottomframe = Frame(rightFrame)
bottomframe.pack(pady=10)

RewindPhoto = PhotoImage(file='images/rewind.png')
RewindBtn = ttk.Button(bottomframe, image=RewindPhoto, command=rewind_music)
RewindBtn.grid(row=0, column=0)

mutePhoto = PhotoImage(file='images/mute.png')
VolumePhoto = PhotoImage(file='images/high-volume.png')
VolumeBtn = ttk.Button(bottomframe, image=VolumePhoto, command=mute_music)
VolumeBtn.grid(row=0, column=1)

scale = ttk.Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=set_volume)
scale.set(60)
global vol
vol = 0.6
mixer.music.set_volume(0.6)
scale.grid(row=0, column=2, pady=15, padx=30)


def on_closing():
    stop_music()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
