from rest_framework.routers import DefaultRouter
from apps.firma.api.views.firma_views import FirmaViewSet

router = DefaultRouter()
router.register(r'firma', FirmaViewSet, basename = 'firma')
urlpatterns = router.urls
