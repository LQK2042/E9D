import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import pygame, sys, os

# --- Xác định đường dẫn đúng dù chạy từ Python hay EXE ---
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS   # thư mục tạm PyInstaller tạo ra khi chạy EXE
else:
    base_path = os.path.dirname(__file__)

gif_path = os.path.join(base_path, "gif.gif")
music_path = os.path.join(base_path, "music.mp3")

# --- Khởi tạo pygame mixer ---
pygame.mixer.init()
pygame.mixer.music.load(music_path)   # dùng đường dẫn đúng
pygame.mixer.music.play(-1)           # -1 = lặp vô hạn

# --- Cửa sổ hiển thị GIF ---
root = tk.Tk()
root.overrideredirect(True)
root.wm_attributes('-transparentcolor', 'black')
root.wm_attributes('-topmost', True)
root.geometry("+500+300")

# --- Nạp ảnh GIF ---
gif = Image.open(gif_path)
frames = [ImageTk.PhotoImage(frame.convert("RGBA")) for frame in ImageSequence.Iterator(gif)]

label = tk.Label(root, bg='black')
label.pack()

frame_delay = 100

# --- Hiển thị từng frame ---
def animate(index):
    label.config(image=frames[index])
    index = (index + 1) % len(frames)
    root.after(frame_delay, animate, index)

animate(0)

# --- Cho phép di chuyển CHỈ khi giữ Ctrl ---
def move_window(event):
    if event.state & 0x0004:
        root.geometry(f"+{event.x_root}+{event.y_root}")

label.bind("<B1-Motion>", move_window)

# --- Phím ESC để tắt toàn bộ ---
def stop_all(event):
    if event.keysym == "Escape":
        pygame.mixer.music.stop()
        root.destroy()

root.bind("<Key>", stop_all)

root.mainloop()
