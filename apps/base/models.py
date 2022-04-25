from django.db import models
from pytz import timezone


class BaseModel(models.Model):
    id = models.AutoField(primary_key = True)
    state = models.BooleanField('Estado', default = True)
    #created_date = models.DateField('Fecha de creacion', auto_now = False, auto_now_add = True)
    #created_date = models.DateTimeField('Fecha de creacion', auto_now = False, auto_now_add = True, default = timezone('America/Mexico_City') )
    created_date = models.DateTimeField('Fecha de creacion', default = timezone('America/Mexico_City') )
    
    
    



    modified_date = models.DateField('Fecha de modificacion', auto_now = True, auto_now_add = False)
    deleted_date = models.DateField('Fecha de eliminacion', auto_now = True, auto_now_add =False)

    class Meta:
        abstract = True
        verbose_name = 'Modelo Base'
        verbose_name_plural = 'Modelos Base'

