from django.contrib import admin
from apps.team.models import Team, TeamMembers

class TeamMembersAdmin(admin.ModelAdmin):
    list_display = ('id', 'fk_team', 'fk_user', 'solicitudEquipo')

admin.site.register(Team)
admin.site.register(TeamMembers, TeamMembersAdmin)



