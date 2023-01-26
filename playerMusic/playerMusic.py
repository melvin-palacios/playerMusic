from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from random import randint
import pygame
import shutil
import os


window = Tk()
window.geometry("750x600")
window.title("playerMusic")
window.resizable(FALSE,FALSE)
window.config(bg="#424242")
onglet = ttk.Notebook(window)
onglet.config(width=750,height= 600)
onglet.pack()
frame1 = Frame(onglet, bg="#424242", width=750, height=600)
frame2 = Frame(onglet, bg="#424242", width=750, height=600)
frame1.pack(expand=1, fill=BOTH)
frame2.pack(expand=1, fill=BOTH)
onglet.add(frame1, text="Player")
onglet.add(frame2, text="Song")

pygame.mixer.init()

playlist = Listbox(frame2, bg="#424242", fg="white", width=120,height=30, selectbackground="#18CC42", selectforeground="black")
playlist.pack(pady=5)

pause_button_image = PhotoImage(file="img/pause.png")
play_button_image = PhotoImage(file="img/play-button.png")
stop_button_image = PhotoImage(file="img/stop-button.png")
repeat_button_image = PhotoImage(file="img/repeat.png")
repeat_button_image2 = PhotoImage(file="img/repeat blue.png")
back_button_image = PhotoImage(file="img/previous-track.png")
next_button_image = PhotoImage(file="img/next-track.png")
music_image = PhotoImage(file="img/musical-note.png")
shuffle_image = PhotoImage(file="img/shuffle.png")
shuffle_image2 = PhotoImage(file="img/shuffle_blue.png")
button_frame = Frame(frame1, bg="#424242")


# variable
loop = False
pause = False
shuffle = False
count = 0

# fonction part


def add_song():
    song = filedialog.askopenfilename(title="Choose a song", filetypes=(("mp3 Files", "*.mp3"),))
    target = "song/"
    if not os.path.exists(target):
        os.makedirs(target)
    shutil.copy(song, target)
    innit_playlist("song/")


def innit_playlist(folder):
    nb = 0
    i = 0
    while i < count_files(folder):
        title = files_titles(folder, i)
        title_button = Button(playlist, text=title, bg="#424242", fg="white"
                              , width=100, height=2, activebackground='#424242', relief='flat',borderwidth=0,
                              command=lambda nb=nb: play_song(nb))
        title_button.grid(row=i, column=0)
        nb += 1
        i += 1


def count_files(directory):
    return len([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])


def files_titles(directory, nb):
    song_title = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    return song_title[nb]


def random_song():
    nb = randint(0, count_files("song/")-1)
    print(nb)
    return nb

def play_song(nb):
    global count
    global loop
    global shuffle
    if nb == count_files("song/"):
        nb = 0
    elif nb < 0:
        nb = count_files("song/") - 1
    count = nb
    if shuffle == True:
        nb = random_song()
        song_title = [f for f in os.listdir("song") if os.path.isfile(os.path.join("song", f))]
        pygame.mixer.music.load(f"song/{song_title[nb]}")
        title_song.config(text=song_title[nb])
    else:
        song_title = [f for f in os.listdir("song") if os.path.isfile(os.path.join("song", f))]
        pygame.mixer.music.load(f"song/{song_title[nb]}")
        title_song.config(text=song_title[nb])
    pygame.mixer.music.play()
    play_button.config(image=pause_button_image)


def volume(x):
    pygame.mixer.music.set_volume(float(x))


def stop():
    pygame.mixer.music.stop()
    title_song.config(text="No song is played")


def pause_unpause():
    global pause
    if pause == False:
        pygame.mixer.music.pause()
        play_button.config(image=play_button_image)
        pause = True
    else:
        pygame.mixer.music.unpause()
        play_button.config(image=pause_button_image)
        pause = False


def play_next_song():
    global count
    global loop
    global shuffle
    if shuffle == True:
        nb = random_song()
        song_title = [f for f in os.listdir("song") if os.path.isfile(os.path.join("song", f))]
        pygame.mixer.music.load(f"song/{song_title[nb]}")
        title_song.config(text=song_title[nb])
        pygame.mixer.music.play()
    elif loop == True:
        pygame.mixer.music.play()
    else:
        count += 1
        play_song(count)


def play_previous_song():
    global count
    count -= 1
    play_song(count)

def loop_song():
    global loop
    if loop == False:
        repeat_button.config(image=repeat_button_image2)
        loop = True
    else:
        repeat_button.config(image=repeat_button_image)
        loop = False


def random1():
    global shuffle
    if shuffle == False:
        shuffle_button.config(image=shuffle_image2)
        shuffle = True
    else:
        shuffle_button.config(image=shuffle_image)
        shuffle = False


# label part
title_song = Label(frame1, text="No song is played", bg="#424242", fg="white", font=("Arial", 22))
title_song.place(relx=0.50, y=110, anchor=CENTER)

# button part

button_frame.place(anchor=CENTER, relx=0.53, y=440)

play_button = Button(button_frame, image=play_button_image, bg="#424242", activebackground='#424242'
                     , relief='flat',borderwidth=0,command=pause_unpause)
stop_button = Button(button_frame, image=stop_button_image, bg="#424242", activebackground='#424242'
                     , relief='flat',borderwidth=0,command=stop)
repeat_button = Button(button_frame, image=repeat_button_image, bg="#424242", activebackground='#424242'
                       , relief='flat',borderwidth=0,command=loop_song)
back_button = Button(button_frame, image=back_button_image, bg="#424242", activebackground='#424242'
                     , relief='flat',borderwidth=0,command=play_previous_song)
next_button = Button(button_frame, image=next_button_image, bg="#424242", activebackground='#424242'
                     , relief='flat',borderwidth=0,command=play_next_song)
shuffle_button = Button(button_frame, image=shuffle_image, bg="#424242", activebackground='#424242'
                     , relief='flat',borderwidth=0,command=random1)

add_song_button = Button(frame2, text="Add song", bg="#18CC42", fg="white",height=3, width=20,command=add_song)

music_button = Button(frame1, image=music_image, bg="#424242", activebackground='#424242', relief='flat',borderwidth=0)

music_button.place(relx=0.49, rely=0.45, anchor=CENTER)
play_button.grid(row=0, column=2, padx=10)
stop_button.grid(row=0, column=0, padx=10)
repeat_button.grid(row=0, column=4, padx=10)
back_button.grid(row=0, column=1, padx=10)
next_button.grid(row=0, column=3, padx=10)
shuffle_button.grid(row=0, column=5, padx=10)
add_song_button.pack(side=BOTTOM, pady=10)


# advancement scale part
state_label = Label(frame1, text="0.00", bg="#424242", fg="white", font=("Arial", 10))
state_label.place(x=170, y=380)
end_label = Label(frame1, text="1.33", bg="#424242", fg="white", font=("Arial", 10))
end_label.place(x=545, y=380)

scale = ttk.Scale(frame1, from_=0, to=100, orient=HORIZONTAL, length=400)
scale.place(relx=0.50, y=370, anchor=CENTER)


# volume part
volume_label = Label(frame1, text="Volume", bg="#424242", fg="white", font=("Arial", 12))
volume_label.place(x=30, y=480)
w = ttk.Scale(frame1, from_=0, to=1, length=200, orient=HORIZONTAL,command=lambda x: volume(x))
w.set(0.7)
w.place(x=30, y=500)
s = ttk.Style()
s.configure("TScale", background="#424242")
s.configure("Scale", thumbcolor="#18CC42")
w = ttk.Scale(frame1, style="TScale")


innit_playlist("song/")

window.mainloop()