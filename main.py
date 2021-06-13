import os
from tkinter import Canvas, Frame, Label, filedialog, ttk, messagebox
from tkinter.constants import BOTH, END, LEFT, NW, TOP, X
from tkdnd_wrapper import TkDND
from PIL import Image, ImageTk
from threading import Thread
from hdpitkinter import HdpiTk
import cv2
import subprocess

os.environ["TKDND_LIBRARY"] = "pytkdnd2.8"

base_color = "#fafafa"


class Global:
    def __init__(self):
        self.ipfileAddr = None
        self.ipextension = None
        self.opDir = None
        self.opextension = None
        self.file_name = None
        self.fileType = None
        self.dnd_image = None
        self.preview_pic = "dnd.png"


Global = Global()

root = HdpiTk()
# root=Tk()
root.title("Convertor Utility")
root.minsize(450, 420)
root.resizable(False, False)
root.config(bg=base_color)


def create_frame_image():
    # global dnd_image
    scale = Global.dnd_image.width / Global.dnd_image.height

    if Global.dnd_image.width > Global.dnd_image.height + dndframe.winfo_height():
        img_width = dndframe.winfo_width()
        img_height = img_width / scale
    else:
        img_height = dndframe.winfo_height()
        img_width = img_height * scale

    Global.dnd_image = Global.dnd_image.resize(
        (int(img_width), int(img_height)), Image.ADAPTIVE
    )
    Global.dnd_image = ImageTk.PhotoImage(Global.dnd_image)
    dndframe.create_image(
        (dndframe.winfo_width() - Global.dnd_image.width()) / 2,
        (dndframe.winfo_height() - Global.dnd_image.height()) / 2,
        image=Global.dnd_image,
        anchor=NW,
    )
    dndframe.image = Global.dnd_image


def make_video_thumbnail():
    # global ipfileAddr, dnd_image
    vcap = cv2.VideoCapture(Global.ipfileAddr)
    res, im_ar = vcap.read()
    while im_ar.mean() < res:
        res, im_ar = vcap.read()
    im_ar = cv2.resize(im_ar, (1920, 1080), 0, 0, cv2.INTER_LINEAR)
    color_coverted = cv2.cvtColor(im_ar, cv2.COLOR_BGR2RGB)

    Global.dnd_image = Image.fromarray(color_coverted)
    create_frame_image()


def img_preview():
    # global preview_pic, dnd_image
    root.update()
    Global.dnd_image = Image.open(Global.preview_pic)
    create_frame_image()


def resetUI():
    # global ipfileAddr, opDir, preview_pic
    Global.ipfileAddr = Global.opDir = None
    inputBox.delete(0, "end")
    outputBox.delete(0, "end")
    Global.preview_pic = "dnd.png"
    img_preview()


def update_status():
    print("Converted Successfully")
    status.config(text="Converted Successfully")
    resetUI()


def decide_preview():
    # global ipfileAddr, ipextension, fileType, preview_pic
    if Global.ipextension in ["jpg", "jpeg", "png", "webp", "tiff"]:
        Global.fileType = "image"
        Global.preview_pic = Global.ipfileAddr
        img_preview()
    elif Global.ipextension in ["mp3", "wav", "flac", "ogg"]:
        Global.fileType = "audio"
    elif Global.ipextension in ["mp4", "avi", "flv", "mov", "mkv", "webm"]:
        Global.fileType = "video"
        make_video_thumbnail()


def openFile():
    # global ipfileAddr, ipextension, preview_pic, fileType
    inputBox.delete(0, "end")
    outputBox.delete(0, "end")
    Global.ipfileAddr = (
        filedialog.askopenfile(
            parent=root,
            mode="rb",
            title="Choose a file",
            filetype=[("All files", "*.*")],
        )
    ).name
    inputBox.insert(END, Global.ipfileAddr)
    Global.ipextension = getExtension(Global.ipfileAddr).lower()
    print(f'Input File: "{Global.ipfileAddr}"\nExt: {Global.ipextension}')
    if Global.ipfileAddr:
        status.config(text="Now select output directory")
    decide_preview()


def getExtension(loc):
    # global file_name
    Global.file_name, file_extension = os.path.splitext(loc)
    file_extension = file_extension[1:]
    return file_extension


