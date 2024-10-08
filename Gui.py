# -*- coding: gbk -*-
import os
from time import sleep
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
from tkinter.tix import PopupMenu
from turtle import bgcolor, left
import pygame
import threading 
import Bilibili as Bi
import sys
from tkinter import *

class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)



def find_music_files(directory):  
    # 定义常见的音乐文件扩展名  
    music_extensions = ['.mp3', '.wav', '.flac', '.ogg', '.aac', '.m4a']  
      
    # 存储找到的音乐文件路径  
    music_files = []  
      
    # 遍历指定目录下的所有文件  
    for filename in os.listdir(directory):  
        # 获取文件的完整路径  
        filepath = os.path.join(directory, filename)  
        #print(filepath)  
        # 检查文件是否是普通文件（不是目录）  
        if os.path.isfile(filepath):  
            # 获取文件的扩展名  
            _, file_extension = os.path.splitext(filename)  
              
            # 检查文件扩展名是否在音乐文件扩展名列表中  
            if file_extension.lower() in music_extensions:  
                music_files.append(filepath)  
      
    return music_files  


class Music:
    def __init__(self, bv="", path="", name="", singer=""):
        self.bv = bv 
        self.path  = path 
        self.name = name 
        self.singer = singer

class MusicList:
    def __init__(self, name=""):
        self.name = name
        self.list = [] 

    def append(self, music):
        self.list.append(music)





window = tk.Tk()
window.title('BMusic')
window.geometry("600x500+100+50")

download_thread_list = []
def shutDown():
    if download_thread_list:
        print(f"nnum={len(threading.enumerate())}")
        if tk.messagebox.askokcancel("有下载任务进行中", "确定要退出吗？"):
            window.destroy()
    #销毁root窗   
    else: window.destroy()
    

window.protocol("WM_DELETE_WINDOW", shutDown)

playing_frame =  tk.Frame(window,bg='red')
list_frame = tk.Frame(window,bg='yellow')
search_frame = tk.Frame(window,bg='blue')
favor_frame = tk.Frame(window,bg='red')
up_frame= tk.Frame(window,bg='yellow') 
download_frame = tk.Frame(window, bg='blue')

#下载列表界面
download_label =  tk.Label(download_frame, text='下载中数量：', font=('Arial', 12),  height=1,)
download_scrollbar = tk.Scrollbar(download_frame) #滚动条
download_listbox = tk.Listbox(download_frame, yscrollcommand=download_scrollbar.set)

download_label.pack(side='top', fill='x', expand=0)
download_listbox.pack(side='left', fill='both', expand=1)
download_scrollbar.pack(side='right', fill='y')
download_scrollbar.config(command=download_listbox.yview)

download_list = [] #存储下载连接
download_title = []

download_list_lock = False
def downloadThread():
    global download_list_lock
    while True:
        if len(download_thread_list) <  6 and download_list and not download_list_lock:
            download_list_lock = True
            thread1 = threading.Thread(target=Bi.getMp3, args=(download_list[0],))  
            download_thread_list.append(thread1)
            download_thread_list[-1].start()
            download_list.pop(0)
            download_title.pop(0)
            download_listbox.delete(0)
            download_list_lock = False
            print(f"xianchengshu:{len(threading.enumerate())}")

        download_listbox.selection_clear(0, 'end') 
               
        for i in range(len(download_thread_list) - 1, -1, -1):
            if not download_thread_list[i].is_alive():
                download_thread_list.pop(i)
                download_label.config(text=f"下载中数量：{len(download_thread_list)}") 

def showDownloadList():
    global download_list_lock
    while True:
        if not download_list_lock:
            download_list_lock = True
            download_listbox.delete(0, 'end')
            for i in download_title:
                download_listbox.insert('end', i)
            download_list_lock = False
            return

download_thread = threading.Thread(target=downloadThread)  
download_thread.start()

def changePlayingFrame():
    list_frame.forget()
    search_frame.forget()
    favor_frame.forget()
    up_frame.forget()
    download_frame.forget()
    playing_frame.pack(fill='both', expand=1, side='left')

def changeListFrame():
    search_frame.forget()
    playing_frame.forget()
    favor_frame.forget()
    up_frame.forget()
    download_frame.forget()
    list_frame.pack(fill='both', expand=1, side='left')

def changeSearchFrame():
    playing_frame.forget()
    list_frame.forget()
    favor_frame.forget()
    up_frame.forget()
    download_frame.forget()
    search_frame.pack(fill='both', expand=1, side='left')

