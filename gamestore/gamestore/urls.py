from catalog.views import index
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalog.urls'))
]
handler404 = 'catalog.views.page_not_found'
