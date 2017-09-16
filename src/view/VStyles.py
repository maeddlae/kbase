'''
Created on 11 Sep 2017

@author: Mathias Bucher
'''
from Tkinter import Tk
from Tkinter import Button
from Tkinter import Entry
from Tkinter import W, END, FLAT
from Tkinter import Label
from Tkinter import Frame
from Tkinter import Text
from Tkinter import Menu
from ttk import Notebook, Style

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

def getEntrySmall(parent):
    entry = Entry(parent)
    entry["background"] = "white"   # unclicked background
    entry["borderwidth"] = 0
    entry["foreground"] = "black"  # unclicked text
    entry["font"] = ("Helvetica", 10, "bold")
    entry.grid(padx=5, pady=5, sticky=W) # padding
    return entry

def getLabel(parent, text):
    label = Label(parent, text=text)
    label["background"] = rootColor    # unclicked background
    label["borderwidth"] = 0
    label["activeforeground"] = "black"    # text when clicked
    label["foreground"] = "black"  # unclicked text
    label["activebackground"] = blue2  # background when clicked
    label["font"] = ("Helvetica", 15, "bold")
    label.grid(padx=5, pady=5, sticky=W) # padding
    return label

def getLabelBlue(parent, text):
    label = Label(parent, text=text)
    label["background"] = blue1    # unclicked background
    label["borderwidth"] = 0
    label["activeforeground"] = "black"    # text when clicked
    label["foreground"] = "black"  # unclicked text
    label["activebackground"] = blue2  # background when clicked
    label["font"] = ("Helvetica", 15, "bold")
    label.grid(padx=5, pady=5, sticky=W) # padding
    return label

def getLabelSmall(parent, text):
    label = Label(parent, text=text)
    label["background"] = rootColor    # unclicked background
    label["borderwidth"] = 0
    label["activeforeground"] = "black"    # text when clicked
    label["foreground"] = "black"  # unclicked text
    label["activebackground"] = blue2  # background when clicked
    label["font"] = ("Helvetica", 10, "bold")
    label.grid(padx=5, pady=5, sticky=W) # padding
    return label

def getImageLabel(parent, image):
    label = Label(parent, image=image)
    label["background"] = rootColor    # unclicked background
    label["borderwidth"] = 0
    label["activeforeground"] = "black"    # text when clicked
    label["foreground"] = "black"  # unclicked text
    label["activebackground"] = blue2  # background when clicked
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

def getLargeTextBlue(parent, text):
    t = Text(parent)
    t["height"] = 1
    t["width"] = 32
    t["background"] = blue1    # unclicked background
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

def getMenu(parent):
    menu = Menu(parent, tearoff=0)
    menu["activebackground"] = blue2  # background when clicked
    menu["background"] = rootColor    # unclicked background
    menu["borderwidth"] = 0
    menu["activeborderwidth"] = 0
    menu["activeforeground"] = "black"    # text when clicked
    menu["foreground"] = "black"  # unclicked text
    menu["relief"] = FLAT  # unclicked text
    menu["font"] = ("Helvetica", 15, "bold")
    return menu

def styleNotebook(notebook):
    style = Style()

    style.theme_create( "yummy", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0], "background" : rootColor} },
        "TNotebook.Tab": {
            "configure": {"padding": [5, 1], "background": rootColor, 
                          "font" : ("Helvetica", 15, "bold") },
            "map":       {"background": [("selected", rootColor)] } } } )

    style.theme_use("yummy")
    return notebook

