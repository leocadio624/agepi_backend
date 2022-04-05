from django.contrib import admin
from apps.protocol.models import ProtocolState, Protocol

class ProtocolStateAdmin(admin.ModelAdmin):
    list_display = ('id', 'description')

admin.site.register(ProtocolState, ProtocolStateAdmin)
#admin.site.register(ProtocolState)
admin.site.register(Protocol)