from apps.team.models import Team
from rest_framework import serializers


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        exclude = ('state', 'created_date', 'modified_date', 'deleted_date')



    def validate_fk_user(self, value):
        teams = Team.objects.filter(fk_user = value.id, state = True)
        if teams:
            raise serializers.ValidationError('Este usuario ya ha creado un equipo');

        return value


    def validate(self, data):
        return data
    


    def to_representation(self, instance):
        return {
            'id':instance.id,
            'fk_user':instance.fk_user.id,
            'nombre':instance.nombre,
            'created_date':instance.created_date

        }
    