def changeFavorFrame():
    playing_frame.forget()
    list_frame.forget()
    search_frame.forget()
    up_frame.forget()
    download_frame.forget()
    favor_frame.pack(fill='both', expand=1, side='left')

def changeUpFrame():
    playing_frame.forget()
    list_frame.forget()
    favor_frame.forget()
    search_frame.forget()
    download_frame.forget()
    up_frame.pack(fill='both', expand=1, side='left')

def changeDownloadFrame():
    playing_frame.forget()
    list_frame.forget()
    favor_frame.forget()
    search_frame.forget()
    up_frame.forget()
    download_frame.pack(fill='both', expand=1, side='left')


is_lock = False 
def changePlayingMode():
    global is_lock
    if pygame.mixer.music.get_busy():       
        is_lock = True
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()
        is_lock = False

def clearPlayingList():
    playing_list.clear()
    playing_listbox.delete(0, 'end')

def setSavePath():
    path = filedialog.askdirectory(title='请选择文件夹')
    if not path:
        return
    else:
        Bi.save_path =  path


#左侧页签部分
section_frame = tk.Frame(window)
tk.Button(section_frame, text='播放列表', font=('Arial', 12), width=10, height=1, command=changePlayingFrame).pack(side="top")
tk.Button(section_frame, text='清空播放列表', font=('Arial', 12), width=10, height=1, command=clearPlayingList).pack(side="top")
tk.Button(section_frame, text='暂停/继续', font=('Arial', 12), width=10, height=1, command=changePlayingMode).pack(side="top")
tk.Label(section_frame, text=" ").pack(padx=10, fill='x')
tk.Button(section_frame, text='本地歌单', font=('Arial', 12), width=10, height=1, command=changeListFrame).pack(side="top")  
tk.Label(section_frame, text=" ").pack(padx=10, fill='x')
tk.Button(section_frame, text='搜索下载', font=('Arial', 12), width=10, height=1, command=changeSearchFrame).pack(side="top")
tk.Button(section_frame, text='收藏下载', font=('Arial', 12), width=10, height=1, command=changeFavorFrame).pack(side="top")
#tk.Button(section_frame, text='主页下载', font=('Arial', 12), width=10, height=1, command=changeUpFrame).pack(side="top")
tk.Button(section_frame, text='下载列表', font=('Arial', 12), width=10, height=1, command=changeDownloadFrame).pack(side="top")
section_path_button = tk.Button(section_frame, text='下载地址', font=('Arial', 12), width=10, height=1, command=setSavePath)
section_path_button.pack(side="top")
CreateToolTip(section_path_button, "设置音乐的下载地址")
section_frame.pack(ipadx=0, ipady=10, side = 'left', fill='y', expand=0)

#播放界面
playing_list =  [] #播放列表
playing_index = -1
pygame.mixer.init()
next_music = "" #下一首歌的地址
def playMusic():
    global next_music
    global playing_index
    global is_lock
    while True:
        if is_lock:continue
        if not pygame.mixer.music.get_busy():
            if not playing_list: 
                playing_index = -1
                continue
            playing_index = (playing_index + 1) % len(playing_list)
            next_music = playing_list[playing_index]
            #playing_listbox.selection_set(playing_index) 
            print(f"palying {next_music}")
            pygame.mixer.music.load(next_music)
            pygame.mixer.music.play(loops=1)
        
            
            #showPlaying()
            
thread1 = threading.Thread(target=playMusic) 
thread1.start()

playing_scrollbar = tk.Scrollbar(playing_frame) #滚动条
playing_listbox = tk.Listbox(playing_frame, yscrollcommand=playing_scrollbar.set)

#歌单界面list_frame
##变量
MusicLists = [] #歌单列表

##ui
list_menu_frame = tk.Frame(list_frame) #菜单栏
list_content_frame = tk.Frame(list_frame) #内容栏
list_scrollbar = tk.Scrollbar(list_content_frame) #滚动条
list_listbox = tk.Listbox(list_content_frame, yscrollcommand=list_scrollbar.set)

playing_listbox.pack(side='left', fill='both', expand=1)
playing_scrollbar.pack(side='right', fill='y')
playing_scrollbar.config(command=playing_listbox.yview)


def popupmenu(event, menu):
        menu.post(event.x_root, event.y_root)

music_list_index = -1

def playingListDelete():
    print("delete")
    selected_indices = playing_listbox.curselection() 
    if not selected_indices:
        return
    selected_index = selected_indices[0]

    playing_list.pop(selected_index)
    playing_listbox.delete(selected_index)
    #showPlaying()

