from apps.protocol.models import Protocol
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
            'protocol_state':instance.protocol_state.description if instance.protocol_state is not None else ''
        }


