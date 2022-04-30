from rest_framework.routers import DefaultRouter
from apps.firma.api.views.firma_views import FirmaViewSet, FirmaPassViewSet

router = DefaultRouter()
router.register(r'firma', FirmaViewSet, basename = 'firma')
router.register(r'pass', FirmaPassViewSet, basename = 'pass')
urlpatterns = router.urls
