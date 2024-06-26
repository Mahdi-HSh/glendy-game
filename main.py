#!/usr/bin/env python3
from customtkinter import *
from CTkMenuBar import CTkMenuBar
from tkinter import PhotoImage, messagebox, ttk
from os import getlogin
from platform import system
import gui
import netGUI

root = CTk()
icon = PhotoImage(file = 'glenda.png')
root.wm_iconbitmap()
root.iconphoto(True, icon)

if system() == 'Windows':
    import ctypes
    scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
    win_width = 500
    win_height = 500
    scaled_width = root.winfo_screenwidth()
    scaled_height = root.winfo_screenheight()
    x = int(((scaled_width / 2) - (win_width / 2)) * (scale_factor/100))
    y = int(((scaled_height / 2) - (win_height / 1.8)) * (scale_factor/100))
    real_width = ctypes.windll.user32.GetSystemMetrics(0)
    btn_corner_radius = 32

elif system() == 'Linux':
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    win_width = int(screen_width/4)
    win_height = int(screen_width/4)
    x = int((screen_width / 2) - (win_width / 2))
    y = int((screen_height / 2) - (win_height / 1.8))
    real_width = screen_width
    btn_corner_radius = 0

else:
    win_width = 500
    win_height = 500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int((screen_width / 2) - (win_width / 2))
    y = int((screen_height / 2) - (win_height / 1.8))
    real_width = screen_width
    btn_corner_radius = 32

font = ""
font_size = 25

root.geometry(f'{win_width}x{win_height}+{x}+{y}')
root.title('Glendy')
root.resizable(False, False)
set_appearance_mode('System')

def change_theme():
    if get_appearance_mode() == 'Dark':
        set_appearance_mode('Light')
    elif get_appearance_mode() == 'Light':
        set_appearance_mode('Dark')

def get_scale(bsize):
    match bsize:
        case 'Tiny':
            scale = int((real_width/125)/2)-5
        case 'Small':
            scale = int((real_width/125)/2)-3
        case 'Normal':
            scale = int((real_width/125)/2)-1
        case 'Large':
            scale = int((real_width/125)/2)+1
    return scale

def offline_game(window, difficulty, bsize):
    pygame_scale = get_scale(bsize)
    window.destroy()
    root.withdraw()
    game = gui.Glendy(difficulty, pygame_scale, get_appearance_mode())
    game.start()
    root.deiconify()

def online_game(window, name, player, server, bsize, mode):
    if name != '' and len(name) <= 32:
        pygame_scale = get_scale(bsize)
        window.destroy()
        root.withdraw()
        game = netGUI.netGlendy(name, player, server, pygame_scale, mode, get_appearance_mode())
        game.start()
        root.deiconify()
    else:
        if system() == 'Linux':
            window.withdraw()
            messagebox.showwarning(master=window, title='Warning', message='Please enter a valid name.')
            window.deiconify()
        else:
            messagebox.showwarning(master=window, title='Warning', message='Please enter a valid name.')
    
def offline_window():    
    newWin = CTkToplevel(root)
    newWin.after(201, lambda: newWin.iconphoto(False, icon))
    if system() == 'Windows':
        newWin.grab_set()
    newWin.title("Offline mode")
    newWin.geometry(f'{win_width}x{win_height}+{x}+{y}')
    newWin.resizable(False, False)
    lbl = CTkLabel(master=newWin, text="Select difficulty:", font=(font, font_size))
    lbl.place(relx=0.5, rely=0.2, anchor="center")
    lbl2 = CTkLabel(master=newWin, text="Select board size (visually):", font=(font, font_size))
    lbl2.place(relx=0.5, rely=0.4, anchor="center")
    if system() == 'Linux':
        combo_difficulty = ttk.Combobox(master=newWin, values=['Easy', 'Medium', 'Hard', 'Impossible'], state='readonly', font=(font, font_size-5))
        combo_bsize = ttk.Combobox(master=newWin, values=['Tiny', 'Small', 'Normal', 'Large'], state='readonly', font=(font, font_size-5))
    else:
        combo_difficulty = CTkComboBox(master=newWin, values=['Easy', 'Medium', 'Hard', 'Impossible'], state='readonly', font=(font, font_size-5), dropdown_font=(font, font_size-10))
        combo_bsize = CTkComboBox(master=newWin, values=['Tiny', 'Small', 'Normal', 'Large'], state='readonly', font=(font, font_size-5), dropdown_font=(font, font_size-10))
    combo_difficulty.set('Easy')
    combo_bsize.set('Normal')
    combo_difficulty.place(relx=0.5, rely=0.3, anchor='center')
    combo_bsize.place(relx=0.5, rely=0.5, anchor='center')
    btn = CTkButton(master=newWin, text='Start the game!', command=lambda:offline_game(newWin, combo_difficulty.get(), combo_bsize.get()), corner_radius=btn_corner_radius, border_width=2, font=(font, font_size))
    btn.place(relx=0.5, rely=0.75, anchor="center")

