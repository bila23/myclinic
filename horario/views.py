from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.models import HorariosOcupados, Paciente, Horarios
from django.http import JsonResponse
import core.generalFunction as gf
from core.models import Usuario
from .forms import HorConsultaForm
from django.core import serializers
import datetime


@login_required
def home(request):
    try:
        today = gf.getToday()
        today_string = gf.dateToString(today)
        pac_list = Paciente.objects.filter(id_medico = gf.findUser(request.user.username)).order_by('nombre')
        return render(request, 'consulta.html', {'day': today_string, 'pac_list': pac_list})
    except Exception as inst:
        print(inst)
        return render(request, 'consulta.html', {'error_msg': 'Ha ocurrido un error al momento de recuperar los pacientes y/o horarios disponibles de este día'})


@login_required
def show_today(request):
    try:
        today = gf.getToday()
        medico = gf.findUser(request.user.username)
        
        horario_list = HorariosOcupados.objects.filter(id_medico = medico, fecha = today).order_by('id_horario')
        dispo_hor_list = Horarios.objects.filter(id_medico = medico).exclude(id__in = HorariosOcupados.objects.values('id_horario').filter(id_medico = medico, fecha = today) ).order_by('inicio')

        data_hor_list = serializers.serialize('json', horario_list, indent=1, use_natural_foreign_keys=True, use_natural_primary_keys=True)
        data_dispo_hor = serializers.serialize('json', dispo_hor_list)
        
        data = {"horario_list": data_hor_list, "dispo_hor_list": data_dispo_hor}
        return JsonResponse(data, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse({'error_msg': 'Ha ocurrido un error al momento de recuperar los pacientes y/o horarios disponibles de este día'}, safe=False)


@login_required
def find_consulta(request):
    try:
        if (request.method == "POST" and request.is_ajax()):
            form = HorConsultaForm(request.POST)
            medico = gf.findUser(request.user.username)
            day = form.data['vdate']
            day_format = gf.toformat_YYYYMMDD(day)
            
            horario_list = HorariosOcupados.objects.filter(id_medico = medico, fecha = day_format).order_by('id_horario')
            dispo_hor_list = Horarios.objects.filter(id_medico = medico).exclude(id__in = HorariosOcupados.objects.values('id_horario').filter(id_medico = medico, fecha = day_format) ).order_by('inicio')

            data_hor_list = serializers.serialize('json', horario_list, indent=1, use_natural_foreign_keys=True, use_natural_primary_keys=True)
            data_dispo_hor = serializers.serialize('json', dispo_hor_list)

            data = {"horario_list": data_hor_list, "dispo_hor_list": data_dispo_hor}

            return JsonResponse(data, safe=False)
    except Exception as inst:
        print(inst)
        return JsonResponse({'error_msg': 'Ha ocurrido un error al momento de recuperar los pacientes y/o los horarios disponibles'}, safe=False)


@login_required
def save_pac_hor(request):
    try:
        if (request.method == "POST" and request.is_ajax()):
            id_hor = request.POST.get('id_hor')
            id_pac = request.POST.get('id_pac')
            vdate = request.POST.get('vdate')

            day_format = gf.toformat_YYYYMMDD(vdate)
            day = datetime.datetime.strptime(vdate, '%d/%m/%Y')
            medico = gf.findUser(request.user.username)

            model = HorariosOcupados()
            model.id_horario = Horarios.objects.get(id = id_hor)
            model.id_paciente = Paciente.objects.get(id = id_pac)
            model.id_medico = medico
            model.fecha = day
            model.usuario_crea = request.user.username
            model.fec_crea = datetime.datetime.now()
            model.efectiva = 'N'
            model.save()

            horario_list = HorariosOcupados.objects.filter(id_medico = medico, fecha = day_format).order_by('id_horario')
            dispo_hor_list = Horarios.objects.filter(id_medico = medico).exclude(id__in = HorariosOcupados.objects.values('id_horario').filter(id_medico = medico, fecha = day_format) ).order_by('inicio')

            data_hor_list = serializers.serialize('json', horario_list, indent=1, use_natural_foreign_keys=True, use_natural_primary_keys=True)
            data_dispo_hor = serializers.serialize('json', dispo_hor_list)

            data = {"horario_list": data_hor_list, "dispo_hor_list": data_dispo_hor, "msg": 'Se ha reservado el cupo correctamente', 'type': 'success'}

            return JsonResponse(data, safe=False)
    except Exception as inst:
        print(inst)
        return JsonResponse({'msg': 'Ha ocurrido un error al tratar de reservar el cupo', 'type': 'error'}, safe=False)
