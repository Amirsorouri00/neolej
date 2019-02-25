from education.serializers.workshop_serializer import WorkshopSerializer as WS, CourseBodySerializer as CBS, WorkshopFileSerializer as WFS
from django.http import JsonResponse, HttpResponse
from education.models import WorkshopFile
from django.shortcuts import get_object_or_404

def test2(request, format=None):
    print(request.POST)
    workshops = WorkshopFile.objects.all()
    workshops_serializer = WFS(workshops, many=True)
    print('Workshop serialized result = {0}'.format(workshops_serializer.data)) 
    return JsonResponse({'received data': workshops_serializer.data}, safe=False, status=200)