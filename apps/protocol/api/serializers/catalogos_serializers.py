import pytz
from django.utils import timezone
from rest_framework import serializers
#from apps.team.models import Team, TeamMembers
#from apps.comunidad.models import Alumno, Profesor
#from apps.users.models import User
from apps.protocol.models import PeriodoEscolar, catInscripccion


class PeriodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodoEscolar
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
        periodo = str(instance.anio) + '-' + str(instance.periodo)

        
        descp = instance.descp+ ' del ' +str(instance.anio)

        return {
            'id':instance.id,
            'periodo':periodo,
            'descp':descp,
            'created_date':created_date,
            'deleted_date':modified_date,
            'state':instance.state
        }

class PeriodoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodoEscolar
        exclude = ('state', 'created_date', 'modified_date', 'deleted_date')


    def to_representation(self, instance):
        periodo = str(instance.anio) + '-' + str(instance.periodo)        
        
        return {
            'id':instance.id,
            'periodo':periodo
        }


class InscripccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = catInscripccion
        fields = '__all__'
        
    def to_representation(self, instance):


        return {
            'id':instance.id,
            'descp':instance.descp,
            'state':instance.state
        }



