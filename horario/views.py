from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.models import HorariosOcupados
from django.http import JsonResponse
import core.generalFunction as gf
from core.models import Usuario
import datetime
from .forms import HorConsultaForm
from django.core import serializers
from django.http import HttpResponse

@login_required
def home(request):
    try:
        today = datetime.datetime.today()
        today_string = gf.dateToString(today)
        return render(request, 'consulta.html', {'day': today_string})
    except Exception as inst:
        print(inst)
        return render(request, 'consulta.html',{
            'error_msg': 'Ha ocurrido un error al momento de recuperar los pacientes de este día'
        })


@login_required
def show_today(request):
    try:
        today = datetime.datetime.today()
        horario_list = HorariosOcupados.objects.filter(id_medico = gf.findUser(request.user.username), fecha = today)
        data = serializers.serialize('json', horario_list)
        return JsonResponse(data, safe=False)
    except Exception as inst:
        print (inst)


@login_required
def find_consulta(request):
    try:
        if (request.method == "POST" and request.is_ajax()):
            form = HorConsultaForm(request.POST)
            horario_list = HorariosOcupados.objects.filter(id_medico = gf.findUser(request.user.username), fecha = gf.toformat_YYYYMMDD(form.data['vdate']))
            data = serializers.serialize('json', horario_list, indent=1, use_natural_foreign_keys=True, use_natural_primary_keys=True)
            return JsonResponse(data, safe=False)
            #return HttpResponse(horario_list)
    except Exception as inst:
        print(inst)
        return JsonResponse({'msg': 'Ha ocurrido un error al momento de recuperar los pacientes'}, safe=False)
