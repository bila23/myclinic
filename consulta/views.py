from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import core.generalFunction as gf
from django.core import serializers
from django.db.models import Max
from core.models import Consultas, Referencias, ConsultasMed
from .forms import ExpedienteForm
import consulta.service as service
import logging
from django.db import connection

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
        service.save_ref(esp, med, pro, ana, id, gf.findUser(request.user.username), request.user.username)
        data = service.find_ref_query(id, gf.findUser(request.user.username))
        return JsonResponse({'ref_list': data, 'type': 'success', 'msg': 'Se ha guardado correctamente la referencia'})
    except Exception as inst:
        log.error(inst)
        return JsonResponse({'msg': 'Ha ocurrido un error al momento de guardar la referencia m&eacute;dica', 'type': 'error'})

@login_required
def delete_ref(request):
    try:
        id_ref = request.POST.get('id_ref')
        id_consulta = request.POST.get('id_consulta')
        model = get_object_or_404(Referencias, id = id_ref)
        model.delete()
        data = service.find_ref_query(id_consulta, gf.findUser(request.user.username))
        return JsonResponse({'ref_list': data, 'type': 'success', 'msg': 'Se ha eliminado correctamente la referencia'})
    except Exception as inst:
        log.error(inst)
        return JsonResponse({'type': 'error', 'msg': 'Ha ocurrido un error al tratar de eliminar la referencia'})

@login_required
def get_by_key(request):
    try:
        if(request.method == 'POST' and request.is_ajax()):
            pk = request.POST.get('pk')
            model = get_object_or_404(Referencias, id = pk)
            array_result = serializers.serialize('json', [model], ensure_ascii = False)
            obj = array_result[1:-1]
            return JsonResponse({'ref_single': obj, 'type': 'success'})
    except Exception as inst:
        log.error(inst)
        return JsonResponse({'type': 'error', 'msg': 'Ha ocurrido un error al tratar de recuperar la referencia que desea modificar'})

@login_required
def update_ref(request):
    try:
        if(request.method == 'POST' and request.is_ajax()):
            id_ref = request.POST.get('id_ref')
            model = get_object_or_404(Referencias, id = id_ref)
            model.problema_ref = request.POST.get('pro')
            model.analisis_ref = request.POST.get('ana')
            model.medico_ref = request.POST.get('med')
            model.especialidad_ref = request.POST.get('esp')
            model.save()
            data = service.find_ref_query(model.id_consulta, gf.findUser(request.user.username))
            return JsonResponse({'ref_list': data, 'type':'success', 'msg': 'Se ha actualizado correctamente la referencia'})
    except Exception as inst:
        log.error(inst)
        return JsonResponse({'type': 'error', 'msg': 'Ha ocurrido un error al tratar de actualizar la referencia'})

@login_required
def find_med(request, pk):
    try:
        if(request.method == 'POST' and request.is_ajax()):
            med_list = service.find_med_query(pk, gf.findUser(request.user.username))
            return JsonResponse({'med_list': med_list, 'type': 'success'})
    except Exception as inst:
        log.error(inst)
        return JsonResponse({'type': 'error', 'msg': 'Ha ocurrido un error al tratar de recuperar los medicamentos otorgados'})

@login_required
def save_med(request):
    try:
        if(request.method == 'POST' and request.is_ajax()):
            user = request.user.username
            id_doctor = gf.findUser(user)
            pk = request.POST.get('id_consulta')
            service.save_med(request.POST.get('nom'), request.POST.get('can'), request.POST.get('fus'), id_doctor, user, pk)
            med_list = service.find_med_query(pk, id_doctor)
            return JsonResponse({'med_list': med_list, 'type': 'success', 'msg': 'Se ha guardado correctamente el medicamento'})
    except Exception as inst:
        log.error(inst)
        return JsonResponse({'type': 'error', 'msg': 'Ha ocurrido un error al tratar de guardar un medicamento'})

@login_required
def delete_med(request):
    try:
        if(request.method == 'POST' and request.is_ajax()):
            model = get_object_or_404(ConsultasMed, id = request.POST.get('id_med'))
            pk = model.id_consulta
            model.delete()
            med_list = service.find_med_query(pk, gf.findUser(request.user.username))
            return JsonResponse({'med_list': med_list, 'type': 'success', 'msg': 'Se ha eliminado correctamente el medicamento'})
    except Exception as inst:
        log.error(inst)
        return JsonResponse({'type': 'error', 'msg': 'Ha ocurrido un error al tratar de eliminar el medicamento'})

@login_required
def get_by_key_med(request):
    try:
        if(request.method == 'POST' and request.is_ajax()):
            pk = request.POST.get('pk')
            model = get_object_or_404(ConsultasMed, id = pk)
            array_result = serializers.serialize('json', [model], ensure_ascii = False)
            obj = array_result[1:-1]
            return JsonResponse({'ref_single': obj, 'type': 'success'})
    except Exception as inst:
        log.error(inst)
        return JsonResponse({'type': 'error', 'msg': 'Ha ocurrido un error al tratar de recuperar el medicamento que desea modificar'})

@login_required
def update_med(request):
    try:
        if(request.method == 'POST' and request.is_ajax()):
            model = get_object_or_404(ConsultasMed, id = request.POST.get('id_med'))
            model.nombre_medicamento = request.POST.get('nom')
            model.cantidad = request.POST.get('can')
            model.forma_uso = request.POST.get('fum')
            model.save(force_update=True)
            med_list = service.find_med_query(model.id_consulta, gf.findUser(request.user.username))
            return JsonResponse({'med_list': med_list, 'type': 'success', 'msg': 'Se ha actualizado correctamente el medicamento'})
    except Exception as inst:
        log.error(inst)
        return JsonResponse({'type': 'error', 'msg': 'Ha ocurrido un error al momento de actualizar el medicamento'})