def outpFile():  # sourcery no-metrics
    # global ipextension, opDir, opextension, file_name, ipfileAddr, fileType
    # image
    if Global.ipextension == "png":
        fileOptions = [
            ("jpeg files", "*.jpg"),
            ("webp files", "*.webp"),
            ("ico files", "*.ico"),
            ("tiff files", "*.tiff"),
            ("All Files", "*.*"),
        ]

    elif Global.ipextension in ["jpg", "jpeg"]:
        fileOptions = [
            ("png files", "*.png"),
            ("webp files", "*.webp"),
            ("tiff files", "*.tiff"),
            ("All Files", "*.*"),
        ]

    elif Global.ipextension == "webp":
        fileOptions = [
            ("png files", "*.png"),
            ("jpeg files", "*.jpg"),
            ("ico files", "*.ico"),
            ("tiff files", "*.tiff"),
            ("All Files", "*.*"),
        ]

    elif Global.ipextension == "tiff":
        fileOptions = [
            ("png files", "*.png"),
            ("jpeg files", "*.jpg"),
            ("ico files", "*.ico"),
            ("webp files", "*.webp"),
            ("All Files", "*.*"),
        ]

    elif Global.ipextension == "mp3":
        fileOptions = [
            ("wav files", "*.wav"),
            ("flac files", "*.flac"),
            ("ogg files", "*.ogg"),
            ("All Files", "*.*"),
        ]

    elif Global.ipextension == "wav":
        fileOptions = [
            ("mp3 files", "*.mp3"),
            ("flac files", "*.flac"),
            ("ogg files", "*.ogg"),
            ("All Files", "*.*"),
        ]

    elif Global.ipextension == "flac":
        fileOptions = [
            ("mp3 files", "*.mp3"),
            ("wav files", "*.wav"),
            ("ogg files", "*.ogg"),
            ("All Files", "*.*"),
        ]

    elif Global.ipextension == "ogg":
        fileOptions = [
            ("mp3 files", "*.mp3"),
            ("wav files", "*.wav"),
            ("flac files", "*.flac"),
            ("All Files", "*.*"),
        ]

    elif Global.ipextension == "mp4":
        fileOptions = [
            ("avi files", "*.avi"),
            ("flv files", "*.flv"),
            ("mov files", "*.mov"),
            ("mp3 files", "*.mp3"),
            ("mkv files", "*.mkv"),
            ("webm files", "*.webm"),
            ("All Files", "*.*"),
        ]

    elif Global.ipextension == "avi":
        fileOptions = [
            ("mp4 files", "*.mp4"),
            ("flv files", "*.flv"),
            ("mov files", "*.mov"),
            ("mkv files", "*.mkv"),
            ("webm files", "*.webm"),
            ("All Files", "*.*"),
        ]

    elif Global.ipextension == "flv":
        fileOptions = [
            ("mp4 files", "*.mp4"),
            ("avi files", "*.avi"),
            ("mov files", "*.mov"),
            ("mkv files", "*.mkv"),
            ("webm files", "*.webm"),
            ("All Files", "*.*"),
        ]

    elif Global.ipextension == "mov":
        fileOptions = [
            ("mp4 files", "*.mp4"),
            ("avi files", "*.avi"),
            ("flv files", "*.flv"),
            ("mkv files", "*.mkv"),
            ("webm files", "*.webm"),
            ("All Files", "*.*"),
        ]

    elif Global.ipextension == "mkv":
        fileOptions = [
            ("mp4 files", "*.mp4"),
            ("avi files", "*.avi"),
            ("flv files", "*.flv"),
            ("mov files", "*.mov"),
            ("webm files", "*.webm"),
            ("All Files", "*.*"),
        ]

    elif Global.ipextension == "webm":
        fileOptions = [
            ("mp4 files", "*.mp4"),
            ("avi files", "*.avi"),
            ("flv files", "*.flv"),
            ("mov files", "*.mov"),
            ("mkv files", "*.mkv"),
            ("All Files", "*.*"),
        ]

    else:
        messagebox.showerror(
            title="Error", message="Conversion not possible.\nFile type not supported."
        )
        resetUI()
        return
    outputBox.delete(0, "end")

    Global.file_name = Global.file_name[::-1]
    Global.file_name = Global.file_name[Global.file_name.find("/") :]
    Global.file_name = Global.file_name[::-1]

    base = os.path.basename(Global.ipfileAddr)
    base_name = os.path.splitext(base)[0]
    Global.opDir = filedialog.asksaveasfilename(
        parent=root,
        title="Convert as",
        filetypes=fileOptions,
        defaultextension=fileOptions,
        initialdir=Global.file_name,
        initialfile=base_name,
    )
    outputBox.insert(END, Global.opDir)
    Global.opextension = getExtension(Global.opDir)
    print(f'Output File: "{Global.opDir}"\nExt: {Global.opextension}')
    if Global.opDir:
        status.config(text="Press convert")


