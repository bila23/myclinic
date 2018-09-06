from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.models import HorariosOcupados, Paciente, Horarios
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
        return render(request, 'consulta.html', {'day': today_string})
    except Exception as inst:
        print(inst)
        return JsonResponse({'error_msg': 'Ha ocurrido un error al momento de recuperar los pacientes de este día'}, safe=False)


@login_required
def show_today(request):
    try:
        today = datetime.datetime.today()
        medico = gf.findUser(request.user.username)
        
        horario_list = HorariosOcupados.objects.filter(id_medico = medico, fecha = today).order_by('id_horario')
        dispo_hor_list = Horarios.objects.filter(id_medico = medico).exclude(id__in = HorariosOcupados.objects.filter(id_medico = medico, fecha = today) ).order_by('inicio')
        
        data_hor_list = serializers.serialize('json', horario_list, indent=1, use_natural_foreign_keys=True, use_natural_primary_keys=True)
        data_dispo_hor = serializers.serialize('json', dispo_hor_list)
        
        data = {"horario_list": data_hor_list, "dispo_hor_list": data_dispo_hor}
        return JsonResponse(data, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse({'error_msg': 'Ha ocurrido un error al momento de recuperar los pacientes de este día'}, safe=False)


@login_required
def find_consulta(request):
    try:
        if (request.method == "POST" and request.is_ajax()):
            form = HorConsultaForm(request.POST)
            medico = gf.findUser(request.user.username)
            today = datetime.datetime.today()
            
            horario_list = HorariosOcupados.objects.filter(id_medico = medico, fecha = gf.toformat_YYYYMMDD(form.data['vdate'])).order_by('id_horario')
            dispo_hor_list = Horarios.objects.filter(id_medico = medico).exclude(id__in = HorariosOcupados.objects.filter(id_medico = medico, fecha = today) ).order_by('inicio')

            data_hor_list = serializers.serialize('json', horario_list, indent=1, use_natural_foreign_keys=True, use_natural_primary_keys=True)
            data_dispo_hor = serializers.serialize('json', dispo_hor_list)

            data = {"horario_list": data_hor_list, "dispo_hor_list": data_dispo_hor}

            return JsonResponse(data, safe=False)
    except Exception as inst:
        print(inst)
        return JsonResponse({'error_msg': 'Ha ocurrido un error al momento de recuperar los pacientes'}, safe=False)


@login_required
def nueva_cita_today(request):
    try:
        today = datetime.datetime.today()
        #RECUPERO LOS HORARIOS DISPONIBLES
        hor_list = Horarios.objects.filter(id_medico = gf.findUser(request.user.username)).exclude(id__in = HorariosOcupados.objects.filter(id_medico = gf.findUser(request.user.username), fecha = today) ).order_by('inicio')
        #RECUPERO LOS PACIENTES DEL MEDICO
        pac_list = Paciente.objects.filter(id_medico = gf.findUser(request.user.username)).order_by('nombre')
        context = {'hor_list': hor_list, 'pac_list': pac_list, 'today': today}
        return render(request, 'nueva_cita.html', context)
    except Exception as e:
        print(e)
        return render(request, 'nueva_cita.html')
