# -*- coding: utf-8 -*-
from tkinter.filedialog import *
from urllib.request import Request, urlopen, build_opener
from base64 import b64encode
from threading import Thread
import queue
import json
import sys
from KeyHandler import KeyHandler
from tkinter import messagebox
import webbrowser

def linkTo( link ):
    webbrowser.open_new_tab( link )

def elegirFicheros( app ):
    """
    Selecciona los ficheros PNG que usaremos
    """
    files = askopenfilenames(
        parent = app.root,
        initialdir = os.path.expanduser('~'),
        multiple = True,
        filetypes = [( "Imagenes PNG", ("*.png","*.PNG" ))],
        title = "Elige las imagenes PNG que deseas comprimir"
    )
    files = app.root.tk.splitlist(files)
    app.files = files
    changeFileLabel( app )

def changeFileLabel( app ):
    """
    Comprueba y cambia el texto de selección de ficheros según el numero de ficheros seleccionados
    """
    txt = ""
    if app.infoSelectFiles is not None:
        if len(app.files) == 1:
            txt = "Se ha seleccionado un fichero."
        elif len(app.files) > 1:
            txt = "Se han seleccionado " + str(len(app.files)) + " ficheros."
        else:
            txt = "No se ha seleccionado ningún fichero."
    app.infoSelectFiles.config( text = txt )
    app.notifications.hide()

def elegirDestino( app ):
    """
    Selecciona la carpeta de destino de los ficheros
    """
    app.directory = askdirectory(
        parent = app.root,
        initialdir = os.path.expanduser('~'),
        title = "Seleccione la carpeta de destino para los ficheros comprimidos."
    )
    changeFolderDestinationLabel( app )

def changeFolderDestinationLabel( app ):
    """
    Cambia el texto de la información de la carpeta de destino
    """
    txt = ""
    if len( app.directory ) and not app.replaceFiles:
        txt = app.directory
    elif app.replaceFiles:
        txt = "El destino corresponderá a cada fichero."
    else:
        txt = "No se ha seleccionado ningún destino."
    app.infoDestinationFolder.config( text = txt )

def checkReplaceFiles( app ):
    """
    Cambia el estado de la variable para reemplazar los ficheros comprimidos
    """
    app.replaceFiles = not app.replaceFiles
    if app.replaceFiles:
        app.inputNewName.config( state = DISABLED )
        app.destinationFolder.config( state = DISABLED )
        app.keep_name = True
        app.checkbox_keepName.select()
        app.checkbox_keepName.config( state = DISABLED )
    else:
        app.inputNewName.config( state = NORMAL )
        app.destinationFolder.config( state = NORMAL )
        app.keep_name = False
        app.checkbox_keepName.deselect()
        app.checkbox_keepName.config( state = ACTIVE )
    changeFolderDestinationLabel( app )

def checkKeepName( app ):
    """
    Cambia el estado de la variable para conservar el nombre
    """
    app.keep_name = not app.keep_name
    if app.keep_name:
        app.inputNewName.config( state = DISABLED )
    elif not app.replaceFiles and not app.keep_name:
        app.inputNewName.config( state = NORMAL )

def comprimirArchivos( app ):
    """
    Crea un nuevo 'thread' para ejecutar la funcionalidad del programa
    """
    app.resume.hide()
    try:
        app.key = KeyHandler.getKey()
    except Exception as msg:
        app.importantNotifications.show(msg)
        app.key = None
    if app.key is not None:
        if len(app.files) == 0:
            app.notifications.showError( "No se han seleccionado archivos." )
        else:
            if not app.inputNewName.get().strip() and not app.replaceFiles and not app.keep_name:
                app.notifications.showError( "El campo de texto no puede estar vacio." )
            else:
                app.standByApp()
                app.pbComprimidos.show()
                thread = Thread(
                    name = "thr_comprimir",
                    target = comprimir,
                    args = (app,)
                )
                thread.start()
                checkThread( app, thread )
    else:
        app.notifications.showError( "Se debe elegir una clave de producto." )

def checkThread( app, thread ):
    """
    Comprueba que el hilo ya haya acabado para ejecutar los procesos correspondientes
    """
    checkQueue( app )
    if thread.is_alive():
        app.root.after( 100, lambda: checkThread( app, thread ) )
    else:
        app.resume.makeResume( app )
        app.resetApp()

def checkQueue( app ):
    """
    Aumenta la barra de progreso
    """
    percent = 100 / len(app.files)
    while app.qu.qsize():
        try:
            msg = app.qu.get(0)
            app.pbComprimidos.step( percent )
        except queue.empty:
            pass

