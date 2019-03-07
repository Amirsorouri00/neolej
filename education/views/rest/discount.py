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
from education.serializers.discount_serializer import WorkshopDiscountSerializer as WDS
from django.http import JsonResponse, HttpResponse
from education.models import WorkshopDiscount
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
    discounts = WorkshopDiscount.objects.all()
    discounts_serializer = DS(discounts, many=True)
    print('Discount serialized result = {0}'.format(discounts_serializer.data)) 
    return JsonResponse({'received data': discounts_serializer.data}, safe=False, status=200)

def test1(request, format=None):
    print(request.POST)
    serializer = DS(data = request.POST)
    print(serializer.is_valid())
    print(serializer.errors)
    print(serializer.validated_data)
    serializer.save()

    return JsonResponse({'received data': request.POST}, safe=False, status=200)

'''
8888888b.                                                      888 8888888b.  d8b                                             888    
888   Y88b                                                     888 888  "Y88b Y8P                                             888    
888    888                                                     888 888    888                                                 888    
888   d88P .d88b.  888d888 .d8888b   .d88b.  88888b.   8888b.  888 888    888 888 .d8888b   .d8888b .d88b.  888  888 88888b.  888888 
8888888P" d8P  Y8b 888P"   88K      d88""88b 888 "88b     "88b 888 888    888 888 88K      d88P"   d88""88b 888  888 888 "88b 888    
888       88888888 888     "Y8888b. 888  888 888  888 .d888888 888 888    888 888 "Y8888b. 888     888  888 888  888 888  888 888    
888       Y8b.     888          X88 Y88..88P 888  888 888  888 888 888  .d88P 888      X88 Y88b.   Y88..88P Y88b 888 888  888 Y88b.  
888        "Y8888  888      88888P'  "Y88P"  888  888 "Y888888 888 8888888P"  888  88888P'  "Y8888P "Y88P"   "Y88888 888  888  "Y888 
'''

from education.serializers.discount_serializer import WorkshopPersonalDiscountSerializer as WPDS
from education.models import WorkshopPersonalDiscount
from commons.permission_controllers import RestFrameworkPermissionController
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.views.decorators.http import require_http_methods
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from accounts.models import User
from rest_framework import status   

class WorkshopPersonalDiscountAPI(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = (IsAuthenticated, RestFrameworkPermissionController)
    serializer_class = WPDS
    model = WorkshopPersonalDiscount
    errors = []

    def dispatch(self, request, uuid = None, format=None, *args, **kwargs):
        if 'Get' == request.method:
            self.permission_classes = (IsAuthenticated,)
        else:
            self.permission_classes = (IsAuthenticated, RestFrameworkPermissionController)
        return super().dispatch(request, uuid = uuid, format=None, *args, **kwargs)

    def get(self, request, format=None, *args, **kwargs):
        if request.GET.get('field'):
            field = request.GET.get('field')
            if 'all' == field:
                workshop_personal_discounts = self.model.objects.all()
                workshop_personal_discount_serialized = self.serializer_class(workshop_personal_discounts, many=True)
            elif 'user_uuid' == field:
                user = get_object_or_404(User, uuid = request.GET.get('user_uuid'))
                workshop_personal_discounts = get_object_or_404(self.model, person = user.id, used = False)
                workshop_personal_discount_serialized = self.serializer_class(workshop_personal_discounts)
            elif 'workshop_uuid' == field:
                workshop_personal_discounts = get_object_or_404(self.model, workshops__uuid = request.GET.get('user_uuid'))
                workshop_personal_discount_serialized = self.serializer_class(workshop_personal_discounts)
            else:
                return JsonResponse({'error': "This url doesn't provide information based on your request information."}, safe=False, status=status.HTTP_404_NOT_FOUND)
        else:
            workshop_personal_discounts = self.model.objects.filter(used = False)
            workshop_personal_discount_serialized = self.serializer_class(workshop_personal_discounts, many=True)
        return JsonResponse({'response': workshop_personal_discount_serialized.data}, safe=False, status=status.HTTP_202_ACCEPTED)

    def post(self, request, format=None, *args, **kwargs):
        print(request.data)
        personal_discount_serializer = self.serializer_class(data = request.data)
        if personal_discount_serializer.is_valid():
            workshop_personal_discount = personal_discount_serializer.save()
        else:
            print('personal_discount_serializer_errors: {0}'.format(personal_discount_serializer.errors))
            self.errors.append({'personal_discount_serializer_errors': personal_discount_serializer.errors})
            return JsonResponse({'received data': request.data, 'errors': self.errors}, safe=False, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'received data': request.data, 'errors': self.errors}, safe=False, status=status.HTTP_200_OK)
    
    def put(self, request, uuid, format=None, *args, **kwargs):
        print(request.data)
        print(uuid)
        workshop_personal_discount = get_object_or_404(self.model, uuid = uuid)
        personal_discount_serializer = self.serializer_class(workshop_personal_discount, data = request.data, partial=True)
        if personal_discount_serializer.is_valid():
            workshop_personal_discount = personal_discount_serializer.save()
        else:
            print('personal_discount_serializer_errors: {0}'.format(personal_discount_serializer.errors))
            self.errors.append({'personal_discount_serializer_errors': personal_discount_serializer.errors})
            return JsonResponse({'received data': request.data, 'errors': self.errors}, safe=False, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'received data': request.data, 'errors': self.errors}, safe=False, status=status.HTTP_200_OK)

    def delete(self, request, uuid, format=None, *args, **kwargs):
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

