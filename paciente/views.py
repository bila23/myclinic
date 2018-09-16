from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from core.models import Paciente
import core.generalFunction as gf
from django.core import serializers
import logging

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
            paciente = Paciente.objects.get(nombre = id_pac)
            data = serializers.serialize('json', [paciente, ])
            return JsonResponse({"paciente": data}, safe=False)
    except Exception as inst:
        log.error(inst)
        return JsonResponse({'msg': 'Ha ocurrido un error al recuperar el paciente que selecciono', 'type': 'error'}, safe=False)
