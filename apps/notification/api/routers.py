from rest_framework.routers import DefaultRouter
from apps.notification.api.views.notificacion_views import NotificacionViewSet

router = DefaultRouter()
router.register(r'notificaciones', NotificacionViewSet, basename = 'notificaciones')
urlpatterns = router.urls
