from django.contrib import admin
from apps.protocol.models import ProtocolState, Protocol, keyWord, PeriodoEscolar, catInscripccion, AsignacionProtocolo

class ProtocolStateAdmin(admin.ModelAdmin):
    list_display = ('id', 'description')


class keyWordAdmin(admin.ModelAdmin):
    list_display = ('id', 'word')



admin.site.register(ProtocolState, ProtocolStateAdmin)
admin.site.register(Protocol)
admin.site.register(keyWord, keyWordAdmin)
admin.site.register(PeriodoEscolar)
admin.site.register(catInscripccion)
admin.site.register(AsignacionProtocolo)



