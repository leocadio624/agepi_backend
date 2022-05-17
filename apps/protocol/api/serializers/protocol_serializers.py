import pytz
from django.utils import timezone

from apps.protocol.models import Protocol, keyWord
from rest_framework import serializers

class ProtocolSerializer(serializers.ModelSerializer):
    #protocol_state = serializers.StringRelatedField()
    class Meta:
        model = Protocol
        exclude = ('state', 'created_date', 'modified_date', 'deleted_date')

    def to_representation(self, instance):
        return {
            'id':instance.id,
            'number':instance.number,
            'title':instance.title,
            'sumary':instance.sumary,
            'estado':instance.fk_protocol_state.description,
            'fk_periodo':instance.fk_periodo.id,
            'periodo':str(instance.fk_periodo.anio)+'-'+str(instance.fk_periodo.periodo),
            'fk_inscripccion':instance.fk_inscripccion.id,
            'fk_team':instance.fk_team.id,
            'fileProtocol': instance.fileProtocol.url if instance.fileProtocol != '' else '',
            'fk_protocol_state':instance.fk_protocol_state.id
            #'protocol_state':instance.protocol_state.description if instance.protocol_state is not None else ''
        }


class ProtocolLineaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Protocol
        exclude = ('state', 'created_date', 'modified_date', 'deleted_date')

    def convertUTC(self, date):
        fmt = '%d/%m/%Y %H:%M'
        utc = date.replace(tzinfo=pytz.UTC)
        localtz = utc.astimezone(timezone.get_current_timezone())
        return localtz.strftime('%m/%d/%Y %H:%M:%S')


    def to_representation(self, instance):

        return {
            'id':instance.id,
            'number':instance.number,
            'fk_team':instance.fk_team.id,
            'fk_protocol_state':instance.fk_protocol_state.id,
            'creacion':self.convertUTC(instance.modified_date)
            
        }




class keyWordSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = keyWord
        exclude = ('state', 'created_date', 'modified_date', 'deleted_date')

    def to_representation(self, instance):
        return {
            'id':instance.id,
            'word':instance.word,
            'fk_Protocol':instance.fk_Protocol.id
        }

class WordListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = keyWord
        exclude = ('state', 'created_date', 'modified_date', 'deleted_date')

    def to_representation(self, instance):
        return {
            'key':instance.word,
        }
        


