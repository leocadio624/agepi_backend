from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response


from apps.notification.api.serializers.notificacion_serializers import NotificacionSerializer

class NotificacionViewSet(viewsets.ModelViewSet):

    serializer_class = NotificacionSerializer
    
    def get_queryset(self, pk = None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state = True)
        else:
            return self.get_serializer().Meta.model.objects.filter(id = pk, state = True).first()
    
    #get
    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)