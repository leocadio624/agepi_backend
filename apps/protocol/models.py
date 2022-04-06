import os
import datetime
from django.db import models
from simple_history.models import HistoricalRecords
from apps.base.models import BaseModel

#blank=False, null=False, unique=True

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


def user_directory_path(instance, filename):
    return os.path.join(
        'protocols',
        instance.number,
        datetime.datetime.now().strftime('%Y_%m_%d__%H_%M'), 
        filename)


class Protocol(BaseModel):

    number = models.CharField('Numero de protocolo', max_length = 10, blank = False, null = False, unique = True)
    title = models.CharField('Titulo de protocolo', max_length = 150, blank = False, null = False)
    sumary = models.TextField('Resumen de protocolo', blank = False, null = True)
    protocol_state = models.ForeignKey(ProtocolState, on_delete = models.CASCADE, verbose_name = 'Estado del prtocolo', null = True, blank = False)
    fileProtocol = models.FileField('Archivo de protocolo', upload_to = user_directory_path, null = True, blank = True)
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


