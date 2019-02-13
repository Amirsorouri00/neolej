from django.urls import include, path
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from education.views.rest.workshop import test1 as workshop_test1, test2 as workshop_test2, WorkshopAPI
from education.views.rest.workshop_file import test2 as workshop_file_test2

app_name = 'education'

urlpatterns = [
    # path('form/', include(([
    # ], 'education'), namespace='form')),
    
    path('rest/', include(([

        path('workshop/', include(([
            path('test2/', workshop_test2, name='rest_workshop_test2'),
            path('test1/', workshop_test1, name='rest_workshop_test1'),
            path('<int:uuid>/', WorkshopAPI.as_view(), name='rest_workshop_put'),
            path('', WorkshopAPI.as_view(), name='rest_workshop'),
        ], 'education'), namespace='rest_workshops')),

        path('workshop_file/', include(([
            path('test2/', workshop_file_test2, name='rest_workshop_file_test2'),
        ], 'education'), namespace='rest_workshop_files')),
        
    ], 'education'), namespace='rest')),
]