'''
8888888b.           888            8888888b.  d8b                                             888    
888  "Y88b          888            888  "Y88b Y8P                                             888    
888    888          888            888    888                                                 888    
888    888  8888b.  888888 .d88b.  888    888 888 .d8888b   .d8888b .d88b.  888  888 88888b.  888888 
888    888     "88b 888   d8P  Y8b 888    888 888 88K      d88P"   d88""88b 888  888 888 "88b 888    
888    888 .d888888 888   88888888 888    888 888 "Y8888b. 888     888  888 888  888 888  888 888    
888  .d88P 888  888 Y88b. Y8b.     888  .d88P 888      X88 Y88b.   Y88..88P Y88b 888 888  888 Y88b.  
8888888P"  "Y888888  "Y888 "Y8888  8888888P"  888  88888P'  "Y8888P "Y88P"   "Y88888 888  888  "Y888 
'''                                                                                                                                                                                                       
                                                                                                     
from education.serializers.discount_serializer import WorkshopDateDiscountSerializer as WDDS
from education.models import WorkshopDateDiscount
class WorkshopDateDiscountAPI(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = (IsAuthenticated, RestFrameworkPermissionController)
    serializer_class = WDDS
    model = WorkshopDateDiscount
    errors = []

    def dispatch(self, request, uuid = None, format=None, *args, **kwargs):
        if 'Get' == request.method:
            self.permission_classes = (IsAuthenticated,)
        else:
            self.permission_classes = (IsAuthenticated, RestFrameworkPermissionController)
        return super().dispatch(request, uuid = uuid, format=None, *args, **kwargs)

    def get(self, request, format=None, *args, **kwargs):
        if request.GET.get('field'):
            field = request.GET.get('field')
            if 'all' == field:
                workshop_date_discounts = self.model.objects.all()
                workshop_date_discount_serialized = self.serializer_class(workshop_date_discounts, many=True)
            elif 'user_uuid' == field:
                user = get_object_or_404(User, uuid = request.GET.get('user_uuid'))
                workshop_date_discounts = get_object_or_404(self.model, person = user.id, used = False)
                workshop_date_discount_serialized = self.serializer_class(workshop_date_discounts)
            elif 'workshop_uuid' == field:
                workshop_date_discounts = get_object_or_404(self.model, workshops__uuid = request.GET.get('user_uuid'))
                workshop_date_discount_serialized = self.serializer_class(workshop_date_discounts)
            else:
                return JsonResponse({'error': "This url doesn't provide information based on your request information."}, safe=False, status=status.HTTP_404_NOT_FOUND)
        else:
            workshop_date_discounts = self.model.objects.filter(used = False)
            workshop_date_discount_serialized = self.serializer_class(workshop_date_discounts, many=True)
        return JsonResponse({'response': workshop_date_discount_serialized.data}, safe=False, status=status.HTTP_202_ACCEPTED)

    def post(self, request, format=None, *args, **kwargs):
        print(request.data)
        date_discount_serializer = self.serializer_class(data = request.data)
        if date_discount_serializer.is_valid():
            workshop_date_discount = date_discount_serializer.save()
        else:
            print('date_discount_serializer_errors: {0}'.format(date_discount_serializer.errors))
            self.errors.append({'date_discount_serializer_errors': date_discount_serializer.errors})
            return JsonResponse({'received data': request.data, 'errors': self.errors}, safe=False, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'received data': request.data, 'errors': self.errors}, safe=False, status=status.HTTP_200_OK)
    
    def put(self, request, uuid, format=None, *args, **kwargs):
        print(request.data)
        workshop_date_discount = get_object_or_404(self.model, uuid = uuid)
        date_discount_serializer = self.serializer_class(workshop_date_discount, data = request.data, partial=True)
        if date_discount_serializer.is_valid():
            workshop_date_discount = date_discount_serializer.save()
        else:
            print('date_discount_serializer_errors: {0}'.format(date_discount_serializer.errors))
            self.errors.append({'date_discount_serializer_errors': date_discount_serializer.errors})
            return JsonResponse({'received data': request.data, 'errors': self.errors}, safe=False, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'received data': request.data, 'errors': self.errors}, safe=False, status=status.HTTP_200_OK)
    
    def delete(self, request, uuid, format=None, *args, **kwargs):
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

