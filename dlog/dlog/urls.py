from django.contrib import admin
from django.urls import path, include
#from main.views import api

urlpatterns = [
    path('admin/', admin.site.urls),
   path('api/', include('main.urls')),
    
]
