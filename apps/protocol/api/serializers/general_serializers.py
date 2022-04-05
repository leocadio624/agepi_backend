from apps.protocol.models import ProtocolState
from rest_framework import serializers

class ProtocolStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProtocolState
        #fields = '__all__'
        #exclude = ('state',)
        fields = ('id','protocol_state','description',)
