from apps.team.models import Team
from rest_framework import serializers

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        exclude = ('state', 'created_date', 'modified_date', 'deleted_date')


    def to_representation(self, instance):
        print(instance.pk_user)
        return {
            'id':instance.id,
            'nombre':instance.nombre,
            'state':instance.state, 
            'created_date':instance.created_date
        
        }
    
