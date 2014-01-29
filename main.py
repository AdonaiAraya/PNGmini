# -*- coding: utf-8 -*-
from App import *
from functions import find_file_path

if __name__ == "__main__":
    #Ventana principal
    mainWindow = Tk()
    mainWindow.title("PNGmini")
    mainWindow.resizable(0, 0)
    mainWindow.geometry("425x410")
    mainWindow.iconbitmap( find_file_path("PNGmini_logo128x128.ico") )
    mainWindow.config(
        background = "#ffffff",
        width = 425,
        height = 410
    )
    #Aplicacion
    app = App( mainWindow )
    #Bucle principal
    mainWindow.mainloop()
