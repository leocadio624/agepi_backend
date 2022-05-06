import pytz
from django.utils import timezone

from rest_framework import serializers
from apps.notification.models import NotificacionTeam
from apps.users.models import User
from apps.team.models import TeamMembers
from apps.protocol.models import Protocol



class NotificacionTeamSerializer(serializers.ModelSerializer):
	class Meta:
		model = NotificacionTeam
		exclude = ('state', 'created_date', 'modified_date', 'deleted_date')

	def convertUTC(self, date):
		fmt = '%d/%m/%Y %H:%M'
		utc = date.replace(tzinfo=pytz.UTC)
		localtz = utc.astimezone(timezone.get_current_timezone())
		return localtz.strftime('%m/%d/%Y %H:%M:%S')

	def validate(self, data):
		return data

		
	def to_representation(self, instance):
		
		fk_origen = instance.fk_userOrigen.id
		fk_destino = instance.fk_userDestino

		usuario_origen = User.objects.filter(id = fk_origen).first()
		usuario_destino = User.objects.filter(id = fk_origen).first()

		

		str_salida = ''
		if instance.fk_tipoNotificacion.id == 1:
			str_salida = str(usuario_origen.name) +' '+str(usuario_origen.last_name) + ' te ha invitado a unirte a su equipo.'
		elif instance.fk_tipoNotificacion.id == 2:
			str_salida = str(usuario_origen.name) +' '+str(usuario_origen.last_name) + ' se ha unido a tú equipo.'
		elif instance.fk_tipoNotificacion.id == 3:
			str_salida = str(usuario_origen.name) +' '+str(usuario_origen.last_name) + ' ha rechazado tú solicitud de equipo,'
		elif instance.fk_tipoNotificacion.id == 4:
			fk_team = instance.fk_userDestino.fk_team
			protocol = Protocol.objects.filter(fk_team = fk_team, state = True).first()
			str_salida = 'Tienes el protocolo con número: '+protocol.number+' y título \"'+protocol.title+'\" pendiente por firmar.'

		
		created_date = self.convertUTC(instance.created_date)
		return {
		'id':instance.id,
		'user_origen': str(usuario_origen.name) +' '+str(usuario_origen.last_name),
		'fk_user_origen':fk_origen,
		'fk_user_destino':fk_destino.id,	
		'fk_tipoNotificacion':instance.fk_tipoNotificacion.id,
		'notificacion':instance.fk_tipoNotificacion.descp,
		'str_salida':str_salida,
		'fecha':created_date,
		'state':instance.state
		}


class SolicitudFirmaSerializer(serializers.ModelSerializer):
	class Meta:
		model = NotificacionTeam
		exclude = ('state', 'created_date', 'modified_date', 'deleted_date')

	def convertUTC(self, date):
		fmt = '%d/%m/%Y %H:%M'
		utc = date.replace(tzinfo=pytz.UTC)
		localtz = utc.astimezone(timezone.get_current_timezone())
		return localtz.strftime('%m/%d/%Y %H:%M:%S')

	def validate(self, data):
		return data

		
	def to_representation(self, instance):
		
		fk_origen = instance.fk_userOrigen.id
		fk_destino = instance.fk_userDestino

		usuario_origen = User.objects.filter(id = fk_origen).first()
		usuario_destino = User.objects.filter(id = fk_origen).first()

		
		fk_team = instance.fk_userDestino.fk_team
		protocol = Protocol.objects.filter(fk_team = fk_team, state = True).first()

		
		#'fileProtocol': protocol.fileProtocol.url if protocol.fileProtocol != '' else '',

		
		created_date = self.convertUTC(instance.created_date)
		return {
		'id':instance.id,
		'user_origen': str(usuario_origen.name) +' '+str(usuario_origen.last_name),
		'fk_user_origen':fk_origen,
		'fk_user_destino':fk_destino.id,	
		'fk_tipoNotificacion':instance.fk_tipoNotificacion.id,
		'notificacion':instance.fk_tipoNotificacion.descp,
		'path_protocol':protocol.fileProtocol.url if protocol.fileProtocol != '' else '',
		'numero':protocol.number,
		'titulo':protocol.title,
		'periodo':str(protocol.fk_periodo.anio)+'-'+str(protocol.fk_periodo.periodo),
		'fecha':created_date,
		'state':instance.state
		}


class TeamMembersSerializer(serializers.ModelSerializer):
	class Meta:
		model = TeamMembers
		exclude = ('state', 'created_date', 'modified_date', 'deleted_date')

	def validate(self, data):
		return data

		
	def to_representation(self, instance):
		return {
		'id'   				:instance.id,
		'fk_team'  			:instance.fk_team,
		'fk_user'  			:instance.fk_user,
		'solicitudEquipo' 	:instance.solicitudEquipo
		}

