from django.contrib import admin
from apps.team.models import Team, TeamMembers, RequestTeam

admin.site.register(Team)
admin.site.register(TeamMembers)
admin.site.register(RequestTeam)

