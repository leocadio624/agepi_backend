from django.contrib import admin
from apps.team.models import Team, TeamMembers

admin.site.register(Team)
admin.site.register(TeamMembers)

