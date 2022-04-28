from rest_framework.routers import DefaultRouter
from apps.notification.api.views.notificacion_views import NotificacionViewSet, CancelInvitationViewSet

router = DefaultRouter()
router.register(r'notificaciones', NotificacionViewSet, basename = 'notificaciones')
router.register(r'cancelarInvitacion', CancelInvitationViewSet, basename = 'cancelarInvitacion')
urlpatterns = router.urls