def comprimir( app ):
    """
    Comprime los ficheros llamando a la API de tiny PNG
    """
    counter = 1
    for file in app.files:
        extension = os.path.splitext(os.path.basename(file))[1]
        if extension.lower() == ".png":
            newName = ""
            if app.keep_name:
                newName = os.path.splitext(os.path.basename(file))[0]
            else:
                newName = app.inputNewName.get()
            dir = ""
            if len( app.directory ):
                dir = app.directory
            else:
                dir = os.path.dirname(file)
            newPath = ""
            if app.keep_name:
                newPath = dir + "/" + newName + extension
                counter = 0
            else:
                newPath = dir + "/" + newName + "_" + str(counter) + extension
            while os.path.isfile(newPath):
                counter += 1
                newPath =  os.path.dirname(file) + "/" + newName + "_" + str(counter) + extension
            request = Request("https://api.tinypng.com/shrink", open(file, "rb").read())
            auth = b64encode(bytes("api:" + app.key, "ascii")).decode("ascii")
            request.add_header("Authorization", "Basic %s" % auth)
            response = urlopen(request)
            if response.status == 201:
                result = urlopen(response.getheader("Location")).read()
                content = response.read()
                content = json.loads(content.decode("utf8"))
                if content["output"]["size"] < content["input"]["size"]:
                    if app.replaceFiles:
                        if os.access(file, os.W_OK):
                            open(file, "wb").write(result)
                        else:
                            app.notifications.showError( "No se puede sobreescribir el fichero " + os.path.splitext(os.path.basename(file))[0] + ".png" )
                            fileInfo = {
                                "name" : file,
                                "msg" : "No se puede sobreescribir."
                            }
                            app.errorFiles.append(fileInfo)
                    else:
                        open(newPath, "wb").write(result)
                    app.notifications.showSuccess( "La compresión de '" + os.path.splitext(os.path.basename(file))[0] + ".png' ha sido satisfactoria." )
                    fileInfo = {
                        "name" : newPath,
                        "inputSize" : content["input"]["size"],
                        "outputSize" : content["output"]["size"],
                        "bytesSaved" : content["input"]["size"] - content["output"]["size"],
                        "ratio" : content["output"]["ratio"]
                    }
                    app.successFiles.append(fileInfo)
                else:
                    app.notifications.showError( "El archivo '" + os.path.splitext(os.path.basename(file))[0] + ".png' no se puede comprimir más." )
                    fileInfo = {
                        "name" : newPath,
                        "msg" : "No se puede comprimir más."
                    }
                    app.errorFiles.append(fileInfo)
            else:
                app.notifications.showError( "La compresión de '" + os.path.splitext(os.path.basename(file))[0] + ".png' ha fallado, intentelo más adelante." )
                fileInfo = {
                    "name" : newPath,
                    "msg" : "No se ha podido realizar la compresión."
                }
                app.errorFiles.append(fileInfo)
            msg = "archivo procesado"
            app.qu.put( msg )
            counter += 1
        else:
            app.notifications.showError( "El fichero '" + os.path.splitext(os.path.basename(file))[0] + os.path.splitext(os.path.basename(file))[1] + "' debe ser png." )
            fileInfo = {
                "name" : newPath,
                "msg" : "No tiene el formato correcto."
            }
            app.errorFiles.append(fileInfo)

def selectItem( event, app ):
    if len(event.widget.curselection()) > 0:
        index_item_seleccionado = int(event.widget.curselection()[0])
        usuario_seleccionado = app.users[index_item_seleccionado]
        app.entry_correo.delete( 0, END )
        app.entry_correo.insert( 0, usuario_seleccionado["email"] )
        app.entry_clave.delete( 0, END )
        app.entry_clave.insert( 0, usuario_seleccionado["key"] )
        if usuario_seleccionado["current"]:
            app.checkbox_current.select()
            app.setCurrent = True
        else:
            app.checkbox_current.deselect()
            app.setCurrent = False

def checkSetCurrent( app ):
    """
    Cambia el estado de la variable usada para identificar si se ha seleccionado un email como actual
    """
    app.setCurrent = not app.setCurrent

def addEditUser( app, correo, key, current ):
    if not correo.strip():
        app.key_notifications.showError( "El correo no puede estar vacio." )
    elif not key.strip():
        app.key_notifications.showError( "La clave no puede estar vacia." )
    else:
        try:
            KeyHandler.setKey( correo, key, current )
        except Exception as msg:
            app.key_notifications.showError( msg )
        app.resetApp()
        app.users = KeyHandler.getUsers()
        app.keyList.deleteList()
        app.keyList.insertList( app.users )
        app.key_notifications.showSuccess( "Se ha creado el usuario '" + correo + "' correctamente." )

def deleteUser( app, correo ):
    if not correo.strip():
        app.key_notifications.showError( "Se debe seleccionar un correo si se desea borrar un usuario." )
    else:
        result = messagebox.askquestion("Borrar usuario", "¿Realmente desea borrar el usuario '" + correo + "'?", icon='warning')
        if result == 'yes':
            try:
                KeyHandler.deleteKey( correo )
            except Exception as msg:
                app.key_notifications.showError( msg )
            app.resetApp()
            app.users = KeyHandler.getUsers()
            app.keyList.deleteList()
            app.keyList.insertList( app.users )
            app.key_notifications.showSuccess( "Se ha borrado el usuario '" + correo + "' correctamente." )








