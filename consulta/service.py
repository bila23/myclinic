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
