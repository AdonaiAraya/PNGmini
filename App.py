# -*- coding: utf-8 -*-
from functions import *
from controls import *

class App( Frame ):
    key = None
    root = ""
    replaceFiles = False
    setCurrent = False
    files = []
    successFiles = []
    errorFiles = []
    users = []

    def __init__( self, mainWindow ):
        self.root = mainWindow
        self.createInterface()
        self.panelApp()
        self.qu = queue.Queue()
        try:
            self.key = KeyHandler.getKey()
        except Exception as msg:
            self.importantNotifications.show(msg)
            self.key = None

    def standByApp(self):
        #Panel - Menu
        self.mainMenu.entryconfig(0, state = DISABLED )
        self.mainMenu.entryconfig(1, state = DISABLED )
        #Panel - App
        self.compressFiles.config( state = DISABLED )
        self.selectFiles.config( state = DISABLED )
        self.inputNewName.config( state = DISABLED )
        self.replaceChoice.config( state = DISABLED )
        self.resume.hide()
        #Panel - KeyManager
        self.entry_clave.config( state = DISABLED )
        self.entry_correo.config( state = DISABLED )
        self.checkbox_current.config( state = DISABLED )
        self.keyList.config( state = DISABLED )
        self.button_delete.config( state = DISABLED )
        self.button_add_edit.config( state = DISABLED )

    def resetApp(self):
        #Panel - Menu
        self.mainMenu.entryconfig(0, state = NORMAL )
        self.mainMenu.entryconfig(1, state = NORMAL )
        #Panel - App
        self.files = []
        self.successFiles = []
        self.errorFiles = []
        self.compressFiles.config( state = NORMAL )
        self.selectFiles.config( state = NORMAL )
        self.inputNewName.config( state = NORMAL )
        self.inputNewName.delete( 0, END )
        self.replaceChoice.config( state = ACTIVE )
        self.replaceChoice.deselect()
        self.replaceFiles = False
        self.pbComprimidos.hide()
        self.notifications.hide()
        changeFileLabel( self )
        #Panel - KeyManager
        self.keyList.deleteList()
        self.keyList.config( state = NORMAL )
        self.entry_clave.delete( 0, END )
        self.entry_clave.config( state = NORMAL )
        self.entry_correo.delete( 0, END )
        self.entry_correo.config( state = NORMAL )
        self.checkbox_current.config( state = ACTIVE )
        self.checkbox_current.deselect()
        self.button_delete.config( state = NORMAL )
        self.button_add_edit.config( state = NORMAL )
        self.key_notifications.hide()

    def createInterface(self):
        #Menu
        self.mainMenu = Menu(
            self.root,
            tearoff = False,
            background = "#363636",
            activebackground = "#363636",
            foreground = "#fafafa",
            activeforeground = "#92a8cc",
            cursor = "hand2",
        )
        self.mainMenu.add_command(
            label = "Comprimir ficheros",
            activebackground = "#fafafa",
            activeforeground = "#92a8cc",
            command = lambda : self.showPanelApp()
        )
        self.mainMenu.add_command(
            label = "Gestionar claves",
            activebackground = "#fafafa",
            activeforeground = "#92a8cc",
            command = lambda : self.showPanelKeyManager()
        )
        self.root.config( menu = self.mainMenu )

        #Boton selección fichero
        self.selectFiles = Button(
            self.root,
            text = "Selecciona los ficheros",
            background = "#92a8cc",
            activebackground = "#fafafa",
            foreground = "#fafafa",
            activeforeground = "#92a8cc",
            cursor = "hand2",
            border = 0,
            padx = 8,
            pady = 8,
            command = lambda : elegirFicheros( self )
        )

        #Label información de los ficheros seleccionados
        self.infoSelectFiles = Label(
            self.root,
            text = "No se ha seleccionado ningún fichero.",
            background = "#ffffff",
            foreground = "#363636"
        )

        #Entry Input para el nuevo nombre
        self.inputNewName = Entry(
            self.root,
            background = "#ffffff",
            foreground = "#363636"
        )

        #Label Texto de escoger nuevo nombre
        self.infoInputNewName = Label(
            self.root,
            text = "Escoja el nuevo nombre:",
            background = "#ffffff",
            foreground = "#363636"
        )

        #Checkbox Para elegir si reemplazar los archivos o crear nuevos
        self.replaceChoice = Checkbutton(
            self.root,
            background = "#ffffff",
            activebackground = "#ffffff",
            foreground = "#363636",
            activeforeground = "#363636",
            borderwidth = 0,
            highlightthickness = 0,
            cursor = "hand2",
            offvalue = False,
            onvalue = True,
            text = "Reemplazar archivos",
            command = lambda : checkReplaceFiles( self )
        )

        #Boton comprimir archivos
        self.compressFiles = Button(
            self.root,
            text = "Comprimir archivos",
            background = "#363636",
            activebackground = "#fafafa",
            foreground = "#fafafa",
            activeforeground = "#92a8cc",
            cursor = "hand2",
            border = 0,
            padx = 8,
            pady = 8,
            command = lambda : comprimirArchivos( self )
        )

        #Label Notificaciones importantes
        self.importantNotifications = ImportantNotification( self.root )

        #Label notificaciones
        self.notifications = Notification( self.root )
        self.notifications.place( x = 25, y = 230 )
        self.notifications.savePlaceData()
        self.notifications.hide()

        #Label Resume
        self.resume = Resume( self.root )

        #Barra de progreso
        self.pbComprimidos = PB( self.root )

        #Listbox Correos de listbox
        self.keyList = LB( self.root )
        self.keyList.bind( "<<ListboxSelect>>", lambda event : selectItem( event, self ) )

        #Label Correo
        self.label_correo = Label(
            self.root,
            text = "Email: ",
            background = "#ffffff",
            foreground = "#363636"
        )

        #Entry Correo
        self.entry_correo = Entry(
            self.root,
            background = "#ffffff",
            foreground = "#363636"
        )

        #Label Clave
        self.label_clave = Label(
            self.root,
            text = "Clave: ",
            background = "#ffffff",
            foreground = "#363636"
        )

        #Entry Clave
        self.entry_clave = Entry(
            self.root,
            background = "#ffffff",
            foreground = "#363636"
        )

        #Checkbox Current
        self.checkbox_current = Checkbutton(
            self.root,
            background = "#ffffff",
            activebackground = "#ffffff",
            foreground = "#363636",
            activeforeground = "#363636",
            borderwidth = 0,
            highlightthickness = 0,
            cursor = "hand2",
            offvalue = False,
            onvalue = True,
            text = "Usar esta clave para comprimir ficheros.",
            command = lambda : checkSetCurrent( self )
        )
        #Button Añadir / Editar
        self.button_add_edit = Button(
            self.root,
            text = "Añadir / Editar usuario",
            background = "#363636",
            activebackground = "#fafafa",
            foreground = "#fafafa",
            activeforeground = "#92a8cc",
            cursor = "hand2",
            border = 0,
            padx = 8,
            pady = 8,
            command = lambda : addEditUser( self, self.entry_correo.get(), self.entry_clave.get(), self.setCurrent )
        )

        #Button Delete
        self.button_delete = Button(
            self.root,
            text = "Borrar usuario",
            background = "#363636",
            activebackground = "#fafafa",
            foreground = "#fafafa",
            activeforeground = "#92a8cc",
            cursor = "hand2",
            border = 0,
            padx = 8,
            pady = 8,
            command = lambda : deleteUser( self, self.entry_correo.get() )
        )

        #Label KeyNotification
        self.key_notifications = Notification( self.root )

    def panelApp(self):
        self.selectFiles.place( x = 25, y = 25 )
        self.infoSelectFiles.place( x = 180, y = 30 )
        self.inputNewName.place( x = 180, y = 85, width = 200 )
        self.infoInputNewName.place( x = 25, y = 85 )
        self.replaceChoice.place( x = 25, y = 135 )
        self.compressFiles.place( x = 25, y = 185 )
        self.importantNotifications.place( x = 0, y = 0, width = 425 )
        self.importantNotifications.savePlaceData()
        self.importantNotifications.hide()
        self.resume.place( x = 25, y = 230 )
        self.resume.savePlaceData()
        self.resume.hide()
        self.pbComprimidos.place( x = 25, y = 280, width = 375 )
        self.pbComprimidos.savePlaceData()
        self.pbComprimidos.hide()

    def panelKeyManager(self):
        self.users = KeyHandler.getUsers()
        self.keyList.place( x = 25, y = 25, width = 375, height = 100 )
        self.keyList.savePlaceData()
        self.keyList.insertList( self.users )
        self.keyList.scbar.place( x = 385, y = 25, height = 100 )
        self.keyList.scbar.pi = self.keyList.scbar.place_info()
        self.label_correo.place( x = 25, y = 150 )
        self.entry_correo.place( x = 100, y = 150, width = 300 )
        self.label_clave.place( x = 25, y = 190 )
        self.entry_clave.place( x = 100, y = 190, width = 300 )
        self.checkbox_current.place( x = 25, y = 230 )
        self.button_add_edit.place( x = 25, y = 270 )
        self.button_delete.place( x = 305, y = 270 )
        self.key_notifications.place( x = 25, y = 310 )
        self.key_notifications.savePlaceData()
        self.key_notifications.hide()

    def showPanelApp(self):
        self.resetApp()
        self.hidePanelKeyManager()
        self.panelApp()

    def showPanelKeyManager(self):
        self.resetApp()
        self.hidePanelApp()
        self.panelKeyManager()

    def hidePanelApp(self):
        self.selectFiles.place_forget()
        self.infoSelectFiles.place_forget()
        self.inputNewName.place_forget()
        self.infoInputNewName.place_forget()
        self.replaceChoice.place_forget()
        self.compressFiles.place_forget()
        self.importantNotifications.place_forget()
        self.resume.hide()
        self.pbComprimidos.hide()

    def hidePanelKeyManager(self):
        self.keyList.hide()
        self.label_correo.place_forget()
        self.entry_correo.place_forget()
        self.label_clave.place_forget()
        self.entry_clave.place_forget()
        self.checkbox_current.place_forget()
        self.button_add_edit.place_forget()
        self.button_delete.place_forget()


