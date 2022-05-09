import pytz
from django.utils import timezone

from rest_framework import serializers
from apps.firma.models import Firma, FirmaProtocolo
from datetime import datetime, timedelta, date
#from dateutil.relativedelta import relativedelta


class FirmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firma
        exclude = ('state', 'created_date', 'modified_date', 'deleted_date')


    def convertUTC(self, date):
        fmt = '%d/%m/%Y %H:%M'
        utc = date.replace(tzinfo=pytz.UTC)
        localtz = utc.astimezone(timezone.get_current_timezone())
        return localtz.strftime('%m/%d/%Y %H:%M:%S')


    def validate(self, data):
        return data
    
    def to_representation(self, instance):
        
        created_date = self.convertUTC(instance.created_date)
        modified_date = self.convertUTC(instance.modified_date)
        modified_date = '' if created_date == modified_date else modified_date

        


        time_created = created_date.split(' ')
        vigencia_firma = instance.vigencia_firma.strftime('%m/%d/%Y') +' '+time_created[1]
        
        
        return {
            'id':instance.id,
            #'fk_user':instance.fk_user.id,
            'ruta_public_key':instance.ruta_public_key,
            'ruta_private_key':instance.ruta_private_key,
            'created_date':created_date,
            'vigencia_firma':vigencia_firma,
            'cancel_date':modified_date,
            'state':instance.state
        }


class FirmaProtocoloSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirmaProtocolo
        exclude = ('state', 'created_date', 'modified_date', 'deleted_date')

    def to_representation(self, instance):
        
        return {
            'id':instance.id,
            'fk_protocol':instance.fk_protocol.id,
            'fk_user':instance.fk_user.id,
            'firma':instance.firma,
            'state':instance.state
        }