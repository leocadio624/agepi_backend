from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from apps.comunidad.api.serializers.comunidad_serializers import AlumnoSerializer, ProgramaAcademicoSerializer, ProfesorSerializer


class ComunidadViewSet(viewsets.ModelViewSet):
    serializer_class = AlumnoSerializer
    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(state = True)
        

    def queryProfesor(self):
        return ProfesorSerializer.Meta.model.objects.filter(state = True)
        

    def list(self, request):
        serializerAlumno = self.get_serializer(self.get_queryset(), many = True)
        serializerProfesor = ProfesorSerializer(self.queryProfesor(), many = True)


        return Response(
            {
            'alumnos'    :serializerAlumno.data,
            'profesores'  :serializerProfesor.data
            },
            status = status.HTTP_200_OK)


class ProgramaAcedemicoViewSet(viewsets.ModelViewSet):
    serializer_class = ProgramaAcademicoSerializer

    def get_queryset(self, pk = None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.all()
        else:
            return self.get_serializer().Meta.model.objects.filter(id = pk).first()
    
    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)


class AlumnoViewSet(viewsets.ModelViewSet):
    serializer_class = AlumnoSerializer

    def get_queryset(self, pk = None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state = True)
        else:
            return self.get_serializer().Meta.model.objects.filter(id = pk, state = True).first()
    
    
    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many = True)
        return Response({'alumnos':serializer.data}, status = status.HTTP_200_OK)

    
    def create(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message'   : 'Se ha cargado el alumno correctamente',
                'alumno'    : serializer.data
                },status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk = None):

        if self.get_queryset(pk):
            serializer = self.serializer_class(self.get_queryset(pk), data = request.data)

            if  serializer.is_valid():
                serializer.save()
                return Response({   
                    'message':'Se ha actualizado el alumno correctamente',
                    'alumno':serializer.data
                }, status = status.HTTP_200_OK)
            return Response(protocol_serializer.errors, status = status.HTTP_400_BAD_REQUEST)



    def destroy(self, request, pk = None):
        alumno = self.get_queryset().filter(id = pk).first()
        if  alumno:
            alumno.state = False
            alumno.save()
            return Response({'message':'Se ha eliminado el alumno correctamente'}, status = status.HTTP_200_OK)
        return Response({'message':'No existe un protocolo con estos datos'}, status = status.HTTP_400_BAD_REQUEST)
