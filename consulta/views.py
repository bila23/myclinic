from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import core.generalFunction as gf
from django.core import serializers
from core.models import HorariosOcupados
from .forms import ExpedienteForm
import datetime
import logging

log = logging.getLogger(__name__)


@login_required
def home(request):
    try:
        pk = request.GET.get('pk')
        form = ExpedienteForm()
        if not pk:
            return render(request, 'expediente.html', {'msg': 'Ha ocurrido un error', 'type': 'error'})
        horario = gf.paciente_horario(pk)
        return render(request, 'expediente.html', {'horario': horario, 'form': form})
    except Exception as inst:
        log.error(inst)
        return render(request, 'expediente.html', {'msg': 'Ha ocurrido un error inesperado', 'type': 'error'})
