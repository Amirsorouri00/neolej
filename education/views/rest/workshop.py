from education.serializers.workshop_serializer import WorkshopSerializer as WS, CourseBodySerializer as CBS
from django.http import JsonResponse, HttpResponse
from education.models import Workshop, CourseBody
from django.shortcuts import get_object_or_404

def test2(request, format=None):
    print(request.POST)
    workshops = Workshop.objects.all()
    workshops_serializer = WS(workshops, many=True)
    # workshops = CourseBody.objects.all()
    # workshops_serializer = CBS(workshops, many=True)
    print('Workshop serialized result = {0}'.format(workshops_serializer.data)) 
    return JsonResponse({'received data': workshops_serializer.data}, safe=False, status=200)

def test1(request, format=None):
    print(request.POST)
    serializer = WS(data = request.POST)
    body = CourseBody(description=request.POST.get('body'))
    serializer1 = CBS(data= request.POST)
    print(serializer.is_valid())
    print(serializer1.is_valid())
    print(serializer.errors)
    print(serializer1.errors)
    print(serializer.validated_data)
    print(serializer1.validated_data)
    body = serializer1.save()
    print(body.description,body.id)
    workshop = serializer.save(body=body)
    print(workshop)
    # serializer1.save()
    return JsonResponse({'received data': request.POST}, safe=False, status=200)


from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from rest_framework.views import APIView


@method_decorator([require_http_methods(["GET", "POST", "PUT", "DELETE"])], name='dispatch')
class WorkshopAPI(APIView):
    serializer_class = WS
    model = Workshop

    def get(self, request, *args, **kwargs):
        workshop_serialized = 'workshop_serialized temp'
        if request.GET.get('field'):
            field = request.GET.get('field')
            if 'all' == field:
                workshops = Workshop.objects.all()
                workshops_serialized = WS(workshops, many=True)
            elif 'uuid' == field:
                workshop_serialized = self.serializer_class(get_object_or_404(self.model, uuid = request.GET.get('uuid')))
            elif 'email' == field:
                workshop_serialized = self.serializer_class(get_object_or_404(self.model, email = request.GET.get('email')))
            else:
                return JsonResponse({'error': "This url doesn't provide information based on your request information."}, safe=False, status=400)
        else:
            workshop_serialized = self.serializer_class(get_object_or_404(self.model, uuid = request.GET.get('uuid')))
        return JsonResponse({'response': workshop_serialized.data}, safe=False, status=200)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = request.POST)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'received data': serializer.data}, safe=False, status=200)
        else:
            return JsonResponse({'received data': request.POST, 'errors': serializer.errors}, safe=False, status=500)

    def put(self, request, uuid, *args, **kwargs):
        workshop = get_object_or_404(self.model, uuid = uuid)
        serializer = self.serializer_class(workshop, data = request.POST, partial=True)
        if serializer.is_valid():
            return JsonResponse({'received data': serializer.data}, safe=False, status=200)
        else:
            return JsonResponse({'received data': serializer.errors}, safe=False, status=500)

    def delete(self, request, uuid, *args, **kwargs):
        # delete an object and send a confirmation response
        from django.db.models import ProtectedError
        try:
            get_object_or_404(self.model, uuid=uuid).delete()            
            return JsonResponse({'deleted data': uuid}, safe=False, status=200)
        except ProtectedError:
            error_message = "This object can't be deleted!!"
            return JsonResponse(error_message, status=500)
        except Exception as e:
            error_message = {'errors': [str(val)] for val in e}
            return JsonResponse(error_message, safe=False, status=500)
