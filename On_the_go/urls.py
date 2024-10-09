from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from On_the_go import settings

urlpatterns = [
    path('', include('masterapp.urls')),
    path('admin/', admin.site.urls),
    path('masterapp/', include(('masterapp.urls', 'masterapp'), namespace='masterapp')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
