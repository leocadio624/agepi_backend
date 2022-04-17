from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from apps.team.api.serializers.team_serializers import TeamSerializer, TeamSerializerUpd, TeamMemberSerializer

class TeamViewSet(viewsets.ModelViewSet):
    serializer_class    = TeamSerializer
    serializer_upd      = TeamSerializerUpd
    

    
    def get_queryset(self, pk = None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state = True)
        else:
            return self.get_serializer().Meta.model.objects.filter(id = pk, state = True).first()

    #post
    def create(self, request):


        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            serializer.save()

            fk_team = serializer.data['id']
            fk_user = request.data['fk_user']

            serializer_member   = TeamMemberSerializer(data = {'fk_team':fk_team, 'fk_user':fk_user})

            if serializer_member.is_valid():
                print( serializer_member.is_valid() )
                serializer_member.save()
            else:
                print(serializer.errors)


            return Response({
                'message':'Se ha creado el equipo correctamente',
                'team':serializer.data
                }, status = status.HTTP_200_OK)

        return Response({'message':'Ya haz creado un equipo'}, status = status.HTTP_400_BAD_REQUEST)
        


    def update(self, request, pk = None):
        
        if self.get_queryset(pk):
            serializer = self.serializer_upd(self.get_queryset(pk), data = request.data)

            if  serializer.is_valid():
                serializer.save()
                return Response(
                    {
                    'message'   : 'Se ha actualizado el equipo correctamente',
                    'team'      : serializer.data
                    },
                    status = status.HTTP_200_OK)
        return Response({'message':'No existe un equipo con estos datos'}, status = status.HTTP_400_BAD_REQUEST)
    
    #delete
    def destroy(self, request, pk = None):
        protocol = self.get_queryset().filter(id = pk).first()
        if protocol:
            protocol.state = False
            protocol.save()
            return Response({'message':'Se ha eliminado el equipo correctamente'}, status = status.HTTP_200_OK)
        return Response({'message':'No existe un equipo con estos datos'}, status = status.HTTP_400_BAD_REQUEST)


class teamListViewSet(viewsets.ModelViewSet):
    serializer_class = TeamSerializer

    def get_queryset(self, id):
        return self.get_serializer().Meta.model.objects.filter(fk_user = id, state = True)

    def list(self, request):

        pk_user = request.GET["pk_user"]
        serializer = self.get_serializer(self.get_queryset(pk_user), many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
