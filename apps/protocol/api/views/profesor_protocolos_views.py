from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response


from apps.protocol.api.serializers.protocol_serializers import ProtocolSelectSerializer
from apps.comunidad.api.serializers.comunidad_serializers import ProfesorSerializer
from apps.protocol.api.serializers.protocol_serializers import AsignacionProtocoloSerializer
from apps.team.api.serializers.team_serializers import TeamMemberSerializer



class protocolsProfesorInit(viewsets.ModelViewSet):
    serializer_class = ProtocolSelectSerializer

    def get_estados(self, pk = None):
        return ProtocolStateSerializer.Meta.model.objects.all()

    def get_queryset(self, pk = None):
        equipos = TeamMemberSerializer.Meta.model.objects.filter(fk_user = pk, solicitudEquipo = 2, state = True).values('fk_team')
        profesor = ProfesorSerializer.Meta.model.objects.filter(fk_user = pk, state = True).first()
        academia = profesor.fk_academia.id
        lista_protocols = AsignacionProtocoloSerializer.Meta.model.objects.filter(fk_academia = academia, state = True).values('fk_protocol')
        return self.get_serializer().Meta.model.objects.filter(id__in = lista_protocols, fk_protocol_state__in = [5,6], state = True).exclude(fk_team__in = equipos)

    def list(self, request):
        pk_user = request.GET['pk_user']
        protocol_serializer = self.get_serializer(self.get_queryset(pk_user), many = True)
        return Response(protocol_serializer.data,status = status.HTTP_200_OK)

