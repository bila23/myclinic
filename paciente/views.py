from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from core.models import Paciente
from .forms import PacienteForm
import core.generalFunction as gf
from django.core import serializers
import logging
from django.utils import timezone

log = logging.getLogger(__name__)

@login_required
def paciente_home(request):
    try:
        pac_list = Paciente.objects.filter(id_medico = gf.findUser(request.user.username)).order_by('nombre')
        return render(request, 'paciente.html', {'pac_list': pac_list})
    except Exception as inst:
        log.error(inst)
        return render(request, 'paciente.html')

@login_required
def find_paciente_by_key(request):
    try:
        if (request.method == "POST" and request.is_ajax()):
            id_pac = request.POST.get('name_pac')
            paciente_list = Paciente.objects.filter(nombre = id_pac, id_medico = gf.findUser(request.user.username))
            data = serializers.serialize('json', paciente_list)
            return JsonResponse({"paciente": data}, safe=False)
    except Exception as inst:
        log.error(inst)
        return JsonResponse({'msg': 'Ha ocurrido un error al recuperar el paciente que selecciono', 'type': 'error'}, safe=False)

@login_required
def save_paciente(request):
    try:
        if (request.method == "POST" and request.is_ajax()):
            user = request.user.username
            model = PacienteForm(request.POST)
            paciente = model.save(commit = False)
            fecha_nac = request.POST.get('fecha_nac')
            paciente.id_medico = gf.findUser(user)
            paciente.fecha_nac = gf.toformat_YYYYMMDD(fecha_nac)
            paciente.usuario_crea = user
            paciente.fec_crea = timezone.now()
            paciente.save()
            return JsonResponse({'msg': 'Se ha guardado correctamente el paciente', 'type': 'success'}, safe=False)
    except Exception as inst:
        log.error(inst)
        return JsonResponse({'msg': 'Ha ocurrido un error al tratar de guardar el paciente', 'type': 'error'}, safe=False)
