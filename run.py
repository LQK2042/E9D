import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import pygame
import sys
import os

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

gif_path = os.path.join(base_path, "gif.gif")
music_path = os.path.join(base_path, "music.mp3")

pygame.mixer.init()
pygame.mixer.music.load(music_path)
pygame.mixer.music.play(-1)
music_muted = False
volume = 1.0
pygame.mixer.music.set_volume(volume)

root = tk.Tk()
root.overrideredirect(True)
root.wm_attributes('-transparentcolor', 'black')
root.wm_attributes('-topmost', True)
root.geometry("+500+300")

gif = Image.open(gif_path)
frames = [ImageTk.PhotoImage(frame.convert("RGBA")) for frame in ImageSequence.Iterator(gif)]

label = tk.Label(root, bg='black')
label.pack()

frame_delay = 80

def animate(index):
    label.config(image=frames[index])
    index = (index + 1) % len(frames)
    root.after(frame_delay, animate, index)

animate(0)

def move_window(event):
    if event.state & 0x0004:
        root.geometry(f"+{event.x_root}+{event.y_root}")

label.bind("<B1-Motion>", move_window)

def key_event(event):
    global frame_delay, volume

    ctrl_pressed = bool(event.state & 0x0004)

    if event.keysym == "Escape":
        pygame.mixer.music.stop()
        root.destroy()

    elif ctrl_pressed and event.keysym == "Left":
        global frame_delay
        frame_delay = min(300, frame_delay + 10)
        print(f"🐢 Chậm lại: {frame_delay} ms/frame")

    elif ctrl_pressed and event.keysym == "Right":
        frame_delay = max(10, frame_delay - 10)
        print(f"⚡ Nhanh hơn: {frame_delay} ms/frame")

    elif ctrl_pressed and event.keysym == "Up":
        global music_muted
        volume = min(1.0, volume + 0.1)
        pygame.mixer.music.set_volume(volume)
        music_muted = False
        print(f"🔊 Âm lượng: {int(volume*100)}%")

    elif ctrl_pressed and event.keysym == "Down":
        volume = max(0.0, volume - 0.1)
        pygame.mixer.music.set_volume(volume)
        music_muted = volume == 0
        print(f"🔉 Âm lượng: {int(volume*100)}%")

root.bind("<Key>", key_event)

def ctrl_right_click(event):
    if event.state & 0x0004: 
        global music_muted
        if not music_muted:
            pygame.mixer.music.set_volume(0)
            music_muted = True
            print("🔇 Nhạc tắt")
        else:
            pygame.mixer.music.set_volume(volume)
            music_muted = False
            print("🔊 Nhạc bật")

label.bind("<Button-3>", ctrl_right_click) 

root.mainloop()
