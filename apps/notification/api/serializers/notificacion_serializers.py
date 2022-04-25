from rest_framework import serializers
from apps.notification.models import Notificacion
from apps.users.models import User



class NotificacionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Notificacion
		exclude = ('state', 'created_date', 'modified_date', 'deleted_date')

	def validate(self, data):
		return data

		
	def to_representation(self, instance):
		
		fk_origen = instance.fk_userOrigen.id
		fk_destino = instance.fk_userDestino

		usuario_origen = User.objects.filter(id = fk_origen).first()
		usuario_destino = User.objects.filter(id = fk_origen).first()

		
		str_salida = ''
		if instance.fk_tipoNotificacion.id == 1:
			str_salida = str(usuario_origen.name) +' '+str(usuario_origen.last_name) + ' te ha invitado a unirte a su equipo'

		created_date = instance.created_date.strftime("%d/%m/%y %H:%M:%S")
		
		
		return {
		'id':instance.id,
		'fk_user_origen':fk_origen,
		'fk_user_destino':fk_destino,	
		'fk_tipoNotificacion':instance.fk_tipoNotificacion.id,
		'notificacion':instance.fk_tipoNotificacion.descp,
		'str_salida':str_salida,
		'fecha':created_date
		}
