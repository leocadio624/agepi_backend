from apps.team.models import Team, TeamMembers
from rest_framework import serializers
from apps.comunidad.models import Alumno, Profesor
from apps.users.models import User


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

        integrantes = len( TeamMembers.objects.filter(fk_team = instance.id, state = True) )
        return {
            'id':instance.id,
            'fk_user':instance.fk_user.id,
            'nombre':instance.nombre,
            'created_date':instance.created_date,
            'integrantes': integrantes

        }
        
class TeamSerializerUpd(serializers.ModelSerializer):
    class Meta:
        model = Team
        exclude = ('state', 'created_date', 'modified_date', 'deleted_date')


class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMembers
        exclude = ('state', 'created_date', 'modified_date', 'deleted_date')


    def to_representation(self, instance):
        return {
            'id':instance.id,
            'fk_team':instance.fk_user.id,
            'fk_user':instance.fk_user.id,
            'fecha_integracion':instance.created_date

        }

"""
* Descripcion:  Lista los usuarios disponibles para integrarce a un equipo 
* en modulo registro equipo
* Fecha de la creacion:     22/04/2022
* Author:                   Eduardo B 
"""
class AlumnoTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumno
        exclude = ('state', 'created_date', 'modified_date', 'deleted_date')


    
    def to_representation(self, instance):

        instance_user = User.objects.filter(id = instance.fk_user).first()
        return {
            #'id':instance.id,
            'pk_user':instance.fk_user,
            'name':instance_user.name,
            'last_name':instance_user.last_name,
            'fk_programa':instance.fk_programa.id,
            'programa':instance.fk_programa.programa,
            'email':instance.email,
            'boleta':instance.boleta

        }

    
