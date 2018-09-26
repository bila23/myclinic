from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import core.generalFunction as gf
from django.core import serializers
from django.db.models import Max
from core.models import HorariosOcupados, Consultas
from .forms import ExpedienteForm
import datetime
import logging

log = logging.getLogger(__name__)

@login_required
def home(request):
    try:
        pk = request.GET.get('pk')
        form = ExpedienteForm()
        if not pk:
            return render(request, 'expediente.html', {'msg': 'Ha ocurrido un error al tratar de recuperar el expediente del paciente', 'type': 'error'})
        consulta_recover = None
        horario = gf.paciente_horario(pk)
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
            consulta.usuario_crea = request.user.username
            consulta.fec_crea = datetime.datetime.now()
            consulta.id = id
            consulta.save(force_insert=True)
            consulta_recover = consulta
        else:
            consulta_recover = Consultas.objects.get(id_horario = horario, id_medico = horario.id_medico, id_paciente = horario.id_paciente)
        return render(request, 'expediente.html', {'horario': horario, 'form': form, 'consulta': consulta_recover})
    except Exception as inst:
        log.error(inst)
        return render(request, 'expediente.html', {'msg': 'Ha ocurrido un error inesperado', 'type': 'error'})

@login_required
def save(request):
    try:
        if (request.method == "POST" and request.is_ajax()):
            model = ExpedienteForm(request.POST)
            print(model.data['id_int'])
            print(model.data['id_horario'])
            print(model.data['id_paciente'])
            #consultas.save()
            return JsonResponse({'msg': 'Se ha guardado correctamente la consulta', 'type': 'success'})
    except Exception as inst:
        log.error(inst)
        return JsonResponse({'msg': 'Ha ocurrido un error al tratar de guardar la consulta', 'type': 'error'})
