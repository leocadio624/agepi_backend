from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from apps.team.api.serializers.team_serializers import TeamSerializer, TeamSerializerUpd, TeamMemberSerializer, AlumnoTeamSerializer, ProfesorTeamSerializer
from apps.notification.api.serializers.notificacion_serializers import NotificacionTeamSerializer

from apps.team.models import TeamMembers, Team
from apps.notification.models import NotificacionTeam

    

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

        al_disponibles = []
        objects = TeamMembers.objects.filter(state = True, solicitudEquipo = 2).values('fk_user').exclude(fk_user = pk_user)


        for i in objects:
            al_disponibles.append(i['fk_user'])
        al_disponibles.append( pk_user )

        
        return self.get_serializer().Meta.model.objects.filter(alta_app = True, fk_programa = programa, state = True).exclude(fk_user__in = al_disponibles)

    
    
    def queryProfesor(self):
        return ProfesorTeamSerializer.Meta.model.objects.filter(alta_app = True, state = True)

    def queryTeam(self, id):
        return TeamSerializer.Meta.model.objects.filter(fk_user = id, state = True)


    def list(self, request):    

        pk_user = request.GET["pk_user"]
        serial_team = TeamSerializer(self.queryTeam(pk_user), many = True)


        alumno = self.get_serializer().Meta.model.objects.filter(fk_user = pk_user, state = True).first()
        programa = alumno.fk_programa.id

        serial_al = self.get_serializer(self.get_queryset(pk_user, programa), many = True)
        serial_prof = ProfesorTeamSerializer(self.queryProfesor(), many = True)

        team = TeamMembers.objects.filter(fk_user = pk_user, solicitudEquipo = 2, state = True).first()
        solicitudes = []

        if  team:
            fk_team = team.fk_team.id
            solicitudes = self.getSolicitudes(fk_team)

        return Response({
                'teams' : serial_team.data,
                'alumnos' : serial_al.data,
                'profesores' : serial_prof.data,
                'solicitudes' : solicitudes
            }, status = status.HTTP_200_OK)

    
    
    """
    def create(self, request):

        id = request.data['id']
        fk_user = request.data['fk_user']
        
        

        notificacion_serilizer   = NotificacionSerializer(data = {'fk_userOrigen':id, 'fk_userDestino':fk_user, 'fk_tipoNotificacion':1})
        print( notificacion_serilizer.is_valid() )

        return Response({
            'message' : 'mensaje generico'
            }, status = status.HTTP_200_OK)
    """

        
    def create(self, request):

        id = request.data['id']
        fk_user = request.data['fk_user']
        

        team = TeamMembers.objects.filter(state = True, fk_user = id).values('fk_team').first()
        if team is None:
            return Response({'message' : 'Para enviar una solicitud de equipo debe crear ó pertenecer a un equipo'}, status = status.HTTP_206_PARTIAL_CONTENT)
        
        fk_team = team['fk_team']


        serializer_member   = TeamMemberSerializer(data = {'fk_team':fk_team, 'fk_user':fk_user, 'solicitudEquipo':1})
        if serializer_member.is_valid():
            serializer_member.save()

            notificacion_serilizer   = NotificacionTeamSerializer(data = {'fk_userOrigen':id, 'fk_userDestino':serializer_member.data['id'], 'fk_tipoNotificacion':1})
            if  notificacion_serilizer.is_valid():
                notificacion_serilizer.save()


        solicitudes = []
        solicitudes = self.getSolicitudes(fk_team)

        return Response({
            'message' : 'Se ha enviado la solicitud de equipo correctamente',
            'solicitudes' : solicitudes
            }, status = status.HTTP_200_OK)


    def destroy(self, request, pk = None):
    
        solicitud = TeamMembers.objects.filter(state = True, fk_user = pk, solicitudEquipo = 1).first()

        if  solicitud is None:
            return Response({'message' : 'No se encontró una solicitud con estos datos'}, status = status.HTTP_206_PARTIAL_CONTENT)





        """
        """
        solicitud.state = False
        solicitud.solicitudEquipo = 3
        solicitud.save()

        notificacion = NotificacionTeam.objects.filter(state = True, fk_userDestino = solicitud.id).first()
        notificacion.state = False
        notificacion.save()

        

        solicitudes = []
        solicitudes = self.getSolicitudes(solicitud.fk_team.id)

        return Response({
                    'message':'Se ha cancelado la solicitud de equipo correctamente',
                    'solicitudes':solicitudes
                }, status = status.HTTP_200_OK)


        


        return Response({'message':'Mensaje generico'}, status = status.HTTP_200_OK)

        """
        protocol = self.get_queryset().filter(id = pk).first()
        if protocol:
            protocol.state = False
            protocol.save()
            return Response({'message':'Se ha eliminado el equipo correctamente'}, status = status.HTTP_200_OK)
        return Response({'message':'No existe un equipo con estos datos'}, status = status.HTTP_400_BAD_REQUEST)
        """



    def getSolicitudes(self, fk_team):
        solicitudes = []
        objects = TeamMembers.objects.filter(fk_team = fk_team, solicitudEquipo = 1, state = True).values('fk_user');
        for i in objects:
            solicitudes.append(i['fk_user'])

        return solicitudes
        
