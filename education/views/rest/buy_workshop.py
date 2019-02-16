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
from education.serializers.workshop_serializer import WorkshopSerializer as WS
from django.http import JsonResponse, HttpResponse
from education.models import Workshop
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
888888b.   888     888 Y88b   d88P 8888888 888b    888  .d8888b.              d8888 8888888b. 8888888 
888  "88b  888     888  Y88b d88P    888   8888b   888 d88P  Y88b            d88888 888   Y88b  888   
888  .88P  888     888   Y88o88P     888   88888b  888 888    888           d88P888 888    888  888   
8888888K.  888     888    Y888P      888   888Y88b 888 888                 d88P 888 888   d88P  888   
888  "Y88b 888     888     888       888   888 Y88b888 888  88888         d88P  888 8888888P"   888   
888    888 888     888     888       888   888  Y88888 888    888        d88P   888 888         888   
888   d88P Y88b. .d88P     888       888   888   Y8888 Y88b  d88P       d8888888888 888         888   
8888888P"   "Y88888P"      888     8888888 888    Y888  "Y8888P88      d88P     888 888       8888888 
'''                                                                                                   
                                                                                                      
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from accounts.models import User
from rest_framework import status


@method_decorator([require_http_methods(["GET", "POST", "PUT", "DELETE"])], name='dispatch')
class BuyAPI(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    serializer_class = WS
    model = Workshop
    errors = []

    def get(self, request, format=None, *args, **kwargs):
        if request.GET.get('field'):
            field = request.GET.get('field')
            user = get_object_or_404(User, uuid = request.GET.get('user_uuid'))
            if 'all' == field:
                workshops = self.model.objects.filter(buyers__uuid = request.GET.get('user_uuid'))
                workshop_serialized = self.serializer_class(workshops, many=True)
            elif 'uuid' == field:
                workshops = get_object_or_404(self.model, buyers__uuid = request.GET.get('user_uuid'), uuid = request.GET.get('uuid'))
                workshop_serialized = self.serializer_class(workshops)
            elif 'id' == field:
                workshops = get_object_or_404(self.model, buyers__uuid = request.GET.get('user_uuid'), id = request.GET.get('id'))
                workshop_serialized = self.serializer_class(workshops)
            else:
                return JsonResponse({'error': "This url doesn't provide information based on your request information."}, safe=False, status=status.HTTP_404_NOT_FOUND)
        else:
            workshops = get_object_or_404(self.model, buyers__id = request.GET.get('user_id'))
            workshop_serialized = self.serializer_class(workshops, many=True)
        return JsonResponse({'response': workshop_serialized.data}, safe=False, status=status.HTTP_202_ACCEPTED)

    def post(self, request, format=None, *args, **kwargs):
        print(request.data)
        print('not for:{0}'.format(request.data.get('workshop_uuid')))
        workshop = get_object_or_404(self.model, uuid = request.data.get('workshop_uuid'))
        for user_uuid in request.data.get('users'):
            print('in for:{0}'.format(user_uuid))
            user  = get_object_or_404(User, uuid = user_uuid)
            workshop.buyers.add(user)
        return JsonResponse({'received data': request.data, 'errors': self.errors}, safe=False, status=status.HTTP_200_OK)

    def put(self, request, uuid, format=None, *args, **kwargs):
        return JsonResponse({'received data': request.POST, 'errors': "This method isn't supported by this url."}, safe=False, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, workshop_uuid, user_uuid, format=None, *args, **kwargs):
        # delete an object and send a confirmation response
        from django.db.models import ProtectedError
        try:
            user = get_object_or_404(User, uuid=uuid)
            workshop = get_object_or_404(self.model, uuid=uuid).buyers.remove(user)            
            return JsonResponse({'deleted user{0} from workshop{1}'.format(user.id, workshop.title): True}, safe=False, status=status.HTTP_200_OK)
        except ProtectedError:
            error_message = "This object can't be deleted!!"
            return JsonResponse(error_message, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            error_message = {'errors': [str(val)] for val in e}
            return JsonResponse(error_message, safe=False, status=status.HTTP_400_BAD_REQUEST)

    def get_workshop_serializer(self):
        if 'get' == self.request.method:
            # for read
            return WS
        else:
            # for write
            return WS
                                                                                        