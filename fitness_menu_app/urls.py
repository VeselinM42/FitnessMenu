from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('fitness_menu_app.web.urls')),
    path('accounts/', include('fitness_menu_app.accounts.urls')),
    path('recipes/', include('fitness_menu_app.recipes.urls'))
]
