from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from apps.comunidad.api.serializers.comunidad_serializers import AlumnoSerializer, ProfesorSerializer

class ComunidadViewSet(viewsets.ModelViewSet):

    serializer_class = AlumnoSerializer
    #serializer_class_ = ProfesorSerializer
    

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

        #return Response({'message':'Se ha eliminado el protocolo correctamente'}, status = status.HTTP_200_OK)

    """
    #post
    def create(self, request):
        
        
        serializer = self.serializer_class(data = request.data)
        nextProtocolo = len(self.get_queryset())


        keyWords = request.data['keyWords']
        keyWords = keyWords.split(',')

        if nextProtocolo == 0:  
            nextProtocolo = 1
        else:
            nextProtocolo = nextProtocolo + 1
        
        nextProtocolo = "%02d" % (nextProtocolo,)
        request.data['number'] = nextProtocolo


        if serializer.is_valid():

            serializer.save()
            fk_Protocol = serializer.data['id']

            for word in keyWords:
                key_serializer = keyWordSerializer(data = {'word':word, 'fk_Protocol':fk_Protocol})
                if key_serializer.is_valid():
                    key_serializer.save()
            
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        

    
    #update
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
    """