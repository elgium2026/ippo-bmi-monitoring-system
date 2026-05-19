from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path

urlpatterns = [
    path('healthz/', lambda request: JsonResponse({'status': 'ok'})),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
