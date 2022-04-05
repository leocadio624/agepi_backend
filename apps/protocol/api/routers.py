from rest_framework.routers import DefaultRouter
from apps.protocol.api.views.protocol_views import ProtocolViewSet

router = DefaultRouter()
router.register(r'protocols', ProtocolViewSet, basename = 'products')
urlpatterns = router.urls
