from django.db import models

class EspecialidadesMedicas(models.Model):
    nombre = models.CharField(max_length=300, blank=True, null=True)
    usuario_crea = models.CharField(max_length=15, blank=True, null=True)
    fec_crea = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'especialidades_medicas'

        
class Roles(models.Model):
    nombre = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roles'


class Usuario(models.Model):
    id = models.CharField(primary_key=True, max_length=15)
    pwd = models.CharField(max_length=1000)
    nombre = models.CharField(max_length=2000, blank=True, null=True)
    correo = models.CharField(max_length=40, blank=True, null=True)
    clinica = models.CharField(max_length=2000, blank=True, null=True)
    fec_creacion = models.DateTimeField(blank=True, null=True)
    id_rol = models.ForeignKey(Roles, models.DO_NOTHING, db_column='id_rol', blank=True, null=True)
    estado = models.CharField(max_length=5, blank=True, null=True)
    usuario_crea = models.CharField(max_length=15, blank=True, null=True)
    id_usuario = models.ForeignKey('self', models.DO_NOTHING, db_column='id_usuario', blank=True, null=True)
    fecha_cancelado = models.DateTimeField(blank=True, null=True)
    logo = models.CharField(max_length=45, blank=True, null=True)
    sexo = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuario'


class Medicamentos(models.Model):
    nombre_comercial = models.CharField(max_length=2000, blank=True, null=True)
    usuario_crea = models.CharField(max_length=15, blank=True, null=True)
    fec_crea = models.DateTimeField(blank=True, null=True)
    estado = models.CharField(max_length=1, blank=True, null=True)
    nombre_generico = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'medicamentos'


class MedicoEspecialidad(models.Model):
    id_especialidad = models.ForeignKey(EspecialidadesMedicas, models.DO_NOTHING, db_column='id_especialidad', primary_key=True)
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_usuario')
    usuario_crea = models.CharField(max_length=15, blank=True, null=True)
    fec_crea = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'medico_especialidad'
        unique_together = (('id_especialidad', 'id_usuario'),)

class PacienteManager(models.Manager):
    def get_by_natural_key(nombre):
        return self.get(nombre=nombre)

class Paciente(models.Model):
    objects = PacienteManager()

    nombre = models.CharField(max_length=3000, blank=True, null=True)
    fecha_nac = models.DateField(blank=True, null=True)
    sexo = models.CharField(max_length=1, blank=True, null=True)
    correo = models.CharField(max_length=30, blank=True, null=True)
    celular = models.CharField(max_length=15, blank=True, null=True)
    telefono_casa = models.CharField(max_length=15, blank=True, null=True)
    telefono_oficina = models.CharField(max_length=15, blank=True, null=True)
    aseguradora = models.CharField(max_length=100, blank=True, null=True)
    id_medico = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_medico', blank=True, null=True)
    usuario_crea = models.CharField(max_length=15, blank=True, null=True)
    fec_crea = models.DateTimeField(blank=True, null=True)
    dui = models.CharField(max_length=11, blank=True, null=True)
    direccion = models.CharField(max_length=4000, blank=True, null=True)
    estado_civil = models.CharField(max_length=1, blank=True, null=True)
    profesion = models.CharField(max_length=4000, blank=True, null=True)
    empresa = models.CharField(max_length=2000, blank=True, null=True)
    direccion_empresa = models.CharField(max_length=4000, blank=True, null=True)
    municipio = models.CharField(max_length=3, blank=True, null=True)

    def natural_key(self):
        return (self.nombre)

    class Meta:
        managed = False
        db_table = 'paciente'


class TipoDiag(models.Model):
    nombre = models.CharField(max_length=3000, blank=True, null=True)
    estado = models.CharField(max_length=1, blank=True, null=True)
    fec_crea = models.DateTimeField(blank=True, null=True)
    usuario_crea = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipo_diag'


class TipoExamenes(models.Model):
    nombre = models.CharField(max_length=3000, blank=True, null=True)
    usuario_crea = models.CharField(max_length=15, blank=True, null=True)
    fec_crea = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipo_examenes'


