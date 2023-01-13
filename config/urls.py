from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from config import settings
from core.homepage.views import IndexView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('login/', include('core.login.urls')),
    path('pos/', include('core.pos.urls')),
    path('reports/', include('core.reports.urls')),
    path('user/', include('core.user.urls')),
    path('api/', include('core.api.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
