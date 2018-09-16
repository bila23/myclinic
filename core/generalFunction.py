'''
Created on Apr 13, 2018
@author: wjuarez
'''
from .models import Usuario
from datetime import datetime
from datetime import timedelta


''''
verifico si es enfermera o doctor el usuario que pasamos como parametro
con la finalidad de recuperar el usuario del medico, recupero el
nombre del usuario, no el objeto
'''
def findUserName(username):
    try:
        user = Usuario.objects.get(id = username)
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
        user = Usuario.objects.get(id = username)
        if(user.id_rol.id == 1):
            return user
        else:
            return user.id_usuario
    except Exception as ex:
        raise (ex)

'''
retorna la fecha que paso como parametro en formato dd/mm/yyyy en un string
'''
def dateToString(date):
    if not date:
        return ''
    today_string = ''
    if(date.day < 10):
        today_string = '0' + str(date.day - 1)
    else:
        today_string = str(date.day)
    if(date.month < 10):
        today_string = today_string + '/0' + str(date.month)
    else:
        today_string = today_string + '/' + str(date.month)
    today_string = today_string + '/' + str(date.year)
    return today_string

'''
Funcion que pasa un string que posee una fecha en formato DD/MM/YYYY
a string con formato YYYY-MM-DD
'''
def toformat_YYYYMMDD(date):
    if not date:
        return ''
    if '/' not in date:
        return ''
    day,month,year = date.split('/')
    return str(year) + '-' + str(month) + '-' + day

'''
Funcion que retorna el dia actual en objeto de tipo Date
'''
def getToday():
    return datetime.now()


def stringToDate(date):
    '''
    Funcion que transforma un objeto de tipo string a date
    '''
    if not date:
        return None
    return datetime.strptime(date, "%Y-%m-%d").date()


def stringToDate_DDMMYYYY(date):
    if not date:
        return None
    return datetime.strptime(date, '%d/%m/%Y').date()


def stringToWeekday(date):
    if not date:
        return None
    return stringToDate_DDMMYYYY(date).weekday()
