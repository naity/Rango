from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Examples:
    # url(r'^$', 'tango_with_django_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^rango/', include('rango.urls', namespace='rango')),
    url(r'^admin/', include(admin.site.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)