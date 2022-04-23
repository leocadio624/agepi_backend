from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from apps.team.api.serializers.team_serializers import TeamSerializer, TeamSerializerUpd, TeamMemberSerializer, AlumnoTeamSerializer
from apps.team.models import TeamMembers, Team

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

            serializer_member   = TeamMemberSerializer(data = {'fk_team':fk_team, 'fk_user':fk_user, 'solicitudEquipo':2})
            if serializer_member.is_valid():
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

"""
* Descripcion:  Viewset de los usuarios disponibles para integrarce a un equipo 
* en modulo registro equipo
* Fecha de la creacion:     22/04/2022
* Author:                   Eduardo B 
"""
class AlumnoTeamViewSet(viewsets.ModelViewSet):
    serializer_class = AlumnoTeamSerializer


    def get_queryset(self, pk_user, programa):

        objects = TeamMembers.objects.filter(state = True, solicitudEquipo = 2).values('fk_user').exclude(fk_user = pk_user)
        al_disponibles = []
        for i in objects:
            al_disponibles.append(i['fk_user'])
        al_disponibles.append( pk_user )

        #al_disponibles = [1, 9, 20]
        #print(self.get_serializer().Meta.model.objects.filter(alta_app = True, fk_programa = programa, state = True))
        
        return self.get_serializer().Meta.model.objects.filter(alta_app = True, fk_programa = programa, state = True).exclude(fk_user__in = al_disponibles)

        



        #return  self.get_serializer().Meta.model.objects.filter(alta_app = True, fk_programa = programa, state = True).exclude(fk_user__in = al_disponibles)


    def list(self, request):
        pk_user = request.GET["pk_user"]

        alumno = self.get_serializer().Meta.model.objects.filter(fk_user = pk_user, state = True).first()
        programa = alumno.fk_programa.id
        serial_al = self.get_serializer(self.get_queryset(pk_user, programa), many = True)


        solicitudes = []

        team = TeamMembers.objects.filter(fk_user = pk_user, solicitudEquipo = 2, state = True).first()
        #fk_team = team.fk_team.id

        print(team)
        """
        if  team:
            solicitudes = self.getSolicitudes(fk_team)

            objects = TeamMembers.objects.filter(fk_team = fk_team, solicitudEquipo = 1, state = True).values('fk_user');
            for i in objects:
                solicitudes.append(i['fk_user'])
        """


        return Response({
            'alumnos' : serial_al.data,
            'solicitudes' : solicitudes
            }, status = status.HTTP_200_OK)

        

    def create(self, request):

        """
        self.mensaje('mariana angel')
        return Response({
            'message' : 'Mensaje generico'
            }, status = status.HTTP_200_OK)
        """

        

        id = request.data['id']
        fk_user = request.data['fk_user']
        

        team = TeamMembers.objects.filter(state = True, fk_user = id).values('fk_team').first()
        if team is None:
            return Response({'message' : 'Para enviar una solicitud de equipo debe crear ó pertenecer a un equipo'}, status = status.HTTP_206_PARTIAL_CONTENT)
        
        fk_team = team['fk_team']


        serializer_member   = TeamMemberSerializer(data = {'fk_team':fk_team, 'fk_user':fk_user, 'solicitudEquipo':1})
        if serializer_member.is_valid():
            serializer_member.save()

        solicitudes = []
        solicitudes = self.getSolicitudes(fk_team)

        """
        objects = TeamMembers.objects.filter(fk_team = fk_team, solicitudEquipo = 1, state = True).values('fk_user');
        solicitudes = []
        for i in objects:
            solicitudes.append(i['fk_user'])
        """

        return Response({
            'message' : 'Se ha enviado la solicitud de equipo correctamente',
            'solicitudes' : solicitudes
            }, status = status.HTTP_200_OK)


    def getSolicitudes(self, fk_team):
        solicitudes = []
        objects = TeamMembers.objects.filter(fk_team = fk_team, solicitudEquipo = 1, state = True).values('fk_user');
        for i in objects:
            solicitudes.append(i['fk_user'])

        return solicitudes
        
