from django.urls import path

from .views import *

app_name = 'cart'

urlpatterns = [
    path('', cart_detail, name='detail'),
    path('add/<slug:raffle_slug>/', cart_add, name='add'),
    path('remove/<slug:raffle_slug>/', cart_remove, name='remove')
]