from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'main'

urlpatterns = [
    path('', views.indexPage, name='index'),
    path('admissions/', views.admissionPage, name='admissions'),
    path('events/', views.eventsPage, name='events'),
    path('event/', views.eventPage, name='event'),
    path('launchpad/', views.launchpadPage, name='launchpad'),
    path('reg_submit/', views.reg_submit, name='reg_submit'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
