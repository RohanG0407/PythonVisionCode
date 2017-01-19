import numpy as np
import cv2
from Tkinter import *
from PIL import Image 
from picamera import PiCamera
import time
import sys 
import Tkinter
import picamera.array
import io
import ImageTk

def callback():
        stream = io.BytesIO()
        camera.brightness = int(tbox.get())
        camera.capture(stream, format='jpeg')
        stream.seek(0)
        im2 = Image.open(stream)
        tkimage2 = ImageTk.PhotoImage(im2)
        panel.configure(image=tkimage2)
        panel.image = tkimage2
        print tbox.get()

camera = PiCamera()
camera.brightness = 20
camera.start_preview
#time.sleep(2)
stream = io.BytesIO()
camera.capture(stream, format='jpeg')
stream.seek(0)
im = Image.open(stream)
#root = Tkinter.Tk()
#b = Button(root, text="ok", command=callback)
#b.pack()
#tbox = Entry(root, text='brightness')
#tbox.insert(END,'20')
#tbox.pack()
#tkimage = ImageTk.PhotoImage(im)
#panel = Tkinter.Label(root, image=tkimage)
#panel.pack(side = "bottom", fill = "both", expand = "yes")
#root.mainloop()

