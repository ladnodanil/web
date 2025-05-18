from catalog.views import index
from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf.urls.static import static

from django.conf import settings

admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Магазин игр"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalog.urls')),
    path('__debug__/', include(debug_toolbar_urls())),
]
handler404 = 'catalog.views.page_not_found'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

