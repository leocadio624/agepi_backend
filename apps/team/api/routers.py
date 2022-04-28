from rest_framework.routers import DefaultRouter
from apps.team.api.views.team_views import TeamViewSet, teamListViewSet, AlumnoTeamViewSet, TeamMemberViewSet, TeamMembersByTeamViewSet

router = DefaultRouter()
router.register(r'teams', TeamViewSet, basename = 'teams')
router.register(r'team_list', teamListViewSet, basename = 'team_list')
router.register(r'alumno_team', AlumnoTeamViewSet, basename = 'alumno_team')
router.register(r'team_member', TeamMemberViewSet, basename = 'team_member')
router.register(r'members_by_team', TeamMembersByTeamViewSet, basename = 'members_by_team')


urlpatterns = router.urls
