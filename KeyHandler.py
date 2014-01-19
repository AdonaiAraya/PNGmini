# -*- coding: utf-8 -*-
import json
import os
import sys

def find_data_file( filename ):
    if getattr(sys, 'frozen', False):
        datadir = os.path.dirname(sys.executable)
    else:
        datadir = os.path.dirname(os.path.realpath(__file__))

    return os.path.join(datadir, filename)

class KeyHandler:
    KEY_FILE_PATH = find_data_file( "keys.json" )

    @staticmethod
    def getKey():
        if os.path.exists(KeyHandler.KEY_FILE_PATH):
            if os.access(KeyHandler.KEY_FILE_PATH, os.R_OK):
                json_data = open( KeyHandler.KEY_FILE_PATH ).read()
                data = json.loads(json_data)
                for user in data["users"]:
                    if user["current"]:
                        return user["key"]
                raise Exception( "No hay ninguna clave asignada" )
            else:
                raise Exception( "No se ha podido leer el fichero 'keys.json', comprueba los permisos." )
        else:
            raise Exception( "El fichero 'keys.json' no existe." )

    @staticmethod
    def setKey( email, key, current ):
        if os.path.exists(KeyHandler.KEY_FILE_PATH):
            if os.access(KeyHandler.KEY_FILE_PATH, os.W_OK):
                json_data = open( KeyHandler.KEY_FILE_PATH ).read()
                data = json.loads(json_data)
                if current:
                    for user in data["users"]:
                        user["current"] = False
                for user in data["users"]:
                    if user["email"] == email:
                        user["email"] = email
                        user["key"] = key
                        user["current"] = current
                        break
                else:
                    data["users"].append({
                        "email": email,
                        "key": key,
                        "current": current
                    })
                users = json.dumps( data, indent = 4, sort_keys = True )
                key_file = open( KeyHandler.KEY_FILE_PATH, "w" )
                key_file.write( users )
                key_file.close()
            else:
                raise Exception( "No se ha podido escribir en el fichero 'keys.json', comprueba los permisos." )
        else:
            raise Exception( "El fichero 'keys.json' no existe." )

    @staticmethod
    def deleteKey( email ):
        if os.path.exists(KeyHandler.KEY_FILE_PATH):
            if os.access(KeyHandler.KEY_FILE_PATH, os.W_OK):
                json_data = open( KeyHandler.KEY_FILE_PATH ).read()
                data = json.loads(json_data)
                already_exist = False
                position = 0
                for user in data["users"]:
                    if user["email"] == email:
                        already_exist = True
                        break
                    position += 1
                if already_exist:
                    del data["users"][position]
                else:
                    raise Exception( "El usuario que desea borrar no existe" )
                users = json.dumps( data, indent = 4, sort_keys = True )
                key_file = open( KeyHandler.KEY_FILE_PATH, "w" )
                key_file.write( users )
                key_file.close()
            else:
                raise Exception( "No se ha podido escribir en el fichero 'keys.json', comprueba los permisos." )
        else:
            raise Exception( "El fichero 'keys.json' no existe." )

    @staticmethod
    def getUsers():
        if os.path.exists(KeyHandler.KEY_FILE_PATH):
            if os.access(KeyHandler.KEY_FILE_PATH, os.R_OK):
                json_data = open( KeyHandler.KEY_FILE_PATH ).read()
                data = json.loads(json_data)
                return data["users"]
            else:
                raise Exception( "No se ha podido escribir en el fichero 'keys.json', comprueba los permisos." )
        else:
            raise Exception( "El fichero 'keys.json' no existe." )

