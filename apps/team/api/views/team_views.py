from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from apps.team.api.serializers.team_serializers import TeamSerializer

class TeamViewSet(viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    
    """
    """
    def get_queryset(self, pk = None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state = True)
        else:
            return self.get_serializer().Meta.model.objects.filter(id = pk, state = True).first()

    #post
    def create(self, request):

        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            return Response({'message':'mensaje generico'}, status = status.HTTP_200_OK)
        return Response({'message':'Ya haz creado un equipo'}, status = status.HTTP_400_BAD_REQUEST)        

        """
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message':'Se ha creado el equipo correctamente',
                'team':serializer.data
                }, status = status.HTTP_200_OK)

        return Response({'message':'Ya haz creado un equipo'}, status = status.HTTP_400_BAD_REQUEST)
        """



        """
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Equipo creado'}, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        """

        return Response({'message':'mensaje de pruebas'}, status = status.HTTP_200_OK)

    #post
    def update(self, request, pk = None):
        if self.get_queryset(pk):
            protocol_serializer = self.serializer_class(self.get_queryset(pk), data = request.data)
            if protocol_serializer.is_valid():
                protocol_serializer.save()
                return Response(protocol_serializer.data, status = status.HTTP_200_OK)
            return Response(protocol_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    #delete
    def destroy(self, request, pk = None):
        protocol = self.get_queryset().filter(id = pk).first()
        if protocol:
            protocol.state = False
            protocol.save()
            return Response({'message':'Se ha eliminado el protocolo correctamente'}, status = status.HTTP_200_OK)
        return Response({'message':'No existe un protocolo con estos datos'}, status = status.HTTP_400_BAD_REQUEST)


class teamListViewSet(viewsets.ModelViewSet):
    serializer_class = TeamSerializer

    def get_queryset(self, id):
        return self.get_serializer().Meta.model.objects.filter(fk_user = id, state = True)

    def list(self, request):
        pk_user = request.GET["pk_user"]
        print(pk_user)
        serializer = self.get_serializer(self.get_queryset(pk_user), many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

"""
"""