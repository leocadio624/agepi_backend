from rest_framework.routers import DefaultRouter
from apps.team.api.views.team_views import TeamViewSet, teamListViewSet, AlumnoTeamViewSet

router = DefaultRouter()
router.register(r'teams', TeamViewSet, basename = 'teams')
router.register(r'team_list', teamListViewSet, basename = 'team_list')
router.register(r'alumno_team', AlumnoTeamViewSet, basename = 'alumno_team')

urlpatterns = router.urls
