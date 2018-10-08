from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import core.generalFunction as gf
from django.core import serializers
from django.db.models import Max
from core.models import Consultas, Referencias
from .forms import ExpedienteForm
import consulta.service as service
import logging

log = logging.getLogger(__name__)

@login_required
def home(request):
    try:
        pk = request.GET.get('pk')
        if not pk:
            return render(request, 'expediente.html', {'msg': 'Ha ocurrido un error al tratar de recuperar el expediente del paciente', 'type': 'error'})
        consulta_recover = service.recover_consulta(pk, request.user.username)
        return render(request, 'expediente.html', {'consulta': consulta_recover})
    except Exception as inst:
        log.error(inst)
        return render(request, 'expediente.html', {'msg': 'Ha ocurrido un error inesperado', 'type': 'error'})

@login_required
def update(request, pk):
    try:
        if (request.method == "POST" and request.is_ajax()):
            consulta = get_object_or_404(Consultas, id_medico=gf.findUser(request.user.username), id=pk)
            form = ExpedienteForm(request.POST, instance=consulta)
            if form.is_valid():
                consulta = form.save(commit=False)
                if consulta.id_paciente.fecha_nac:
                    consulta.edad_paciente = service.calculate_age(consulta.id_paciente.fecha_nac)
                if consulta.talla and consulta.peso:
                    consulta.imc = service.calculate_imc(consulta.talla, consulta.peso)
                consulta.save()
            else:
                log.error(form.errors)
                return JsonResponse({'msg': 'Existe un campo que posee un valor incorrecto<br>' + str(form.errors), 'type': 'error'})
            return JsonResponse({'msg': 'Se ha guardado correctamente la consulta', 'type': 'success'})
    except Exception as inst:
        log.error(inst)
        return JsonResponse({'msg': 'Ha ocurrido un error al tratar de guardar la consulta', 'type': 'error'})

@login_required
def find_ref(request, pk):
    try:
        if(request.method == 'POST' and request.is_ajax()):
            data = service.find_ref_query(pk, gf.findUser(request.user.username))
            return JsonResponse({'ref_list': data, 'type': 'success'})
    except Exception as inst:
        log.error(inst)
        return JsonResponse({'msg': 'Ha ocurrido un error al momento de recuperar las referencias m&eacute;dicas', 'type': 'error'})

@login_required
def save_ref(request):
    try:
        esp = request.POST.get('esp')
        med = request.POST.get('med')
        pro = request.POST.get('pro')
        ana = request.POST.get('ana')
        id = request.POST.get('id')
        service.save_ref(esp, med, pro, ana, id, gf.findUser(request.user.username))
        data = service.find_ref_query(id, gf.findUser(request.user.username), request.user.username)
        return JsonResponse({'ref_list': data, 'type': 'success', 'msg': 'Se ha guardado correctamente la referencia'})
    except Exception as inst:
        log.error(inst)
        return JsonResponse({'msg': 'Ha ocurrido un error al momento de guardar la referencia m&eacute;dica', 'type': 'error'})
