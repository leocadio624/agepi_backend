import pytz
from django.utils import timezone

from apps.protocol.models import Protocol, keyWord, AsignacionProtocolo, SelectProtocolo, Evaluacion, Pregunta
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
            'creacion':self.convertUTC(instance.created_date)
            
        }


class ProtocolSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Protocol
        exclude = ('state', 'created_date', 'modified_date', 'deleted_date')

    def to_representation(self, instance):

        select = SelectProtocolo.objects.filter(fk_protocol = instance.id, state = True).values('fk_user')
        lista_prof = []
        for i in select:lista_prof.append(i['fk_user'])
            

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
            'fk_protocol_state':instance.fk_protocol_state.id,
            'num_select': len(select),
            'lista_prof': lista_prof
            
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
        

class AsignacionProtocoloSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AsignacionProtocolo
        exclude = ('state', 'created_date', 'modified_date', 'deleted_date')

    def to_representation(self, instance):
        return {
            'id':instance.id,
            'fk_protocol':instance.fk_protocol,
            'fk_academia':instance.fk_academia
        }

class SelectProtocoloSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SelectProtocolo
        exclude = ('state', 'created_date', 'modified_date', 'deleted_date')

    def to_representation(self, instance):
        return {
            'id':instance.id,
            'fk_protocol':instance.fk_protocol,
            'fk_user':instance.fk_user
        }

class SelectProtocoloLineSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SelectProtocolo
        exclude = ('state', 'created_date', 'modified_date', 'deleted_date')


    def convertUTC(self, date):
        fmt = '%d/%m/%Y %H:%M'
        utc = date.replace(tzinfo=pytz.UTC)
        localtz = utc.astimezone(timezone.get_current_timezone())
        return localtz.strftime('%m/%d/%Y %H:%M:%S')

    def to_representation(self, instance):
        evaluado         = 0
        fecha_evaluacion = ''

        evaluacion = Evaluacion.objects.filter(fk_seleccion = instance.id).first()
        if  evaluacion:
            fecha_evaluacion = self.convertUTC(evaluacion.created_date)
            evaluado = 1
    
        return {
            'id':instance.id,
            'fk_user':instance.fk_user.id,
            'name':instance.fk_user.name+' '+instance.fk_user.last_name,
            #'last_name':instance.fk_user.last_name,
            'created_date':self.convertUTC(instance.created_date),
            'evaluado':evaluado,
            'fecha_evaluacion':fecha_evaluacion
        }


class EvaluacionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Evaluacion
        exclude = ('state', 'created_date', 'modified_date', 'deleted_date')

    def to_representation(self, instance):
        return {
            'id':instance.id,
            'fk_seleccion':instance.fk_seleccion.id,
            'observacion_general':instance.observacion_general,
            'dictamen':instance.dictamen,
            'version':instance.version
        }

class PreguntaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Pregunta
        exclude = ('state', 'created_date', 'modified_date', 'deleted_date')

    def to_representation(self, instance):
        return {
            'id':instance.id,
            'fk_evaluacion':instance.fk_evaluacion.id,
            'numPregunta':instance.numPregunta,
            'estado':instance.estado,
            'observacion':instance.observacion
        }