'''
8888888b.                            8888888b.  d8b                                             888    
888   Y88b                           888  "Y88b Y8P                                             888    
888    888                           888    888                                                 888    
888   d88P  8888b.   .d8888b .d88b.  888    888 888 .d8888b   .d8888b .d88b.  888  888 88888b.  888888 
8888888P"      "88b d88P"   d8P  Y8b 888    888 888 88K      d88P"   d88""88b 888  888 888 "88b 888    
888 T88b   .d888888 888     88888888 888    888 888 "Y8888b. 888     888  888 888  888 888  888 888    
888  T88b  888  888 Y88b.   Y8b.     888  .d88P 888      X88 Y88b.   Y88..88P Y88b 888 888  888 Y88b.  
888   T88b "Y888888  "Y8888P "Y8888  8888888P"  888  88888P'  "Y8888P "Y88P"   "Y88888 888  888  "Y888 
'''                                                                                                       
                                                                                                       
from education.serializers.discount_serializer import WorkshopRaceDiscountSerializer as WRDS
from education.models import WorkshopRaceDiscount
class WorkshopRaceDiscountAPI(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = (IsAuthenticated,)
    serializer_class = WRDS
    model = WorkshopRaceDiscount
    errors = []

    def get(self, request, format=None, *args, **kwargs):
        if request.GET.get('field'):
            field = request.GET.get('field')
            if 'all' == field:
                workshop_race_discounts = self.model.objects.all()
                workshop_race_discount_serialized = self.serializer_class(workshop_race_discounts, many=True)
            elif 'user_uuid' == field:
                user = get_object_or_404(User, uuid = request.GET.get('user_uuid'))
                workshop_race_discounts = get_object_or_404(self.model, person = user.id)
                workshop_race_discount_serialized = self.serializer_class(workshop_race_discounts)
            elif 'workshop_uuid' == field:
                workshop_race_discounts = get_object_or_404(self.model, workshops__uuid = request.GET.get('user_uuid'))
                workshop_race_discount_serialized = self.serializer_class(workshop_race_discounts)
            else:
                return JsonResponse({'error': "This url doesn't provide information based on your request information."}, safe=False, status=status.HTTP_404_NOT_FOUND)
        else:
            workshop_race_discounts = self.model.objects.all()
            workshop_race_discount_serialized = self.serializer_class(workshop_race_discounts, many=True)
        return JsonResponse({'response': workshop_race_discount_serialized.data}, safe=False, status=status.HTTP_202_ACCEPTED)

    def post(self, request, format=None, *args, **kwargs):
        print(request.data)
        race_discount_serializer = self.serializer_class(data = request.data)
        if race_discount_serializer.is_valid():
            workshop_race_discount = race_discount_serializer.save()
        else:
            print('race_discount_serializer_errors: {0}'.format(race_discount_serializer.errors))
            self.errors.append({'race_discount_serializer_errors': race_discount_serializer.errors})
            return JsonResponse({'received data': request.data, 'errors': self.errors}, safe=False, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'received data': request.data, 'errors': self.errors}, safe=False, status=status.HTTP_200_OK)
    
    def put(self, request, uuid, format=None, *args, **kwargs):
        print(request.data)
        workshop_race_discount = get_object_or_404(self.model, uuid = uuid)
        race_discount_serializer = self.serializer_class(workshop_race_discount, data = request.data, partial=True)
        if race_discount_serializer.is_valid():
            workshop_race_discount = race_discount_serializer.save()
        else:
            print('race_discount_serializer_errors: {0}'.format(race_discount_serializer.errors))
            self.errors.append({'race_discount_serializer_errors': race_discount_serializer.errors})
            return JsonResponse({'received data': request.data, 'errors': self.errors}, safe=False, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'received data': request.data, 'errors': self.errors}, safe=False, status=status.HTTP_200_OK)
    
    def delete(self, request, uuid, format=None, *args, **kwargs):
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