def startConvert():
    # global ipfileAddr, ipextension, opDir, opextension, fileType
    if Global.ipfileAddr:
        if Global.opDir:
            print(f"\nConverting from {Global.ipextension} to {Global.opextension}")
            if Global.fileType == "image":
                Thread(target=convertImage).start()
            elif Global.fileType in ["audio", "video"]:
                Thread(target=convertAudio_Video).start()
        else:
            status.config(text="Please select output directory")
            return
    else:
        status.config(text="Please select input file")
        return


def convertAudio_Video():
    # global ipfileAddr, ipextension, opDir, opextension
    status.config(text="Converting...")
    # os.system(f'cmd /c ffmpeg -i "{ipfileAddr}" "{opDir}"')
    subprocess.call(f'ffmpeg -i "{Global.ipfileAddr}" -y "{Global.opDir}"', shell=False)
    update_status()


def convertImage():
    # global ipfileAddr, ipextension, opDir, opextension
    status.config(text="Converting...")
    if Global.opextension == "jpg":
        image = Image.open(Global.ipfileAddr).convert("RGB")
        if image.mode in ("RGBA", "LA"):
            fill_color = "#ffffff"
            background = Image.new(image.mode[:-1], image.size, fill_color)
            background.paste(image, image.split()[-1])
            image = background
        image.save(Global.opDir, "JPEG", quality=95)

    elif Global.opextension == "ico":
        img = Image.open(Global.ipfileAddr)
        new_img = img.resize((256, 256))
        icon_sizes = [
            (16, 16),
            (24, 24),
            (32, 32),
            (48, 48),
            (64, 64),
            (72, 72),
            (80, 80),
            (96, 96),
            (128, 128),
            (256, 256),
        ]
        new_img.save(Global.opDir, sizes=icon_sizes)
    else:
        image = Image.open(Global.ipfileAddr)
        image.save(Global.opDir)
    update_status()


def handle_dnd(event):
    # global ipfileAddr, ipextension, preview_pic
    status.config(text=" ")
    inputBox.delete(0, "end")
    outputBox.delete(0, "end")
    inputBox.insert(0, (event.data).replace("{", "").replace("}", ""))
    Global.ipfileAddr = inputBox.get()
    Global.ipextension = getExtension(inputBox.get()).lower()
    print(f'Input File: "{Global.ipfileAddr}"\nExt: {Global.ipextension}')
    if Global.ipfileAddr:
        status.config(text="Now select output directory")
    decide_preview()


top_frame = Frame(root, bg=base_color)
top_frame.pack(side=TOP, fill=X, padx=10, pady=10)

inputLabel = Label(top_frame, text="Input File", bg=base_color)
inputLabel.pack(side=LEFT)

inputBox = ttk.Entry(top_frame)
# root.update()
inputBox.pack(side=LEFT, fill=X, expand=True, padx=5, ipady=1)
inputBox.focus_set()

browseButton1 = ttk.Button(top_frame, text="Browse", command=openFile)
browseButton1.pack(side=LEFT)


dndframe = Canvas(
    root, highlightthickness=1, relief="solid", highlightbackground="#c5c5c5"
)
dndframe.pack(fill=BOTH, expand=True, padx=10)

dnd = TkDND(root)
dnd.bindtarget(dndframe, handle_dnd, "text/uri-list")


bottom_frame = Frame(root, bg=base_color)
bottom_frame.pack(fill=X, padx=10, pady=10)

outputLabel = Label(bottom_frame, text="Output File", bg=base_color)
outputLabel.pack(side=LEFT)

outputBox = ttk.Entry(bottom_frame)
# root.update()
outputBox.pack(side=LEFT, fill=X, expand=True, padx=5, ipady=1)

browseButton2 = ttk.Button(bottom_frame, text="Browse", command=outpFile)
browseButton2.pack(side=LEFT)


convertButton = ttk.Button(root, text="Convert", command=startConvert)
convertButton.pack()

status = Label(root, text="Begin -> Select input file")
status.pack(pady=(10, 0), fill=X, ipady=1)


img_preview()
root.mainloop()
