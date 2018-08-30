'''
Created on Apr 13, 2018
@author: wjuarez
'''
from .models import Usuario


''''
verifico si es enfermera o doctor el usuario que pasamos como parametro
con la finalidad de recuperar el usuario del medico, recupero el
nombre del usuario, no el objeto
'''
def findUserName(username):
    try:
        user = Usuario.objects.get(pk = username.upper())
        if(user.id_rol.id == 1):
            return username
        else:
            return user.id_usuario.id
    except Exception as ex:
        raise (ex)
    

''''
verifico si es enfermera o doctor el usuario que pasamos como parametro
con la finalidad de recuperar el usuario del medico, recupero el objeto
con referencia al usuario
'''    
def findUser(username):
    try:
        user = Usuario.objects.get(pk = username.upper())
        if(user.id_rol.id == 1):
            return user
        else:
            return user.id_usuario
    except Exception as ex:
        raise (ex)