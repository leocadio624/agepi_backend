from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from apps.protocol.api.serializers.protocol_serializers import ProtocolLineaSerializer
from apps.team.api.serializers.team_serializers import TeamMemberSerializer
from apps.firma.api.serializers.firma_serializers import FirmaProtocoloLineaSerializer



class LineProtocolStartViewSet(viewsets.ModelViewSet):
	serializer_class = ProtocolLineaSerializer
	
	def list(self, request):

		pk_user = request.GET["pk_user"]
		team = TeamMemberSerializer.Meta.model.objects.filter(fk_user = pk_user, solicitudEquipo = 2, state = True).first()

		if team is None:
			return Response([], status = status.HTTP_200_OK)	
		
		fk_team = team.fk_team.id
		protocol_serializer = ProtocolLineaSerializer(ProtocolLineaSerializer.Meta.model.objects.filter(fk_team = fk_team, state = True), many = True)

		return Response(protocol_serializer.data, status = status.HTTP_200_OK)

class getIntegrantesViewSet(viewsets.ModelViewSet):

	def getIntegrantes(self, fk_team):
		return TeamMemberSerializer.Meta.model.objects.filter(fk_team = fk_team, solicitudEquipo = 2, state = True)

	
	def list(self, request):
		fk_team = request.GET["fk_team"]
		integrantes_serializer = TeamMemberSerializer(self.getIntegrantes(fk_team), many = True) 
		return Response(integrantes_serializer.data, status = status.HTTP_200_OK)


class getFirmasViewSet(viewsets.ModelViewSet):

	def getFirmas(self, fk_protocol):
		return FirmaProtocoloLineaSerializer.Meta.model.objects.filter(fk_protocol = fk_protocol, state = True)

	def list(self, request):
		fk_protocol = request.GET["fk_protocol"]
		firmas_serializer = FirmaProtocoloLineaSerializer(self.getFirmas(fk_protocol), many = True) 
		return Response(firmas_serializer.data, status = status.HTTP_200_OK)