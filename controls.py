# -*- coding: utf-8 -*-
from tkinter import Label, Listbox, Scrollbar
from tkinter import ttk
from tkinter import END

#Progress Bar
class PB( ttk.Progressbar ):
    def __init__(self, parent, orient = "horizontal", length = 100, value = 0):
        self.orient = orient
        self.length = length
        self.value = value
        ttk.Progressbar.__init__( self, parent, orient = self.orient, length = self.length, value = self.value )
    def savePlaceData(self):
        self.placeData = self.place_info()
    def getPlaceData(self):
        return self.placeData
    def show(self):
        self.place( self.placeData )
    def hide(self):
        self.place_forget()

#ListBox
class LB( Listbox ):
    def __init__(self, parent):
        Listbox.__init__(self, parent, background = "#ffffff", selectbackground = "#363636", selectforeground = "#fafafa" )
        self.scbar = Scrollbar( parent )
        self.config( yscrollcommand = self.scbar.set )
        self.scbar.config( command = self.yview )
    def insertList(self, list):
        for item in list:
            self.insert( END, item["email"] )
    def deleteList(self):
        self.delete(0, END)
    def savePlaceData(self):
        self.placeData = self.place_info()
    def show(self):
        self.place( self.placeData )
        self.scbar.place( self.scbar.pi )
    def hide(self):
        self.place_forget()
        self.scbar.place_forget()

#Notifications
class Notification( Label ):
    def __init__(self, parent):
        Label.__init__(self, parent, background = "#ffffff" )
    def showError(self, text):
        self.config(
            text = text,
            foreground = "#db0f0f"
        )
        self.place( self.placeData )
    def showSuccess(self, text):
        self.config(
            text = text,
            foreground = "#4b7c38"
        )
        self.place( self.placeData )
    def hide(self):
        self.place_forget()
    def savePlaceData(self):
        self.placeData = self.place_info()

#Important notification
class ImportantNotification( Label ):
    def __init__(self, parent):
        Label.__init__(self, parent, background = "#ff0000", foreground = "#ffffff", justify = "center" )
    def show(self, text):
        self.config(
            text = text
        )
        self.place( self.placeData )
    def hide(self):
        self.place_forget()
    def savePlaceData(self):
        self.placeData = self.place_info()


#Resume
class Resume( Label ):
    def __init__(self, parent):
        Label.__init__(self, parent, background = "#ffffff", foreground = "#363636", justify = "left" )
    def show(self):
        self.place( self.placeData )
    def hide(self):
        self.place_forget()
    def savePlaceData(self):
        self.placeData = self.place_info()
    def setText(self, text):
        self.config( text = text )
    def makeResume(self, app):
        txt = ""
        savedBytes = 0
        savedMegas = 0
        #ficheros correctos
        if len(app.successFiles) > 1:
            txt += str(len(app.successFiles)) + " ficheros comprimidos correctamente\n"
        elif len(app.successFiles) == 1:
            txt += "1 fichero comprimido correctamente\n "
        else:
            txt += "Ningún fichero comprimido correctamente\n "
        #ficheros incorrectos
        if len(app.errorFiles) > 1:
            txt += str(len(app.errorFiles)) + " ficheros no se pudieron comprimir\n"
        elif len(app.errorFiles) == 1:
            txt += "1 fichero no se pudo comprimir\n"
        else:
            txt += "No hubo ningún error al comprimir\n"
        #Megas ahorrados
        for fileInfo in app.successFiles:
            savedBytes += int( fileInfo["bytesSaved"] )
        savedMegas = savedBytes / 1024 / 1024
        if savedBytes > 0:
            txt += "{0:.3f}".format(savedMegas) + " MB ahorrados"
        else:
            txt += "No se ha ahorrado ningún MB"
        self.setText( txt )
        self.show()