from django.urls import path
from apps.protocol.api.views.general_views import ProtocolStateListAPIView
from apps.protocol.api.views.protocol_views import (
    #ProtocolListCreateAPIView,
    #ProductRetrieveUpdateDestroyAPIView    
)
urlpatterns = [
    path('protocol_state/', ProtocolStateListAPIView.as_view(), name = 'protocol_state'),
    #path('protocol/', ProtocolListCreateAPIView.as_view(), name = 'protocol_list_create'),
    #path('protocol/retrieve_update_destroy/<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name = 'protocol_retrieve_update_destroy')
]