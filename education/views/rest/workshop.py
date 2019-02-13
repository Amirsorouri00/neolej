'''
 .d8888b.  888          888               888      8888888                                         888             
d88P  Y88b 888          888               888        888                                           888             
888    888 888          888               888        888                                           888             
888        888  .d88b.  88888b.   8888b.  888        888   88888b.d88b.  88888b.   .d88b.  888d888 888888 .d8888b  
888  88888 888 d88""88b 888 "88b     "88b 888        888   888 "888 "88b 888 "88b d88""88b 888P"   888    88K      
888    888 888 888  888 888  888 .d888888 888        888   888  888  888 888  888 888  888 888     888    "Y8888b. 
Y88b  d88P 888 Y88..88P 888 d88P 888  888 888        888   888  888  888 888 d88P Y88..88P 888     Y88b.       X88 
 "Y8888P88 888  "Y88P"  88888P"  "Y888888 888      8888888 888  888  888 88888P"   "Y88P"  888      "Y888  88888P' 
                                                                         888                                       
                                                                         888                                       
                                                                         888                                       
'''                                                                         
from education.serializers.workshop_serializer import WorkshopSerializer as WS, CourseBodySerializer as CBS, WorkshopFileSerializer as WFS
from django.http import JsonResponse, HttpResponse
from education.models import Workshop, CourseBody
from django.shortcuts import get_object_or_404

'''
88888888888                888             
    888                    888             
    888                    888             
    888   .d88b.  .d8888b  888888 .d8888b  
    888  d8P  Y8b 88K      888    88K      
    888  88888888 "Y8888b. 888    "Y8888b. 
    888  Y8b.          X88 Y88b.       X88 
    888   "Y8888   88888P'  "Y888  88888P' 
                                                                           
'''                                        
                                        

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
    print(request.FILES)

    file_serializer = WFS(data=request.FILES)
    workshop = serializer.save(body=body)
    if file_serializer.is_valid():
        file_serializer.save(workshop = workshop)
    else:
        print(file_serializer.errors)
    print(workshop)
    return JsonResponse({'received data': request.POST}, safe=False, status=200)


'''
888       888                  888               888                              d8888 8888888b. 8888888 
888   o   888                  888               888                             d88888 888   Y88b  888   
888  d8b  888                  888               888                            d88P888 888    888  888   
888 d888b 888  .d88b.  888d888 888  888 .d8888b  88888b.   .d88b.  88888b.     d88P 888 888   d88P  888   
888d88888b888 d88""88b 888P"   888 .88P 88K      888 "88b d88""88b 888 "88b   d88P  888 8888888P"   888   
88888P Y88888 888  888 888     888888K  "Y8888b. 888  888 888  888 888  888  d88P   888 888         888   
8888P   Y8888 Y88..88P 888     888 "88b      X88 888  888 Y88..88P 888 d88P d8888888888 888         888   
888P     Y888  "Y88P"  888     888  888  88888P' 888  888  "Y88P"  88888P" d88P     888 888       8888888 
                                                                   888                                    
                                                                   888                                    
                                                                   888                                    
'''
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser


@method_decorator([require_http_methods(["GET", "POST", "PUT", "DELETE"])], name='dispatch')
class WorkshopAPI(APIView):
    serializer_class = WS
    model = Workshop
    parser_classes = (MultiPartParser, FormParser)
    errors = []

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
        print(request.data)
        workshop_serializer = WS(data = request.POST)
        if workshop_serializer.is_valid():
            workshop = workshop_serializer.save()
            body = CourseBody(description=request.POST.get('body'))
            body_serializer = CBS(data= request.POST)
            if body_serializer.is_valid():
                body = body_serializer.save()
                workshop_serializer.save(body=body)
            else:
                print('body_serializer_errors: {0}'.format(body_serializer.errors))
                self.errors.append({'body_serializer': body_serializer.errors})
            file_serializer = WFS(data=request.data)
            if file_serializer.is_valid():
                file_serializer.save(workshop_id = workshop.id)
                # file_serializer.save()
            else:
                print('file_serializer_errors: {0}'.format(file_serializer.errors))
                self.errors.append({'file_serializer': file_serializer.errors})
        else:
            print('workshop_serializer_errors: {0}'.format(workshop_serializer.errors))
            self.errors.append({'workshop_errors': workshop_serializer.errors})
            return JsonResponse({'received data': request.POST, 'errors': self.errors}, safe=False, status=500)
 
        return JsonResponse({'received data': request.POST, 'errors': self.errors}, safe=False, status=200)


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
