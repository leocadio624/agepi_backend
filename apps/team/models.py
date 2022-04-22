from django.db import models
from simple_history.models import HistoricalRecords
from apps.base.models import BaseModel
from apps.users.models import User

class Team(BaseModel):

    nombre  = models.CharField('Nombre equipo', max_length = 50, blank = False, null = False, unique = False)
    historical = HistoricalRecords()
    fk_user = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = 'pk de usuario', null = False, blank = False)
    

    @property
    def _history_user(self):
        return self.change_by
    
    @_history_user.setter
    def _history_user(self, vale):
        self.changed_by = value

    class Meta:
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'


class TeamMembers(BaseModel):

    fk_team = models.ForeignKey(Team, on_delete = models.CASCADE, verbose_name = 'pk de equipo', null = False, blank = False)
    fk_user = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = 'pk de usuario', null = False, blank = False)
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.change_by
    
    @_history_user.setter
    def _history_user(self, vale):
        self.changed_by = value

    class Meta:
        verbose_name = 'Miembro equipo'
        verbose_name_plural = 'Miembros de equipo'


class RequestTeam(BaseModel):
    fk_team = models.ForeignKey(Team, on_delete = models.CASCADE, verbose_name = 'pk de equipo', null = False, blank = False)
    fk_user = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = 'pk de usuario', null = False, blank = False)
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.change_by
    
    @_history_user.setter
    def _history_user(self, vale):
        self.changed_by = value

    class Meta:
        verbose_name = 'Solicitud equipo'
        verbose_name_plural = 'Solicitudes de equipo'