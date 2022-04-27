from django.db import models
from simple_history.models import HistoricalRecords
from apps.base.models import BaseModel
from apps.users.models import User
from apps.team.models import TeamMembers



class TipoNotificacion(models.Model):
	id = models.IntegerField(primary_key = True)
	descp = models.CharField('Descripccion de la notificacion', max_length = 255, blank = False, null = False, unique = False)
	historical = HistoricalRecords()


	@property
	def _history_user(self):
	    return self.change_by

	@_history_user.setter
	def _history_user(self, vale):
	    self.changed_by = value

	class Meta:
		verbose_name = 'Tipo de notificacion'
		verbose_name_plural = 'Tipo de notificaciones'

	def __str__(self):
		return f'{self.id} {self.descp}'



class NotificacionTeam(BaseModel):
	fk_userOrigen 	= models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = 'pk de usuario que genera notificacion', null = False, blank = False)
	#fk_userDestino 	= models.IntegerField(default = 0, null = False, blank = False)
	fk_userDestino 	= models.ForeignKey(TeamMembers, on_delete = models.CASCADE, verbose_name = 'Relacion de miembro de equipo a relacionar', null = False, blank = False)
	fk_tipoNotificacion = models.ForeignKey(TipoNotificacion, on_delete = models.CASCADE, verbose_name = 'pk tipo de notificacion', null = False, blank = False)
		

	@property
	def _history_user(self):
	    return self.change_by

	@_history_user.setter
	def _history_user(self, vale):
	    self.changed_by = value

	class Meta:
	    verbose_name = 'Notificacion equipo'
	    verbose_name_plural = 'Notificaciones equipo'

	def __str__(self):
		return f'{self.id} {self.fk_userOrigen} {self.fk_userDestino}'