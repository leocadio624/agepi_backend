from rest_framework import serializers
from apps.notification.models import Notificacion



class NotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        exclude = ('state', 'created_date', 'modified_date', 'deleted_date')

    def validate(self, data):
        return data
    


    def to_representation(self, instance):

        return {
        'id':instance.id,
        'fk_user_origen':fk_userOrigen.id,
        'fk_user_destino':instance.fk_userDestino,
        'fk_tipoNotificacion':instance.fk_tipoNotificacion.id
        }