def playingPlay():
    global is_lock
    global playing_index
    is_lock = True
    print("!!!!!!!")
    selected_indices = playing_listbox.curselection() 
    if not selected_indices:
        return
    #if pygame.mixer.music.get_busy():
        #pygame.mixer.music.stop()
    selected_index = selected_indices[0]
    playing_index = selected_index
    next_music = playing_list[selected_index]
    pygame.mixer.music.load(next_music)
    print(next_music)
    pygame.mixer.music.play(loops=1)
    is_lock = False

def showPlaying():
    playing_listbox.delete(0, 'end')  

    for pl in playing_list:
        file_name_with_ext = os.path.basename(pl)  
        file_name, file_ext = os.path.splitext(file_name_with_ext)
        playing_listbox.insert('end', file_name)

    menu = tk.Menu(list_listbox, tearoff=0)
    menu.add_command(label="播放", command=playingPlay)
    menu.add_command(label="从列表中删除", command=playingListDelete)
    playing_listbox.bind('<Button-3>', lambda event: popupmenu(event, menu))
    #list_listbox.bind('<Double-1>', showList)


def musicDelete():
    selected_indices = list_listbox.curselection() 
    if not selected_indices:
        return
    selected_index = selected_indices[0]

    MusicLists[music_list_index].list.pop(selected_index)
    list_listbox.delete(selected_index)
    #showList(music_list_index)
    
def musicAdd():
    selected_indices = list_listbox.curselection()
    if not selected_indices:
        return
    selected_index = selected_indices[0]

    playing_list.append(MusicLists[music_list_index].list[selected_index].path)
    global next_music
    if next_music == "":
        next_music = playing_list[0]
    showPlaying()

def showList(index=-1): #显示歌单内容
    selected_indices = list_listbox.curselection() 
    if not selected_indices:
        return
    if index == -1:
        selected_index = selected_indices[0]
    else:
        selected_index = index

    global music_list_index
    music_list_index = selected_index

    list_listbox.delete(0, 'end')
    for m in MusicLists[selected_index].list:
        list_listbox.insert('end', m.name)

    menu = tk.Menu(list_listbox, tearoff=0)
    menu.add_command(label="添加到播放列表", command=musicAdd)
    menu.add_command(label="从歌单中删除", command=musicDelete)
    list_listbox.bind('<Button-3>', lambda event: popupmenu(event, menu))
    list_listbox.bind('<Double-1>', showList)



def musicListRename():
    selected_indices = list_listbox.curselection() 
    if not selected_indices:
        return
    selected_index = selected_indices[0]

    user_input = simpledialog.askstring("输入", "请输入内容:")  
    if not user_input:
        return
    else:
        MusicLists[selected_index].name = user_input
        showMusicList()

def musicListDelete():
    selected_indices = list_listbox.curselection() 
    if not selected_indices:
        return
    selected_index = selected_indices[0]

    MusicLists.pop(selected_index)
    showMusicList()

def musicListAdd():
    selected_indices = list_listbox.curselection() 
    if not selected_indices:
        return
    selected_index = selected_indices[0]

    for m in MusicLists[selected_index].list:
        playing_list.append(m.path)

    showPlaying()


def showMusicList():
    list_listbox.delete(0, 'end')  

    for ml in MusicLists:
        list_listbox.insert('end', ml.name)

    menu = tk.Menu(list_listbox, tearoff=0)
    menu.add_command(label="添加到播放列表", command=musicListAdd)
    menu.add_command(label="打开", command=showList)
    menu.add_command(label="重命名", command=musicListRename)
    menu.add_command(label="从列表中删除", command=musicListDelete)
    list_listbox.bind('<Button-3>', lambda event: popupmenu(event, menu))
    list_listbox.bind('<Double-1>', showList)
    

    

def getLocalList():  
    path = filedialog.askdirectory(title='请选择文件夹')
    if not path:
        return
    files = find_music_files(path)
    if not files:
        tk.messagebox.showerror(title='Error', message='未找到音乐文件') 
        return
    

    new_list = MusicList(name="新建歌单")
    for f in files:
        new_music = Music(path=f)
        file_name_with_ext = os.path.basename(f)  
        file_name, file_ext = os.path.splitext(file_name_with_ext) 
        new_music.name = file_name
        new_list.append(new_music)
    MusicLists.append(new_list) 
    showMusicList()




tk.Button(list_menu_frame, text='从本地建立歌单', font=('Arial', 12), width=16, height=1, command=getLocalList).pack(side="left")
tk.Button(list_menu_frame, text='返回歌单列表', font=('Arial', 12), width=16, height=1, command=showMusicList).pack(side="left")
list_menu_frame.pack(side='top', fill='x', expand=0)
list_listbox.pack(side='left', fill='both', expand=1)
list_scrollbar.pack(side='right', fill='y')
list_scrollbar.config(command=list_listbox.yview)

