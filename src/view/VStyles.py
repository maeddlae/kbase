'''
Created on 11 Sep 2017

@author: Mathias Bucher
'''
from Tkinter import Tk
from Tkinter import Button
from Tkinter import Entry
from Tkinter import W, END
from Tkinter import Label
from Tkinter import Frame
from Tkinter import Text
from Tkinter import Scrollbar

# used colors
blue0 = "#99CCFF"
blue1 = "#66B2FF"
blue2 = "#3399FF"

# default background color
rootColor = blue0

def getRoot():
    root = Tk()
    root.title("kbase")
    root.geometry("550x500")
    root.configure(bg=rootColor)
    return root
    
def getButtonMenu(parent):
    button = Button(parent)
    button["activebackground"] = blue2  # background when clicked
    button["background"] = blue1    # unclicked background
    button["borderwidth"] = 0
    button["activeforeground"] = "black"    # text when clicked
    button["foreground"] = "black"  # unclicked text
    button["font"] = ("Helvetica", 15, "bold")
    button.grid(padx=5, pady=5, sticky=W) # padding
    return button
    
def getButtonEntry(parent, command):
    button = Button(parent, command=command)
    button["activebackground"] = blue2  # background when clicked
    button["background"] = blue1    # unclicked background
    button["borderwidth"] = 0
    button["activeforeground"] = "black"    # text when clicked
    button["foreground"] = "black"  # unclicked text
    button["font"] = ("Helvetica", 15, "bold")
    button.grid(padx=5, pady=5, sticky=W) # padding
    return button
    
def getEntry(parent):
    entry = Entry(parent)
    entry["background"] = "white"    # unclicked background
    entry["borderwidth"] = 0
    entry["foreground"] = "black"  # unclicked text
    entry["font"] = ("Helvetica", 15, "bold")
    entry.grid(padx=5, pady=5, sticky=W) # padding
    return entry

def getLabel(parent, text):
    label = Label(parent, text=text)
    label["activebackground"] = rootColor  # background when clicked
    label["background"] = rootColor    # unclicked background
    label["borderwidth"] = 0
    label["activeforeground"] = "black"    # text when clicked
    label["foreground"] = "black"  # unclicked text
    label["font"] = ("Helvetica", 15, "bold")
    label.grid(padx=5, pady=5, sticky=W) # padding
    return label

def getFrame(parent):
    frame = Frame(parent)
    frame["background"] = rootColor    # unclicked background
    frame["borderwidth"] = 0
    frame.grid(padx=5, pady=5, sticky=W) # padding
    return frame

def getLargeText(parent, text):
    t = Text(parent)
    t["height"] = 1
    t["width"] = 32
    t["background"] = rootColor    # unclicked background
    t["borderwidth"] = 0
    t["foreground"] = "black"  # unclicked text
    t["font"] = ("Helvetica", 15, "bold")
    t.insert(END, text)
    t.grid(sticky=W)
    return t

def getSmallText(parent, text):
    t = Text(parent)
    t["height"] = 6
    t["width"] = 50
    t["background"] = rootColor    # unclicked background
    t["borderwidth"] = 0
    t["foreground"] = "black"  # unclicked text
    t["font"] = ("Helvetica", 10)
    t.insert(END, text)
    t.grid(sticky=W)
    return t

def getScrollbar(parent, target):
    scrollbar = Scrollbar(parent, command=target.yview)
    scrollbar["activebackground"] = rootColor  # background when clicked
    scrollbar["background"] = rootColor    # unclicked background
    scrollbar["borderwidth"] = 0
    scrollbar["troughcolor"] = rootColor    # unclicked background
    scrollbar.grid(sticky=W)
    target['yscrollcommand'] = scrollbar.set  
    return scrollbar