from tkinter import *
from tkinter import filedialog
from tkinter import ttk 
from tkinter import messagebox   
import os
os.environ['TKDND_LIBRARY'] = "pytkdnd2.8-win32-x86_64\pytkdnd2.8"
from untested_tkdnd_wrapper import TkDND 
from PIL import Image    
from pydub import AudioSegment     
from threading import Thread
from PIL import ImageTk

base_color="#fafafa"
ipfileAddr=ipextension=opDir=opextension=file_name=fileType=None


def resetUI():
    global ipfileAddr,opDir
    ipfileAddr=opDir=None
    inputBox.delete(0, 'end')
    outputBox.delete(0, 'end')
    # resize_img(None)

def update_status():
    print("Converted Successfully")
    status.config(text="Converted Successfully")
    resetUI()

def openFile():
    global ipfileAddr,ipextension
    inputBox.delete(0, 'end')
    outputBox.delete(0, 'end')
    ipfileAddr=(filedialog.askopenfile(parent=root,mode='rb',title='Choose a file',filetype=[("All files","*.*")])).name
    inputBox.insert(END,ipfileAddr)
    ipextension=getExtension(ipfileAddr)
    print(f'Input File: "{ipfileAddr}"\nExt: {ipextension}')
    if ipfileAddr:
        status.config(text="Now select output directory")

def getExtension(loc):
    global file_name
    file_name, file_extension = os.path.splitext(loc)
    file_extension=file_extension[1:]
    # print(file_name)
    # print(file_extension)
    return file_extension

def outpFile():
    global ipextension,opDir,opextension,file_name,ipfileAddr,fileType
    #image
    if ipextension=="png":
        fileOptions = [("jpeg files","*.jpg"),("webp files","*.webp"),("ico files","*.ico"),("tiff files","*.tiff"),('All Files', '*.*')]
        fileType="image"
    elif ipextension=="jpg":
        fileOptions = [("png files","*.png"),("webp files","*.webp"),("tiff files","*.tiff"),('All Files', '*.*')]
        fileType="image"
    elif ipextension=="webp":
        fileOptions = [("png files","*.png"),("jpeg files","*.jpg"),("ico files","*.ico"),("tiff files","*.tiff"),('All Files', '*.*')]
        fileType="image"
    elif ipextension=="tiff":
        fileOptions = [("png files","*.png"),("jpeg files","*.jpg"),("ico files","*.ico"),("webp files","*.webp"),('All Files', '*.*')]
        fileType="image"

    #audio
    elif ipextension=="mp3":
        fileOptions = [("wav files","*.wav"),("flac files","*.flac"),("ogg files","*.ogg"),('All Files', '*.*')]
        fileType="audio"
    elif ipextension=="wav":
        fileOptions = [("mp3 files","*.mp3"),("flac files","*.flac"),("ogg files","*.ogg"),('All Files', '*.*')]
        fileType="audio"
    elif ipextension=="flac":
        fileOptions = [("mp3 files","*.mp3"),("wav files","*.wav"),("ogg files","*.ogg"),('All Files', '*.*')]
        fileType="audio"
    elif ipextension=="ogg":
        fileOptions = [("mp3 files","*.mp3"),("wav files","*.wav"),("flac files","*.flac"),('All Files', '*.*')]
        fileType="audio"

    #video
    elif ipextension=="mp4":
        fileOptions = [("avi files","*.avi"),("flv files","*.flv"),("mov files","*.mov"),("mp3 files","*.mp3"),("mkv files","*.mkv"),("webm files","*.webm"),('All Files', '*.*')]
        fileType="video"    
    elif ipextension=="avi":
        fileOptions = [("mp4 files","*.mp4"),("flv files","*.flv"),("mov files","*.mov"),("mkv files","*.mkv"),("webm files","*.webm"),('All Files', '*.*')]
        fileType="video" 
    elif ipextension=="flv":
        fileOptions = [("mp4 files","*.mp4"),("avi files","*.avi"),("mov files","*.mov"),("mkv files","*.mkv"),("webm files","*.webm"),('All Files', '*.*')]
        fileType="video" 
    elif ipextension=="mov":
        fileOptions = [("mp4 files","*.mp4"),("avi files","*.avi"),("flv files","*.flv"),("mkv files","*.mkv"),("webm files","*.webm"),('All Files', '*.*')]
        fileType="video" 
    elif ipextension=="mkv":
        fileOptions = [("mp4 files","*.mp4"),("avi files","*.avi"),("flv files","*.flv"),("mov files","*.mov"),("webm files","*.webm"),('All Files', '*.*')]
        fileType="video" 
    elif ipextension=="webm":
        fileOptions = [("mp4 files","*.mp4"),("avi files","*.avi"),("flv files","*.flv"),("mov files","*.mov"),("mkv files","*.mkv"),('All Files', '*.*')]
        fileType="video" 

    else:
        messagebox.showerror(title="Error",message="Conversion not possible.\nFile type not supported.")
        resetUI()
        return
    outputBox.delete(0, 'end')
    
    # print(file_name)
    file_name=file_name[::-1]
    file_name = file_name[file_name.find("/"):]
    file_name=file_name[::-1]
    # print(file_name)
    
    base=os.path.basename(ipfileAddr)
    base_name=os.path.splitext(base)[0]
    opDir=(filedialog.asksaveasfilename(parent=root,title='Convert as',filetypes=fileOptions,defaultextension = fileOptions,initialdir=file_name,initialfile=base_name))
    outputBox.insert(END,opDir)
    opextension=getExtension(opDir)
    print(f'Output File: "{opDir}"\nExt: {opextension}')
    if opDir:
        status.config(text="Press convert")

