from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from apps.protocol.api.serializers.catalogos_serializers import PeriodoSerializer, InscripccionSerializer
from apps.protocol.models import catInscripccion

class PeriodoViewSet(viewsets.ModelViewSet):
    serializer_class = PeriodoSerializer

    def get_queryset(self, pk = None):        
        return self.get_serializer().Meta.model.objects.all().order_by('-created_date')
        

    def list(self, request):
        periodos_serializer = self.get_serializer(self.get_queryset(), many = True)
        inscripccion_serializer = InscripccionSerializer(catInscripccion.objects.all(), many = True)
        

        return Response({
            'periodos':periodos_serializer.data,
            'inscripcciones':inscripccion_serializer.data
            },status = status.HTTP_200_OK)

    #post
    def create(self, request):
        
        anio = request.data['anio']
        periodo = request.data['periodo']

        periodos = self.get_serializer().Meta.model.objects.filter(anio = anio, periodo = periodo, state = True)
        if  periodos:
            return Response({'message':'Solo puede existir un período habilitado por semestre'}, status = status.HTTP_400_BAD_REQUEST)
        
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Se ha creado del registro del período'}, status = status.HTTP_200_OK)
        return Response({'message':'Ocurrió una interrupción, favor de reintentar la operación.'}, status = status.HTTP_400_BAD_REQUEST)

    #delete
    def destroy(self, request, pk = None):
        protocol = self.get_queryset().filter(id = pk).first()
        if protocol:
            protocol.state = False
            protocol.save()
            return Response({'message':'Se ha inhabilitado el período correctamente'}, status = status.HTTP_200_OK)
        return Response({'message':'No existe un periodo con estos datos'}, status = status.HTTP_400_BAD_REQUEST)


class InscripccionViewSet(viewsets.ModelViewSet):
    serializer_class = InscripccionSerializer

    #post
    def create(self, request):
        pk      = request.data['id']
        state  = request.data['state']

        inscripccion = self.get_serializer().Meta.model.objects.filter(id = pk).first()
        inscripccion.state = state
        inscripccion.save()

        inscripccion_serializer = self.get_serializer(catInscripccion.objects.all(), many = True)
        message = 'Inscripcción habilitada' if state else 'Inscripcción deshabilitada'

        
        return Response(
                {
                'message'        : message,
                'inscripcciones' : inscripccion_serializer.data
                }
                , status = status.HTTP_200_OK)
