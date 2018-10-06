from core.models import HorariosOcupados, Consultas
import core.generalFunction as gf
import datetime
from django.db.models import Max

def recover_consulta(pk, user):
    consulta_recover = None
    horario = HorariosOcupados.objects.get(id=pk)
    if horario.efectiva == 'N':
        id = Consultas.objects.filter(id_medico = horario.id_medico).aggregate(Max('id'))
        if not id['id__max'] or id['id__max'] is None:
            id = 1
        else:
            id = id['id__max'] + 1
        horario.efectiva = 'S'
        horario.save()
        consulta = Consultas()
        consulta.id_medico = horario.id_medico
        consulta.id_horario = horario
        consulta.fecha = horario.fecha
        consulta.id_paciente = horario.id_paciente
        consulta.usuario_crea = user
        consulta.fec_crea = datetime.datetime.now()
        consulta.id = id
        consulta.save(force_insert=True)
        consulta_recover = consulta
    else:
        consulta_recover = Consultas.objects.get(id_horario = horario, id_medico = horario.id_medico, id_paciente = horario.id_paciente)
    return consulta_recover


def calculate_age(date):
    if not date:
        return 0
    today = datetime.date.today()
    if today < date:
        return 0
    year = today.year
    month = today.month
    day = today.day
    age = 0
    age = year - date.year
    if month < date.month:
        return age
    if month >= date.month and day >= date.day:
        age = age + 1
    return age


def calculate_imc(talla, peso):
    peso_kg = peso * 0.45
    return round(peso_kg / (talla * talla), 2)
