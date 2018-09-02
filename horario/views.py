from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.models import HorariosOcupados
from django.http import JsonResponse
import core.generalFunction as gf
import datetime
from .forms import HorConsultaForm

@login_required
def home(request):
    try:
        today = datetime.datetime.today()
        today_string = ''
        if(today.day < 10):
            today_string = '0' + str(today.day)
        else:
            today_string = str(today.day)
        if(today.month < 10):
            today_string = today_string + '/0' + str(today.month)
        else:
            today_string = today_string + '/' + str(today.month)
        
        today_string = today_string + '/' + str(today.year)

        horario_list = HorariosOcupados(id_medico = gf.findUser(request.user.username), fecha = today)
        if not horario_list:
            print('la lista esta vacia')
        context = {'horario_list': horario_list, 'day': today_string}
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
            horario_list = HorariosOcupados(id_medico = gf.findUser(request.user.username), fecha = form.date)
            data = {'horario_list': horario_list}
            return JsonResponse(data, safe=False)
    except Exception as inst:
        print(inst)
        return render(request, 'consulta.html',{
            'error_msg': 'Ha ocurrido un error al momento de recuperar los pacientes'
        })