class AuditoriaInout(models.Model):
    usuario = models.CharField(max_length=15, blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    accion = models.CharField(max_length=2, blank=True, null=True)
    mes = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auditoria_inout'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.SmallIntegerField()
    is_active = models.SmallIntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Consultas(models.Model):
    id_medico = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_medico')
    #id = models.IntegerField()
    id_horario = models.ForeignKey('HorariosOcupados', models.DO_NOTHING, db_column='id_horario')
    id_paciente = models.ForeignKey('Paciente', models.DO_NOTHING, db_column='id_paciente')
    fecha = models.DateField()
    problema = models.CharField(max_length=5000, blank=True, null=True)
    tratamiento = models.CharField(max_length=5000, blank=True, null=True)
    recomendacion = models.CharField(max_length=5000, blank=True, null=True)
    talla = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    peso = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    presion_art = models.CharField(max_length=20, blank=True, null=True)
    imc = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    usuario_crea = models.CharField(max_length=15, blank=True, null=True)
    fec_crea = models.DateTimeField(blank=True, null=True)
    observacion_receta = models.CharField(max_length=4000, blank=True, null=True)
    edad_paciente = models.IntegerField(blank=True, null=True)
    diagnostico = models.CharField(max_length=5000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'consultas'
        unique_together = (('id_medico', 'id'),)


class ConsultasDiag(models.Model):
    id_medico = models.ForeignKey(Consultas, models.DO_NOTHING, db_column='id_medico', primary_key=True)
    id_consulta = models.IntegerField()
    id_enf = models.ForeignKey('Diagnosticos', models.DO_NOTHING, db_column='id_enf')
    usuario_crea = models.CharField(max_length=15, blank=True, null=True)
    fec_crea = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'consultas_diag'
        unique_together = (('id_medico', 'id_consulta', 'id_enf'),)


class ConsultasMed(models.Model):
    id_medico = models.ForeignKey(Consultas, models.DO_NOTHING, db_column='id_medico', primary_key=True)
    id_consulta = models.IntegerField()
    id_med = models.ForeignKey('Medicamentos', models.DO_NOTHING, db_column='id_med')
    cantidad = models.CharField(max_length=200, blank=True, null=True)
    forma_uso = models.CharField(max_length=3000, blank=True, null=True)
    usuario_crea = models.CharField(max_length=15, blank=True, null=True)
    fec_crea = models.DateTimeField(blank=True, null=True)
    casa = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'consultas_med'
        unique_together = (('id_medico', 'id_consulta', 'id_med'),)


class ContadorConsultas(models.Model):
    id_medico = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_medico', primary_key=True)
    valor = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contador_consultas'


class ContadoresMedicos(models.Model):
    tabla = models.CharField(primary_key=True, max_length=30)
    valor = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contadores_medicos'


class Diagnosticos(models.Model):
    nombre = models.CharField(max_length=3000, blank=True, null=True)
    estado = models.CharField(max_length=1, blank=True, null=True)
    id_tipo_diag = models.ForeignKey('TipoDiag', models.DO_NOTHING, db_column='id_tipo_diag', blank=True, null=True)
    usuario_crea = models.CharField(max_length=15, blank=True, null=True)
    fec_crea = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'diagnosticos'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'



class Examenes(models.Model):
    nombre = models.CharField(max_length=3000, blank=True, null=True)
    estado = models.CharField(max_length=1, blank=True, null=True)
    id_tipo_exam = models.ForeignKey('TipoExamenes', models.DO_NOTHING, db_column='id_tipo_exam', blank=True, null=True)
    usuario_crea = models.CharField(max_length=15, blank=True, null=True)
    fec_crea = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'examenes'


class ExamenesDiag(models.Model):
    id_medico = models.ForeignKey(Consultas, models.DO_NOTHING, db_column='id_medico', primary_key=True)
    id_consulta = models.IntegerField()
    id_exa = models.ForeignKey(Examenes, models.DO_NOTHING, db_column='id_exa')
    usuario_crea = models.CharField(max_length=15, blank=True, null=True)
    fec_crea = models.DateTimeField(blank=True, null=True)
    resultado = models.CharField(max_length=4000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'examenes_diag'
        unique_together = (('id_medico', 'id_consulta', 'id_exa'),)

class HorariosManager(models.Manager):
    def get_by_natural_key(self, inicio, fin):
        return self.get(inicio = inicio, fin = fin)

class Horarios(models.Model):
    objects = HorariosManager()

    dia = models.IntegerField(blank=True, null=True)
    inicio = models.TimeField(blank=True, null=True)
    fin = models.TimeField(blank=True, null=True)
    id_medico = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_medico', blank=True, null=True)
    usuario_crea = models.CharField(max_length=15, blank=True, null=True)
    fec_crea = models.DateTimeField(blank=True, null=True)

    def natural_key(self):
        return (self.inicio, self.fin)

    class Meta:
        managed = False
        db_table = 'horarios'


class HorariosOcupados(models.Model):
    id_horario = models.ForeignKey(Horarios, models.DO_NOTHING, db_column='id_horario')
    id_paciente = models.ForeignKey('Paciente', models.DO_NOTHING, db_column='id_paciente')
    id_medico = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_medico')
    fecha = models.DateField()
    usuario_crea = models.CharField(max_length=15, blank=True, null=True)
    fec_crea = models.DateTimeField(blank=True, null=True)
    efectiva = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'horarios_ocupados'



class Referencias(models.Model):
    id_medico = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_medico')
    id_consulta = models.IntegerField()
    #id = models.IntegerField(primary_key=True)
    problema_ref = models.CharField(max_length=5000, blank=True, null=True)
    analisis_ref = models.CharField(max_length=5000, blank=True, null=True)
    medico_ref = models.CharField(max_length=5000, blank=True, null=True)
    especialidad_ref = models.CharField(max_length=2000, blank=True, null=True)
    usuario_crea = models.CharField(max_length=15, blank=True, null=True)
    fec_crea = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'referencias'
        #unique_together = (('id_medico', 'id_consulta', 'id'),)


class UsuarioErrores(models.Model):
    id_usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='id_usuario', primary_key=True)
    id = models.IntegerField()
    descripcion = models.CharField(max_length=4000, blank=True, null=True)
    fec_crea = models.DateTimeField(blank=True, null=True)
    pantalla = models.CharField(max_length=1000, blank=True, null=True)
    estado = models.CharField(max_length=1, blank=True, null=True)
    usuario_resuelve = models.CharField(max_length=15, blank=True, null=True)
    solucion = models.CharField(max_length=4000, blank=True, null=True)
    fec_resuelve = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuario_errores'
        unique_together = (('id_usuario', 'id'),)


class UsuarioOlvidaPwd(models.Model):
    id_usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='id_usuario', primary_key=True)
    id = models.IntegerField()
    fecha = models.DateTimeField(blank=True, null=True)
    cont_pivote = models.CharField(max_length=45, blank=True, null=True)
    estado = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuario_olvida_pwd'
        unique_together = (('id_usuario', 'id'),)


class UsuarioPagos(models.Model):
    id_usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='id_usuario', primary_key=True)
    mes = models.IntegerField()
    anio = models.IntegerField()
    fecha = models.DateTimeField(blank=True, null=True)
    dia_prog = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuario_pagos'
        unique_together = (('id_usuario', 'mes', 'anio'),)
