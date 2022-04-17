from rest_framework.routers import DefaultRouter
from apps.comunidad.api.views.comunidad_views import AlumnoViewSet, ComunidadViewSet

router = DefaultRouter()
router.register(r'comunidad', ComunidadViewSet, basename = 'comunidad')
router.register(r'alumnos', AlumnoViewSet, basename = 'alumnos')
urlpatterns = router.urls
