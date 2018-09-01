from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.models import HorariosOcupados

@login_required
def home(request):
    try:
        horario_list = HorariosOcupados.objects.filter(id_medico = request.user.username)
        context = {'horario_list': horario_list}
        return render(request, 'consulta.html', context)
    except Exception as inst:
        print(inst)
        return render(request, 'consulta.html',{
            'error_msg': 'Ha ocurrido un error al momento de recuperar los pacientes de este día'
        })
