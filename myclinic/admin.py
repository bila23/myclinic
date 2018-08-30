from django.contrib import admin
from core.models import AuditoriaInout
from core.models import Consultas
from core.models import ConsultasDiag
from core.models import ConsultasMed
from core.models import ContadorConsultas
from core.models import ContadoresMedicos
from core.models import Diagnosticos
from core.models import EspecialidadesMedicas
from core.models import Examenes
from core.models import ExamenesDiag
from core.models import Horarios
from core.models import HorariosOcupados
from core.models import Medicamentos
from core.models import MedicoEspecialidad
from core.models import Paciente
from core.models import Referencias
from core.models import Roles
from core.models import TipoDiag
from core.models import TipoExamenes
from core.models import Usuario
from core.models import UsuarioErrores
from core.models import UsuarioOlvidaPwd
from core.models import UsuarioPagos

admin.site.register(AuditoriaInout)
admin.site.register(Consultas)
admin.site.register(ConsultasDiag)
admin.site.register(ConsultasMed)
admin.site.register(ContadorConsultas)
admin.site.register(ContadoresMedicos)
admin.site.register(Diagnosticos)
admin.site.register(EspecialidadesMedicas)
admin.site.register(Examenes)
admin.site.register(ExamenesDiag)
admin.site.register(Horarios)
admin.site.register(HorariosOcupados)
admin.site.register(Medicamentos)
admin.site.register(MedicoEspecialidad)
admin.site.register(Paciente)
admin.site.register(Referencias)
admin.site.register(Roles)
admin.site.register(TipoDiag)
admin.site.register(TipoExamenes)
admin.site.register(Usuario)
admin.site.register(UsuarioErrores)
admin.site.register(UsuarioOlvidaPwd)
admin.site.register(UsuarioPagos)