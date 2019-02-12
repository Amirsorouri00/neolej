from django.urls import include, path
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from education.views.rest.workshop import test1 as workshop_test1, test2 as workshop_test2


app_name = 'education'

urlpatterns = [
    # path('form/', include(([
    # ], 'education'), namespace='form')),
    
    path('rest/', include(([

        path('workshop/', include(([
            path('test2/', workshop_test2, name='rest_workshop_test2'),
            path('test1/', workshop_test1, name='rest_workshop_test1'),
            
        ], 'education'), namespace='rest_workshops')),
        
    ], 'education'), namespace='rest')),
]