# -*- coding: utf-8 -*-
from App import *

if __name__ == "__main__":
    #Ventana principal
    mainWindow = Tk()
    mainWindow.title("PNGmini")
    mainWindow.resizable(0, 0)
    mainWindow.geometry("425x350")
    mainWindow.iconbitmap( "PNGmini_logo128x128.ico" )
    mainWindow.config(
        background = "#ffffff",
        width = 425,
        height = 350
    )
    #Aplicacion
    app = App( mainWindow )
    #Bucle principal
    mainWindow.mainloop()
