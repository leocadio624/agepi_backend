from rest_framework.routers import DefaultRouter
from apps.comunidad.api.views.comunidad_views import AlumnoViewSet, ProgramaAcedemicoViewSet, ComunidadViewSet

router = DefaultRouter()
router.register(r'comunidad', ComunidadViewSet, basename = 'comunidad')
router.register(r'alumnos', AlumnoViewSet, basename = 'alumnos')
router.register(r'programa_academico', ProgramaAcedemicoViewSet, basename = 'programa_academico')
urlpatterns = router.urls
