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
from django.http import JsonResponse, HttpResponse
from education.models import Workshop, WorkshopRates
from accounts.models import User
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
    # print(request.POST)
    # workshops = Workshop.objects.all()
    # workshops_serializer = WS(workshops, many=True)
    # # workshops = CourseBody.objects.all()
    # # workshops_serializer = CBS(workshops, many=True)
    # print('Workshop serialized result = {0}'.format(workshops_serializer.data)) 
    # return JsonResponse({'received data': workshops_serializer.data}, safe=False, status=200)

def test1(request, format=None):
    # print(request.POST)
    # serializer = WS(data = request.POST)
    # body = CourseBody(description=request.POST.get('body'))
    # serializer1 = CBS(data= request.POST)
    # print(serializer.is_valid())
    # print(serializer1.is_valid())
    # print(serializer.errors)
    # print(serializer1.errors)
    # print(serializer.validated_data)
    # print(serializer1.validated_data)
    # body = serializer1.save()
    # print(body.description,body.id)
    # print(request.FILES)

    # file_serializer = WFS(data=request.FILES)
    # workshop = serializer.save(body=body)
    # if file_serializer.is_valid():
    #     file_serializer.save(workshop = workshop)
    # else:
    #     print(file_serializer.errors)
    # print(workshop)
    # return JsonResponse({'received data': request.POST}, safe=False, status=200)


'''
888       888  .d88888b.  8888888b.  888    d8P   .d8888b.  888    888  .d88888b.  8888888b.       8888888b.         d8888 88888888888 8888888888 .d8888b.  
888   o   888 d88P" "Y88b 888   Y88b 888   d8P   d88P  Y88b 888    888 d88P" "Y88b 888   Y88b      888   Y88b       d88888     888     888       d88P  Y88b 
888  d8b  888 888     888 888    888 888  d8P    Y88b.      888    888 888     888 888    888      888    888      d88P888     888     888       Y88b.      
888 d888b 888 888     888 888   d88P 888d88K      "Y888b.   8888888888 888     888 888   d88P      888   d88P     d88P 888     888     8888888    "Y888b.   
888d88888b888 888     888 8888888P"  8888888b        "Y88b. 888    888 888     888 8888888P"       8888888P"     d88P  888     888     888           "Y88b. 
88888P Y88888 888     888 888 T88b   888  Y88b         "888 888    888 888     888 888             888 T88b     d88P   888     888     888             "888 
8888P   Y8888 Y88b. .d88P 888  T88b  888   Y88b  Y88b  d88P 888    888 Y88b. .d88P 888             888  T88b   d8888888888     888     888       Y88b  d88P 
888P     Y888  "Y88888P"  888   T88b 888    Y88b  "Y8888P"  888    888  "Y88888P"  888             888   T88b d88P     888     888     8888888888 "Y8888P"  
'''                                                                                                                                                            
                                                                                                                                                            
from education.serializers.rate_serializer import RateWorkshopSerializer as RWS                                                                                                                                                             
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser


