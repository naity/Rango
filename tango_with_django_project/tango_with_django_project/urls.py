from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from registration.backends.simple.views import RegistrationView
from django.contrib.auth import views

class MyRegistrationView(RegistrationView):
    def get_success_url(self, request, user):
        return "/rango/add_profile/"

urlpatterns = [
    # Examples:
    # url(r'^$', 'tango_with_django_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^rango/', include('rango.urls', namespace='rango')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/password/reset/$', views.password_reset, name="password_reset"),
    url(r'^accounts/password/reset/done/$',
        views.password_reset_done, name="password_reset_done"),
    url(r'^accounts/password/reset/complete/$', 
        views.password_reset_complete, name="password_reset_complete"),
    url(r'^accounts/password/reset/(?P<uidb64>[0-9A-Za-z]+)/(?P<token>.+)/$',
        views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^accounts/register/$', MyRegistrationView.as_view(), name="registration_register"),
    url(r'^accounts/', include('registration.backends.simple.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)