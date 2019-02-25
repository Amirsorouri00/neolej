from django.conf.urls import url
from file_app.views.rest.file_views import FileView

urlpatterns = [
    url(r'^upload/$', FileView.as_view(), name='file-upload'),
]