def online_window():    
    newWin = CTkToplevel(root)
    newWin.after(201, lambda: newWin.iconphoto(False, icon))
    if system() == 'Windows':
        newWin.grab_set()
    newWin.title("Online mode")
    newWin.geometry(f'{win_width}x{win_height}+{x}+{y}')
    newWin.resizable(False, False)
    lbl1 = CTkLabel(master=newWin, text="Enter your name:", font=(font, font_size))
    lbl1.place(relx=0.5, rely=0.08, anchor="center")
    lbl2 = CTkLabel(master=newWin, text="Select player:", font=(font, font_size))
    lbl2.place(relx=0.5, rely=0.26, anchor="center")
    lbl3 = CTkLabel(master=newWin, text="Select or enter server address:", font=(font, font_size))
    lbl3.place(relx=0.5, rely=0.44, anchor="center")
    lbl4 = CTkLabel(master=newWin, text="Select board size (visually):", font=(font, font_size))
    lbl4.place(relx=0.5, rely=0.62, anchor="center")
    txt_name = CTkTextbox(master=newWin, width=250, height=30, font=(font, font_size-5))
    txt_name.insert('end', getlogin())
    txt_name.place(relx=0.5, rely=0.16, anchor="center")
    if system() == 'Linux':
        combo_player = ttk.Combobox(master=newWin, values=['Trapper', 'Glenda', 'Random'], state='readonly', font=(font, font_size-5))
        combo_server = ttk.Combobox(master=newWin, values=['unix.cloud9p.org:1769'], font=(font, font_size-5))
        combo_bsize = ttk.Combobox(master=newWin, values=['Tiny', 'Small', 'Normal', 'Large'], state='readonly', font=(font, font_size-5))

    else:
        combo_player = CTkComboBox(master=newWin, values=['Trapper', 'Glenda', 'Random'], state='readonly', font=(font, font_size-5), dropdown_font=(font, font_size-10))
        combo_server = CTkComboBox(master=newWin, width=250, values=['unix.cloud9p.org:1769'], font=(font, font_size-5), dropdown_font=(font, font_size-10))
        combo_bsize = CTkComboBox(master=newWin, values=['Tiny', 'Small', 'Normal', 'Large'], state='readonly', font=(font, font_size-5), dropdown_font=(font, font_size-10))
    combo_player.set('Random')
    combo_server.set('unix.cloud9p.org:1769')
    combo_bsize.set('Normal')
    combo_player.place(relx=0.5, rely=0.34, anchor='center')
    combo_server.place(relx=0.5, rely=0.52, anchor='center')
    combo_bsize.place(relx=0.5, rely=0.7, anchor='center')
    radio_var = StringVar(value='')
    radio_mode1 = CTkRadioButton(master=newWin, text='Online multiplayer', value='Multiplayer', variable=radio_var, corner_radius=0, font=(font, font_size-5))
    radio_mode2 = CTkRadioButton(master=newWin, text='Online singleplayer', value='Singleplayer', variable=radio_var, corner_radius=0, font=(font, font_size-5))
    radio_mode1.select()
    radio_mode1.place(relx=0.25, rely=0.8, anchor='center')
    radio_mode2.place(relx=0.75, rely=0.8, anchor='center')
    btn = CTkButton(master=newWin, text='Start the game!', command=lambda:online_game(newWin, txt_name.get('1.0', 'end-1c'), combo_player.get(), combo_server.get(), combo_bsize.get(), radio_var.get()), corner_radius=btn_corner_radius, border_width=2, font=(font, font_size))
    btn.place(relx=0.5, rely=0.9, anchor="center")

def show_help():
    messagebox.showinfo(master=root, title="Help", message=
    '''Glendy is a simple game.
One player plays as Trapper, and the other as Glenda.
Glenda tries to escape by reaching sides,
and Trapper tries to trap Glenda in walls.
To put a wall as Trapper, click on any free circle
on the board each turn.
To escape as Glenda, you can choose from
6 neighboring circles around Glenda each turn.
In offline mode,
for now, you can only play as Trapper.
You can choose difficulty and board size.
Board size have no effect on game logic,
and makes game board larger or smaller visually.
In online mode,
you should enter a name, you can choose
the side you prefer and board size.
You can also enter or choose server address.
There are two modes too,
Online multiplayer and Online single player.''')

menu = CTkMenuBar(master=root)
menu.add_cascade('Light/Dark mode', change_theme)
menu.add_cascade('Help', show_help)

lbl = CTkLabel(master=root, text='Glendy', font=(font, font_size+30))
lbl.place(relx=0.5, rely=0.25, anchor="center")

btn = CTkButton(master=root, text='Offline game', command=offline_window, corner_radius=btn_corner_radius, border_width=2, font=(font, font_size))
btn.place(relx=0.5, rely=0.55, anchor="center")

btn = CTkButton(master=root, text='Online game', command=online_window, corner_radius=btn_corner_radius, border_width=2, font=(font, font_size))
btn.place(relx=0.5, rely=0.75, anchor="center")

root.mainloop()
