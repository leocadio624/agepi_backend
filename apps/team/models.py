from django.db import models
from simple_history.models import HistoricalRecords
from apps.base.models import BaseModel
from apps.users.models import User

class Team(BaseModel):

    nombre  = models.CharField('Nombre equipo', max_length = 10, blank = False, null = False, unique = False)
    historical = HistoricalRecords()
    

    @property
    def _history_user(self):
        return self.change_by
    
    @_history_user.setter
    def _history_user(self, vale):
        self.changed_by = value

    class Meta:
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'