list_content_frame.pack(side='top', fill='both', expand=1)



#搜索界面
search_menu_frame = tk.Frame(search_frame) ##菜单栏
search_content_frame = tk.Frame(search_frame) ##内容栏
search_scrollbar = tk.Scrollbar(search_content_frame) #滚动条
search_listbox = tk.Listbox(search_content_frame, yscrollcommand=search_scrollbar.set)
search_entry = tk.Entry(search_menu_frame, text='', font=('Arial', 12), width=32)

result = []

def searchDownload():
    selected_indices = search_listbox.curselection() 
    if not selected_indices:
        return
    selected_index = selected_indices[0]

    thread1 = threading.Thread(target=Bi.getMp3, args=('https:' + result[selected_index][1],))
    #thread1 = threading.Thread(Bi.getMp3,  ('https:' + result[selected_index][1])) 
    thread1.start()
    


def searchSearch():
    keyword = search_entry.get()
    if not keyword:
        return
    global result
    result = Bi.search(keyword)
    search_listbox.delete(0, 'end') 
    for r in result:
        search_listbox.insert('end', r[0])
    
    menu = tk.Menu(search_listbox, tearoff=0)
    menu.add_command(label="下载", command=searchDownload)
    search_listbox.bind('<Button-3>', lambda event: popupmenu(event, menu))

search_search_button = tk.Button(search_menu_frame, text='搜索', font=('Arial', 12), width=6, height=1, command=searchSearch)
search_search_button.pack(side="left")
CreateToolTip(search_search_button, "输入关键词以搜索")
search_entry.pack(side="left", fill='x', expand=1)
search_listbox.pack(side='left', fill='both', expand=1)
search_scrollbar.pack(side='right', fill='y')
search_scrollbar.config(command=search_listbox.yview)

search_menu_frame.pack(side='top', fill='x', expand=0)
search_content_frame.pack(side='top', fill='both', expand=1)


#收藏下载界面
favor_menu_frame = tk.Frame(favor_frame) ##菜单栏
favor_content_frame = tk.Frame(favor_frame) ##内容栏
favor_scrollbar = tk.Scrollbar(favor_content_frame) #滚动条
favor_listbox = tk.Listbox(favor_content_frame, yscrollcommand=favor_scrollbar.set, selectmode='multiple')
favor_entry = tk.Entry(favor_menu_frame, text='', font=('Arial', 12), width=32)
favor_entry.insert('end', '2421072918')
favor_download_list = []

def favorDownloadAll():   
    for i in range(0, len(result)):
        download_list.append('https://www.bilibili.com/video/' + result[i][1])
        download_title.append(result[i][0])
    thread1 = threading.Thread(target=showDownloadList)
    thread1.start()
 

def favorDownload():
    selected_indices = favor_listbox.curselection() 
    if not selected_indices:
        return
    #selected_index = selected_indices[0]
    for i in selected_indices:
        download_list.append('https://www.bilibili.com/video/' + result[i][1])
        download_title.append(result[i][0])
    thread1 = threading.Thread(target=showDownloadList)
    thread1.start()


def favorGet():
    keyword = favor_entry.get()
    print(f"keyword={keyword}")
    if not keyword:
        return
    global result
    result = Bi.analyse_favorlist(keyword)
    favor_listbox.delete(0, 'end') 
    for r in result:
        favor_listbox.insert('end', r[0])
        print(r[0])
    
    menu = tk.Menu(favor_listbox, tearoff=0)
    menu.add_command(label="下载", command=favorDownload)
    favor_listbox.bind('<Button-3>', lambda event: popupmenu(event, menu))


favor_all_button = tk.Button(favor_menu_frame, text='全部下载', font=('Arial', 12), width=6, height=1, command=favorDownloadAll)
favor_all_button.pack(side="left")
favor_get_button = tk.Button(favor_menu_frame, text='获取', font=('Arial', 12), width=6, height=1, command=favorGet)
favor_get_button.pack(side="left")
CreateToolTip(favor_get_button, '输入收藏夹编号以获取')
favor_entry.pack(side="left", fill='x', expand=1)
favor_listbox.pack(side='left', fill='both', expand=1)
favor_scrollbar.pack(side='right', fill='y')
favor_scrollbar.config(command=favor_listbox.yview)

favor_menu_frame.pack(side='top', fill='x', expand=0)
favor_content_frame.pack(side='top', fill='both', expand=1)







window.mainloop()
