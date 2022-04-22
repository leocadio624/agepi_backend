from django.urls import path
from apps.users.api.api import (user_api_view, user_detail_api_view, activateUserApiView, 
								sendActivateCodeApiView)

urlpatterns = [
    path('usuario/', user_api_view, name = 'usuario_api'),
    path('usuario/<int:pk>', user_detail_api_view, name = 'usuario_detail_api_view'),
    path('activar/', activateUserApiView, name = 'activateUserApiView'),
    path('reenviar_codigo/', sendActivateCodeApiView, name = 'reenviar_codigo')
]