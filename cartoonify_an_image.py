#pip install easygui 
#pip install imageio
#pip install Pillow

#import for image processing
import cv2

#import for opening filebox
import easygui

#import to store images
import numpy as np

#import to read inage stroed at particular path
import imageio

#import to interact with runtime enviorments
import sys

#import for plotting
import matplotlib.pyplot as plt

#import for creating directory structure
import os

#import tkinter library 
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image

####Create a Tkinter window to open in###
top = tk.Tk()

#set window dimensions
top.geometry('400x400')

#set window title name
top.title('Cartoonify Your Image!')

#set backgorund colour
top.configure(background = 'white')

#create a label widget
label = Label(top, background = '#CDCDCD', font = ('calibri', 20, 'bold'))

####Function to upload an image

def upload():
    #open a file dialog to select an image
    ImagePath = filedialog.askopenfilename()
    cartoonify(ImagePath)

####Function to cartoonify an image
def cartoonify(ImagePath):
    #read the image from the specified path 
    originalImage = cv2.imread(ImagePath)

    #convert BGR image to RGB
    originalImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2RGB)

    #check if image loaded successfully; if it didnt give error message and exit system
    if originalImage is None:
        print("Can not find any image. Choose appropriate file.")
        sys.exit()

    #resize image
    ReSized1 = cv2.resize(originalImage, (960,540))
    #plt.imshow(ReSized1, cmap='gray')

    #CONVERT image to grayscale
    grayScaleImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)

    #resize grayscaleimage
    ReSized2 = cv2.resize(grayScaleImage, (960, 540))
    #plt.imshow(ReSized2, cmap='gray')

    #apply median blue to smoothen the gray scale image
    smoothGrayScale = cv2.medianBlur(grayScaleImage, 5)

    #resize smoothgrayscale image
    ReSized3 = cv2.resize(smoothGrayScale, (960,540))
    #plt.imshow(ReSized3, cmap='gray') 

    #Apply adaptive thresholding to retreive edges for cartoon effect
    getEdge = cv2.adaptiveThreshold(smoothGrayScale, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,13,8)
    
    #resize edge image
    ReSized4 = cv2.resize(getEdge, (960,540))
    #plt.imshow(ReSized, cmap = 'gray')

    #Apply bilateral filter to remove noise and keep edges sharp
    colorImage = cv2.bilateralFilter(originalImage, 9, 300, 300)

    #resize colorimage
    ReSized5 = cv2.resize(colorImage, (960, 540))
    #plt.imshow((ReSized5, cmap = 'gray')

    #mask the edged image with the colour image to create the cartoon effect
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask = getEdge)

    #Resize cartoon image
    ReSized6 = cv2.resize(cartoonImage, (960,540))
    #plt.imshow(ReSized6, cmap = 'gray')

    #plot the transition of images using matplotlib
    images = [ReSized1, ReSized2, ReSized3, ReSized4, ReSized5, ReSized6]
    fig, axes = plt.subplots(3, 2, figsize=(8, 8), subplot_kw={'xticks': [], 'yticks': []}, gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i],cmap='gray')

    #Create a button to save the cartoon image
    save1 = Button(top,text = 'Save cartoon image',  command = lambda:save(ReSized6, ImagePath),padx = 30, pady = 5)
    save1.configure(background = '#364156',foreground = 'white', font = ('calibri', 10, 'bold'))
    save1.pack(side = TOP, pady = 50)

    #display plotted images using matplotlin
    plt.show()
    
####Function to save image in imwrite()
def save(ReSized6, ImagePath):

    #define name
    newName = "cartoonified_Image"

    #establish where to save it
    path1 = os.path.dirname(ImagePath)
    extension = os.path.splitext(ImagePath)[1]
    path = os.path.join(path1, newName+extension)
    cv2.imwrite(path, cv2.cvtColor(ReSized6, cv2.COLOR_RGB2BGR))

    #leave a message stating where its saved
    I = "Image Saved by name " + newName + "at" + path
    tk.messagebox.showinfo(title = None, message = I)

####Upload File
upload = Button(top, text = "Cartoonify an Image",command = upload, padx = 10, pady = 5)
upload.configure(background = '#364156', foreground = 'white', font = ('calibri',10,'bold'))
upload.pack(side=TOP, pady = 50)

top.mainloop()
