from django.urls import path

import core.views as views

urlpatterns = [
    path('create', views.create_url),
    path('s/<str:slug>', views.get_url),
]
