# Github.com/Rasooll
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^request/$', views.send_request, name='request'),
    url(r'^verify/$', views.verify , name='verify'),
    url(r'^verify_redirect/$', views.verify_redirect , name='verify_redirect'),
]