def startConvert():
    global ipfileAddr,ipextension,opDir,opextension,fileType
    if ipfileAddr:
        if opDir:
            print(f"\nConverting from {ipextension} to {opextension}")
            if fileType=="image":
                Thread(target=convertImage).start()
            elif fileType=="audio":
                Thread(target=convertAudio).start()
            elif fileType=="video":
                Thread(target=convertVideo).start()
        else:
            status.config(text="Please select output directory")
            return
    else:
        status.config(text="Please select input file")
        return

def convertAudio():
    global ipfileAddr,ipextension,opDir,opextension
    status.config(text="Converting...")
    audio=AudioSegment.from_file(ipfileAddr,format=ipextension)
    audio.export(opDir,format=opextension)
    update_status()
    return

def convertImage():
    global ipfileAddr,ipextension,opDir,opextension
    status.config(text="Converting...")
    if opextension=="jpg":
        fill_color = '#ffffff'  
        image = Image.open(ipfileAddr)
        if image.mode in ('RGBA', 'LA'):
            background = Image.new(image.mode[:-1], image.size, fill_color)
            background.paste(image, image.split()[-1])
            image = background
        image.save(opDir, "JPEG", quality=95)

    elif opextension=="ico":
        img = Image.open(ipfileAddr)
        new_img=img.resize((256, 256))
        icon_sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (72, 72),(80, 80),(96, 96),(128, 128), (256, 256)]
        new_img.save(opDir, sizes=icon_sizes)
    else:
        image = Image.open(ipfileAddr)
        image.save(opDir)
    update_status()
    return

def convertVideo():
    global ipfileAddr,ipextension,opDir,opextension
    status.config(text="Converting...")
    os.system(f'cmd /c "ffmpeg -i "{ipfileAddr}" "{opDir}"')
    update_status()
    return

def handle_dnd(event):
    global ipfileAddr,ipextension
    status.config(text=" ")
    inputBox.delete(0, 'end')
    outputBox.delete(0, 'end')
    inputBox.insert(0, (event.data).replace('{',"").replace('}',""))
    ipfileAddr=inputBox.get()
    ipextension=getExtension(inputBox.get())
    print(f'Input File: "{ipfileAddr}"\nExt: {ipextension}')
    if ipfileAddr:
        status.config(text="Now select output directory")


root = Tk() 
root.title("Convertor Utility (Made by Sourabh Sathe)") 
root.minsize(450,420)
# root.resizable(False,False)
root.config(bg=base_color)

top_frame=Frame(root,bg=base_color)
top_frame.pack(side=TOP,fill=X,padx=10,pady=10)

inputLabel=Label(top_frame,text="Input File",bg=base_color)
inputLabel.pack(side=LEFT)

inputBox = ttk.Entry(top_frame)
# root.update()
inputBox.pack(side=LEFT,fill=X,expand=True,padx=5,ipady=1)
inputBox.focus_set()

browseButton1=ttk.Button(top_frame,text="Browse",command=openFile)
browseButton1.pack(side=LEFT)


dndframe = Canvas(root, highlightthickness=1, relief='solid',highlightbackground="#c5c5c5")
dndframe.pack(fill=BOTH,expand=True,padx=10)

dnd = TkDND(root)
dnd.bindtarget(dndframe, handle_dnd, 'text/uri-list') 


bottom_frame=Frame(root,bg=base_color)
bottom_frame.pack(fill=X,padx=10,pady=10)

outputLabel=Label(bottom_frame,text="Output File",bg=base_color)
outputLabel.pack(side=LEFT)

outputBox = ttk.Entry(bottom_frame)
# root.update()
outputBox.pack(side=LEFT,fill=X,expand=True,padx=5,ipady=1)

browseButton2=ttk.Button(bottom_frame,text="Browse",command=outpFile)
browseButton2.pack(side=LEFT)


convertButton=ttk.Button(root,text="Convert",command=startConvert)
convertButton.pack()

status=Label(root,text="Begin -> Select input file")
status.pack(pady=(10,0),fill=X,ipady=1)


def resize_img(event):
    global dnd_image,dndframe
    if event.height<=event.width:
        dnd_image=Image.open(r"dnd.png").resize((event.height,event.height), Image.AFFINE)
        dnd_image = ImageTk.PhotoImage(dnd_image)
        dndframe.create_image((event.width-event.height)/2,0, image = dnd_image,anchor=NW)
    else:
        dnd_image=Image.open(r"dnd.png").resize((event.width,event.width), Image.AFFINE)
        dnd_image = ImageTk.PhotoImage(dnd_image)
        dndframe.create_image(0,(event.height-event.width)/2, image = dnd_image,anchor=NW)


dndframe.bind("<Configure>",resize_img)
root.mainloop()  