@method_decorator([require_http_methods(["GET", "POST", "PUT", "DELETE"])], name='dispatch')
class RateWorkshoprAPI(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated,)
    serializer_class = RWS
    model = WorkshopRates
    errors = []

    def get(self, request, format=None, *args, **kwargs):
        rate_serialized = 'rate_serialized temp'
        if request.GET.get('field'):
            field = request.GET.get('field')
            sub_field = request.GET.get('sub_field')
            number_or_object = request.GET.get('number_or_object')
            if 'all' == field:
                if 'user' == sub_field:
                    user = get_object_or_404(User, uuid = request.GET.get('user_uuid'))
                    workshop_rates = self.model.objects.filter(user_id = user.id)
                    if True == number_or_object:
                        counted = workshop_rates.count()
                        rate_serialized = self.serializer_class()(workshop_rates, many=True)
                        return JsonResponse({'response': {'rates':rate_serialized.data, 'numbers': counted}}, safe=False, status=status.HTTP_200_OK)
                    else: return JsonResponse({'response': {'rates':rate_serialized.data}}, safe=False, status=status.HTTP_200_OK)
                elif 'course' == sub_field:
                    course = get_object_or_404(User, uuid = request.GET.get('course_uuid'))
                    workshop_rates = self.model.objects.filter(course_id = course.id)
                    if True == number_or_object:
                        counted = workshop_rates.count()
                        rate_serialized = self.serializer_class()(workshop_rates, many=True)
                        return JsonResponse({'response': {'rates':rate_serialized.data, 'numbers': counted}}, safe=False, status=status.HTTP_200_OK)
                    else: return JsonResponse({'response': {'rates':rate_serialized.data}}, safe=False, status=status.HTTP_200_OK)
                else: 
                    return JsonResponse({'error': "This url doesn't provide information based on your request information."}, safe=False, status=status.HTTP_406_NOT_ACCEPTABLE)
            elif 'id' == field:
                rate_serialized = self.serializer_class(get_object_or_404(self.model, id = request.GET.get('id')))
            else:
                return JsonResponse({'error': "This url doesn't provide information based on your request information."}, safe=False, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            rate_serialized = self.serializer_class(self.model.objects.all(), many=True)
        return JsonResponse({'response': rate_serialized.data}, safe=False, status=status.HTTP_200_OK)

    def post(self, request, format=None, *args, **kwargs):
        print(request.data)
        user = get_object_or_404(User, uuid = request.POST.get('user_uuid'))
        course = get_object_or_404(User, uuid = request.POST.get('course_uuid'))
        rate_serializer = self.serializer_class()(data = request.POST)
        if rate_serializer.is_valid():
            workshop_rate = rate_serializer.save(user = user, course = course)
            course.rate = (course.rate*course.rate_numbers + request.POST.get('rate'))/ (course.rate_numbers + 1)
            course.rate_numbers = course.rate_numbers + 1
            course.save()
        else:
            print('rate_serializer_errors: {0}'.format(rate_serializer.errors))
            self.errors.append({'workshop_rate_errors': rate_serializer.errors})
            return JsonResponse({'received data': request.POST, 'errors': self.errors}, safe=False, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'received data': request.POST, 'errors': self.errors}, safe=False, status=status.HTTP_201_CREATED)

    def put(self, request, uuid, format=None, *args, **kwargs):
        print(request.data)
        user = get_object_or_404(User, uuid = request.POST.get('user_uuid'))
        course = get_object_or_404(User, uuid = request.POST.get('course_uuid'))
        workshop_rate = self.model.objects.get(user_id = user.id, course_id = course.id)
        rate_serializer = self.serializer_class()(workshop_rate, data=request.data, partial=True)
        if rate_serializer.is_valid():
            rate = rate_serializer.save()
            return JsonResponse({'received data': request.POST, 'errors': self.errors}, safe=False, status=status.HTTP_201_CREATED)
        else:
            print('rate_serializer_errors: {0}'.format(rate_serializer.errors))
            self.errors.append({'rate_errors': rate_serializer.errors})
            return JsonResponse({'received data': request.POST, 'errors': self.errors}, safe=False, status=status.HTTP_400_BAD_REQUEST)
 
    def delete(self, request, uuid, format=None, *args, **kwargs):
        # delete an object and send a confirmation response
        from django.db.models import ProtectedError
        user = get_object_or_404(User, uuid = request.POST.get('user_uuid'))
        course = get_object_or_404(User, uuid = request.POST.get('course_uuid'))
        try:
            workshop_rate = get_object_or_404(self.model, user_id=user.id, course_id = course.id).delete() 
            course.rate = (course.rate*course.rate_numbers - workshop_rate.rate)/ (course.rate_numbers - 1)
            course.rate_numbers = course.rate_numbers - 1
            course.save()         
            return JsonResponse({'deleted data': rate.uuid}, safe=False, status=200)
        except ProtectedError:
            error_message = "This object can't be deleted!!"
            return JsonResponse(error_message, status=500)
        except Exception as e:
            error_message = {'errors': [str(val)] for val in e}
            return JsonResponse(error_message, safe=False, status=500)
