import os
import datetime
from django.db import models
from simple_history.models import HistoricalRecords
from apps.base.models import BaseModel
from apps.team.models import Team
from apps.comunidad.models import Academia


class catInscripccion(BaseModel):
    id = models.IntegerField(primary_key = True)
    descp = models.CharField('catalogo inscripccion', max_length = 50, blank = False, null = False)
    historical = HistoricalRecords()


    @property
    def _history_user(self):
        return self.change_by

    @_history_user.setter
    def _history_user(self, vale):
        self.changed_by = value

    class Meta:
        verbose_name = 'inscripccion'
        verbose_name_plural = 'inscripcciones'

    def __str__(self):
        return self.descp



class PeriodoEscolar(BaseModel):
    periodo = models.IntegerField('periodo', blank = False, null = False)
    anio = models.IntegerField('anio', blank = False, null = False)
    descp = models.CharField('Descripccion', max_length = 50, blank = False, null = False)
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.change_by
    
    @_history_user.setter
    def _history_user(self, vale):
        self.changed_by = value

    class Meta:
        verbose_name = 'Periodo escolar'
        verbose_name_plural = 'Periodos escolares'

    def __str__(self):
        return self.descp


class ProtocolState(BaseModel):
    protocol_state = models.IntegerField('Estado protocolo', default = True)
    description = models.CharField('Descripccion del estado', max_length = 50, blank = False, null = False, unique = True)
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.change_by
    
    @_history_user.setter
    def _history_user(self, vale):
        self.changed_by = value

    class Meta:
        verbose_name = 'Estado de protocolo'
        verbose_name_plural = 'Estado de protocolos'

    def __str__(self):
        return self.description

#periodo = models.IntegerField('periodo', blank = False, null = False)
#anio = models.IntegerField('anio', blank = False, null = False)

def user_directory_path(instance, filename):
    return os.path.join(
        'protocols',
        str(instance.fk_periodo.anio),
        str(instance.fk_periodo.anio)+'-'+str(instance.fk_periodo.periodo),
        instance.number,
        datetime.datetime.now().strftime('%Y_%m_%d__%H_%M'), 
        filename)


class Protocol(BaseModel):

    number            = models.CharField('Numero de protocolo', max_length = 10, blank = False, null = False, unique = True)
    title             = models.CharField('Titulo de protocolo', max_length = 150, blank = False, null = False)
    sumary            = models.TextField('Resumen de protocolo', blank = False, null = True)
    fileProtocol      = models.FileField('Archivo de protocolo', upload_to = user_directory_path, null = True, blank = True)
    fk_protocol_state = models.ForeignKey(ProtocolState, on_delete = models.CASCADE, verbose_name = 'Estado del prtocolo', null = True, blank = False)
    fk_periodo        = models.ForeignKey(PeriodoEscolar, on_delete = models.CASCADE, verbose_name = 'Perido de inscripccion', null = True, blank = False)
    fk_inscripccion   = models.ForeignKey(catInscripccion, on_delete = models.CASCADE, verbose_name = 'Perido de inscripccion', null = True, blank = False)
    fk_team           = models.ForeignKey(Team, on_delete = models.CASCADE, verbose_name = 'Equipo de protocolo', null = True, blank = False)
    
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.change_by
    
    @_history_user.setter
    def _history_user(self, vale):
        self.changed_by = value

    class Meta:
        verbose_name = 'Protocolo'
        verbose_name_plural = 'Protocolos'


class keyWord(BaseModel):

    word = models.CharField('Palabra clave', max_length = 50, blank = False, null = False, unique = False)
    fk_Protocol = models.ForeignKey(Protocol, on_delete = models.CASCADE, verbose_name = 'pk de prtocolo', null = True, blank = False)
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.change_by
    
    @_history_user.setter
    def _history_user(self, vale):
        self.changed_by = value

    class Meta:
        verbose_name = 'Palabra clave'
        verbose_name_plural = 'Palabras clave'


class AsignacionProtocolo(BaseModel):
    fk_protocol = models.ForeignKey(Protocol, on_delete = models.CASCADE, verbose_name = 'fk_protocol', null = True, blank = False)
    fk_academia = models.ForeignKey(Academia, on_delete = models.CASCADE, verbose_name = 'fk_academia', null = True, blank = False)
        
    historical = HistoricalRecords()
    @property
    def _history_user(self):
        return self.change_by
    
    @_history_user.setter
    def _history_user(self, vale):
        self.changed_by = value

    class Meta:
        verbose_name = 'Asignacion'
        verbose_name_plural = 'Asignaciones'


