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


frameWidth=580
frameHeight=200
ipfileAddr=ipextension=opDir=opextension=file_name=fileType="null"


def resetUI():
    inputBox.delete(0, 'end')
    outputBox.delete(0, 'end')
    dndframe.create_image(2,2, image = image, anchor = NW)

def openFile():
    global ipfileAddr,ipextension
    status.config(text=" ")
    inputBox.delete(0, 'end')
    outputBox.delete(0, 'end')
    ipfileAddr=(filedialog.askopenfile(parent=root,mode='rb',title='Choose a file',filetype=[("All files","*.*")])).name
    inputBox.insert(END,ipfileAddr)
    ipextension=getExtension(ipfileAddr)
    print(f'Input File: "{ipfileAddr}"\nExt: {ipextension}')


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

def startConvert():
    global ipfileAddr,ipextension,opDir,opextension,fileType
    print(f"\nConverting from {ipextension} to {opextension}")
    if fileType=="image":
        Thread(target=convertImage).start()
    elif fileType=="audio":
        Thread(target=convertAudio).start()
    elif fileType=="video":
        Thread(target=convertVideo).start()

def convertAudio():
    global ipfileAddr,ipextension,opDir,opextension
    status.config(text="Converting...")
    audio=AudioSegment.from_file(ipfileAddr,format=ipextension)
    audio.export(opDir,format=opextension)
    print("converted")
    status.config(text="Converted Successfully")
    resetUI()
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
    print("Converted Successfully")
    status.config(text="Converted Successfully")
    resetUI()
    return


def convertVideo():
    global ipfileAddr,ipextension,opDir,opextension
    status.config(text="Converting...")
    os.system(f'cmd /c "ffmpeg -i "{ipfileAddr}" "{opDir}"')
    print("converted")
    status.config(text="Converted Successfully")
    resetUI()
    return


root = Tk() 
root.title("Convertor Util (Made by Sourabh Sathe)") 
root.resizable(False,False)
pixelVirtual=PhotoImage(width=1,height=1)



frame=Frame(root,width=frameWidth,height=frameHeight)
frame.pack()





inputLabel=Label(root,text="Input File")
inputLabel.place(x=10,y=5)

inputBox = Entry(root,width=75)
root.update()
inputBox.place(x=inputLabel.winfo_reqwidth()+15,y=5)
inputBox.focus_set()

browseButton1=Button(root,text="Browse",image=pixelVirtual,compound="c",height=12,command=openFile)
browseButton1.place(x=inputLabel.winfo_width()+inputBox.winfo_reqwidth()+20,y=5)


outputLabel=Label(root,text="Output File")
outputLabel.place(x=10,y=140)

outputBox = Entry(root,width=73)
root.update()
outputBox.place(x=outputLabel.winfo_reqwidth()+15,y=140)


browseButton2=Button(root,text="Browse",image=pixelVirtual,compound="c",height=12,command=outpFile)
browseButton2.place(x=outputLabel.winfo_width()+outputBox.winfo_reqwidth()+20,y=140)


dndframe = Canvas(root, width=100,height=100)
dndframe.place(x=10, y=inputLabel.winfo_reqheight()+10)
image = PhotoImage(file = "dnd.png")
dndframe.create_image(2,2, image = image, anchor = NW)
dnd = TkDND(root)
  
def handle(event):
    global ipfileAddr,ipextension
    status.config(text=" ")
    inputBox.delete(0, 'end')
    outputBox.delete(0, 'end')
    inputBox.insert(0, (event.data).replace('{',"").replace('}',""))
    ipfileAddr=inputBox.get()
    ipextension=getExtension(inputBox.get())
    print(f'Input File: "{ipfileAddr}"\nExt: {ipextension}')
    

dnd.bindtarget(dndframe, handle, 'text/uri-list') 

convertButton=Button(root,text="Convert",command=startConvert)
convertButton.place(x=(frameWidth-convertButton.winfo_reqwidth())/2,y=frameHeight-convertButton.winfo_reqheight()-10)

status=Label(root,text="")
status.place(x=0,y=frameHeight-convertButton.winfo_reqheight()-3)


root.mainloop()  