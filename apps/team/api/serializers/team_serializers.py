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

        integrantes = len( TeamMembers.objects.filter(fk_team = instance.id, state = True, solicitudEquipo = 2) )
        created_date = instance.created_date.strftime("%d/%m/%y %H:%M:%S")
        
        return {
            'id':instance.id,
            'fk_user':instance.fk_user.id,
            'nombre':instance.nombre,
            'created_date':created_date,
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
            'fk_team':instance.fk_team.id,
            'team':instance.fk_team.nombre,
            'fk_user':instance.fk_user.id,
            'fk_user_creator':instance.fk_team.fk_user.id,
            'name':instance.fk_user.name,
            'email':instance.fk_user.email,
            'professionalSummary':instance.fk_user.professionalSummary,
            'last_name':instance.fk_user.last_name,
            'fecha_integracion':instance.created_date
        }

class TeamMemberDictamenSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMembers
        exclude = ('state', 'created_date', 'modified_date', 'deleted_date')



    def to_representation(self, instance):
        return {
            'email':instance.fk_user.email,
            'name':instance.fk_user.name,
            'last_name':instance.fk_user.last_name
        }






"""
* Descripcion:  Lista los alumnos disponibles para integrarce a un equipo 
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
            'pk_user':instance.fk_user,
            'name':instance_user.name,
            'last_name':instance_user.last_name,
            'fk_programa':instance.fk_programa.id,
            'programa':instance.fk_programa.programa,
            'email':instance.email,
            'boleta':instance.boleta
        }

"""
* Descripcion:  Lista los profesores disponibles para integrarce a un equipo 
* en modulo registro equipo
* Fecha de la creacion:     22/04/2022
* Author:                   Eduardo B 
"""
class ProfesorTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesor
        exclude = ('state', 'created_date', 'modified_date', 'deleted_date')


    
    def to_representation(self, instance):

        num_equipos = len( TeamMembers.objects.filter(fk_user = instance.fk_user, state = True, solicitudEquipo = 2) )
        disponible = 0 if num_equipos == 6 else 1

        instance_user = User.objects.filter(id = instance.fk_user).first()

        return {
            'disponible':disponible,
            'pk_user':instance.fk_user,
            'name':instance_user.name,
            'last_name':instance_user.last_name,
            'fk_academia':instance.fk_academia.id,
            'academia':instance.fk_academia.academia,
            'email':instance.email,
            'noEmpleado':instance.noEmpleado
        }

    
