from django.urls import path

from fitness_menu_app.web.views import index

urlpatterns = [
    path('', index, name='index'),
]
