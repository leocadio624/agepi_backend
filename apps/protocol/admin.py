from django.contrib import admin
from apps.protocol.models import (  ProtocolState, Protocol, keyWord, PeriodoEscolar, catInscripccion,
                                     AsignacionProtocolo, SelectProtocolo, Evaluacion, Pregunta)

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
admin.site.register(SelectProtocolo)
admin.site.register(Evaluacion)
admin.site.register(Pregunta)




