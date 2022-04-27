from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from apps.notification.api.serializers.notificacion_serializers import NotificacionTeamSerializer
from apps.team.models import TeamMembers, Team

class NotificacionViewSet(viewsets.ModelViewSet):
    serializer_class = NotificacionTeamSerializer
    
    def get_queryset(self, pk = None):

        
        objects = TeamMembers.objects.filter(state = True, fk_user = pk).values('id')
        print(objects)
        return self.get_serializer().Meta.model.objects.filter(fk_userDestino__in = objects).order_by('-created_date')
        

    def list(self, request):
    	
    	pk_user = request.GET["pk_user"]

    	serializer = self.get_serializer(self.get_queryset(pk_user), many = True)
    	return Response({'notificaciones':serializer.data}, status = status.HTTP_200_OK)


    def create(self, request):

        id_notificacion = request.data['id_notificacion']
        fk_user = request.data['id_user']
        fk_user_origen = request.data['fk_user_origen']
        id_teamMember = request.data['id_teamMember']

        team = TeamMembers.objects.filter(fk_user = fk_user, state = True, solicitudEquipo = 2).first()
        if  team:
            #aqui se inhabilita la notificacion
            notificacion = self.get_serializer().Meta.model.objects.filter(id = id_notificacion).first()
            notificacion.state = False
            notificacion.save()
            return Response({'team':team.fk_team.nombre}, status = status.HTTP_226_IM_USED)


        team_member = TeamMembers.objects.filter(id = id_teamMember, state = True, solicitudEquipo = 1).first()
        if  team_member:
            team_member.solicitudEquipo = 2
            team_member.save()

            #Cambia de estado la notificacion entrante
            notificacion = self.get_serializer().Meta.model.objects.filter(id = id_notificacion).first()
            notificacion.state = False
            notificacion.save()

            
            #Obtiene pk de equipo para genrar notificacion de vuelta
            team = TeamMembers.objects.filter(fk_user = fk_user_origen, state = True, solicitudEquipo = 2).first()
            notificacion_serilizer   = NotificacionTeamSerializer(data = {'fk_userOrigen':fk_user, 'fk_userDestino':team.id, 'fk_tipoNotificacion':2})
            if  notificacion_serilizer.is_valid():
                notificacion_serilizer.save()
            
            return Response({'team':team_member.fk_team.nombre}, status = status.HTTP_200_OK)
        return Response({'message':'Ocurrio un error en la integracion al equipo'}, status = status.HTTP_400_BAD_REQUEST)


        

    """

    serializer_class = keyWordSerializer
    def get_queryset(self, pk = None):
        
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state = True)
        else:            
            return self.get_serializer().Meta.model.objects.filter(id = pk, state = True).first()  


    def list(self, request):
        keyWord_serializer = self.get_serializer(self.get_queryset(), many = True)
        return Response(keyWord_serializer.data, status = status.HTTP_200_OK)


    def create(self, request):
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk = None):
        keyWord = self.get_queryset().filter(id = pk).first()

        if keyWord:
            keyWord.state = False
            keyWord.save()
            return Response(
                {
                'pk' : keyWord.id,
                'fk_protocol' : keyWord.fk_Protocol.id
                },
                status = status.HTTP_200_OK)
        return Response({'message':'No existe un protocolo con estos datos'}, status = status.HTTP_400_BAD_REQUEST)
    """
