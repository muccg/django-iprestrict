from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('iprestrict/', include('iprestrict.urls')),
    path('admin/', admin.site.urls),
]
