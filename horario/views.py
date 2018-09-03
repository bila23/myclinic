from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.models import HorariosOcupados
from django.http import JsonResponse
import core.generalFunction as gf
from core.models import Usuario
import datetime
from .forms import HorConsultaForm
from django.core import serializers

@login_required
def home(request):
    try:
        today = datetime.datetime.today()
        today_string = gf.dateToString(today)
        horario_list = HorariosOcupados.objects.filter(id_medico = gf.findUser(request.user.username), fecha = today)
        form = HorConsultaForm
        context = {'horario_list': horario_list, 'day': today_string, 'form': form}
        return render(request, 'consulta.html', context)
    except Exception as inst:
        print(inst)
        return render(request, 'consulta.html',{
            'error_msg': 'Ha ocurrido un error al momento de recuperar los pacientes de este día'
        })

@login_required
def find_consulta(request):
    try:
        if (request.method == "POST" and request.is_ajax()):
            form = HorConsultaForm(request.POST)
            horario_list = HorariosOcupados.objects.filter(id_medico = gf.findUser(request.user.username), fecha = gf.toformat_YYYYMMDD(form.data['vdate']))
            data = serializers.serialize('json', horario_list)
            return JsonResponse(data, safe=False)
    except Exception as inst:
        print(inst)
        return JsonResponse({'msg': 'Ha ocurrido un error al momento de recuperar los pacientes'}, safe=False)
