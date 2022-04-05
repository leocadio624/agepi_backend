from apps.base.api import GeneralListApiView
from apps.protocol.api.serializers.general_serializers import ProtocolStateSerializer

class ProtocolStateListAPIView(GeneralListApiView):
    serializer_class = ProtocolStateSerializer