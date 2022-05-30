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
        #serializerAlumno = AlumnoSerializer(self.get_queryset(), many = True)

        emails = []
        boletas = []
        objects = AlumnoSerializer.Meta.model.objects.filter(state = True).values('email', 'boleta')

        for i in objects:
            emails.append( i['email'] )
            boletas.append( i['boleta'] )

       
        serializer = self.get_serializer(self.get_queryset(), many = True)

        return Response(
            {   'programas':serializer.data,
                'al_emails':emails,
                'al_boletas':boletas
            }
            , status = status.HTTP_200_OK)


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

        
        existeEmail = self.get_serializer().Meta.model.objects.filter(email = request.data['email'], state = True).values('email')
        existeBoleta = self.get_serializer().Meta.model.objects.filter(boleta = request.data['boleta'], state = True).values('boleta')

        if existeEmail:
            return Response({'message':'Ya se existe un alumno registrado con este correo electrónico', 'campo':'email'},status = status.HTTP_226_IM_USED)
        if existeBoleta:
            return Response({'message':'Ya se existe un alumno registrado con este numero de boleta', 'campo':'boleta'},status = status.HTTP_226_IM_USED)

        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message'   : 'Se ha registrado el alumno correctamente',
                'alumno'    : serializer.data
                },status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk = None):
        
        if self.get_queryset(pk):
            boleta = self.get_queryset(pk).boleta
            request.data['boleta'] = boleta

            serializer = self.serializer_class(self.get_queryset(pk), data = request.data)
            if  serializer.is_valid():
                serializer.save()
                return Response({   
                    'message':'Se ha actualizado el alumno correctamente',
                    'alumno':serializer.data
                }, status = status.HTTP_200_OK)
            return Response(protocol_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        return Response({'message':'No existe un alumno con estos datos'}, status = status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, pk = None):
        alumno = self.get_queryset().filter(id = pk).first()
        if  alumno:
            alumno.state = False
            alumno.save()
            return Response({'message':'Se ha eliminado el alumno correctamente'}, status = status.HTTP_200_OK)
        return Response({'message':'No existe un alumno con estos datos'}, status = status.HTTP_400_BAD_REQUEST)

class cargarDatosAlumnosViewSet(viewsets.ModelViewSet):
    serializer_class = AlumnoSerializer
    def create(self, request):
        
        alumnos = request.data['alumnos']

        aceptados = []
        rechazados = []

        for i in alumnos:
            if i['estado'] == 1:
                serializer = self.serializer_class(data = {'fk_programa':i['programa_academico'], 'email':i['correo'], 'boleta':i['boleta']})
                if serializer.is_valid():
                    serializer.save()
                    aceptados.append(i)
                else:
                    rechazados.append(i)

        emails = []
        boletas = []
        objects = AlumnoSerializer.Meta.model.objects.filter(state = True).values('email', 'boleta')

        for i in objects:
            emails.append( i['email'] )
            boletas.append( i['boleta'] )


        return Response({
            'aceptados':aceptados,
            'rachazados':rechazados,
            'al_emails':emails,
            'al_boletas':boletas
            }, status = status.HTTP_200_OK)

