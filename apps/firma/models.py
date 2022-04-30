from django.db import models
from simple_history.models import HistoricalRecords
from apps.base.models import BaseModel
from apps.users.models import User



class Firma(BaseModel):

    fk_user             = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = 'pk de usuario', null = False, blank = False)
    password_firma      = models.CharField('Password de firma', max_length = 50, blank = False, null = False)
    ruta_public_key     = models.CharField('Llave publica de certificado', max_length = 250, blank = False, null = False )
    ruta_private_key    = models.CharField('Llave privada de certificado', max_length = 250, blank = False, null = False)
    vigencia_firma      = models.DateField(blank=True, null = True)
    historical          = HistoricalRecords()

    @property
    def _history_user(self):
        return self.change_by
    
    @_history_user.setter
    def _history_user(self, vale):
        self.changed_by = value

    class Meta:
        verbose_name = 'Firma'
        verbose_name_plural = 'Firmas'

    def __str__(self):
        return f'{self.fk_user}'

    """
    """