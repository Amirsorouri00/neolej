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
from education.serializers.workshop_serializer import WorkshopSerializer as WS, CourseBodySerializer as CBS, WorkshopFileSerializer as WFS, PriceSerializer as PS
from django.http import JsonResponse, HttpResponse
from education.models import Workshop, CourseBody, Price
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
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from file_app.serializers.file_serializer import FileSerializer as FS


@method_decorator([require_http_methods(["GET", "POST", "PUT", "DELETE"])], name='dispatch')
class WorkshopAPI(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated,)
    serializer_class = WS
    model = Workshop
    errors = []

    def get(self, request, format=None, *args, **kwargs):
        workshop_serialized = 'workshop_serialized temp'
        if request.GET.get('field'):
            field = request.GET.get('field')
            if 'all' == field:
                workshops = Workshop.objects.all()
                workshop_serialized = self.serializer_class(workshops, many=True)
            elif 'id' == field:
                workshop_serialized = self.serializer_class(get_object_or_404(self.model, id = request.GET.get('id')))
            elif 'title' == field:
                workshop_serialized = self.serializer_class(get_object_or_404(self.model, title = request.GET.get('title')))
            else:
                return JsonResponse({'error': "This url doesn't provide information based on your request information."}, safe=False, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            workshop_serialized = self.serializer_class(get_object_or_404(self.model, uuid = request.GET.get('uuid')))
        return JsonResponse({'response': workshop_serialized.data}, safe=False, status=status.HTTP_200_OK)

    def post(self, request, format=None, *args, **kwargs):
        print(request.data)
        workshop_serializer = self.get_workshop_serializer()(data = request.POST)
        if workshop_serializer.is_valid():
            workshop = workshop_serializer.save()
            body = CourseBody(description=request.POST.get('description'))
            body_serializer = self.get_course_body_serializer()(data= request.POST)
            if body_serializer.is_valid():
                body = body_serializer.save()
                workshop_serializer.save(body=body)
            else:
                print('body_serializer_errors: {0}'.format(body_serializer.errors))
                self.errors.append({'body_serializer': body_serializer.errors})

            # price
            # price_serializer = self.get_price_serializer()(data= request.POST)
            # if price_serializer.is_valid():
            #     price = price_serializer.save()
            #     workshop_serializer.save(price=price)
            # else:
            #     print('price_serializer_errors: {0}'.format(price_serializer.errors))
            #     self.errors.append({'price_serializer': price_serializer.errors})
            # price = Price.objects.create(online_or_workshop = False, unit = 1, cost = request.POST.get('price'))

            # file
            # print(request.data.getlist('file'))
            files = request.data.getlist('file')
            for file in files:
                tmp_dict = {}
                tmp_dict['file'] = file
                if None == request.data.get('remark'):
                    tmp_dict['remark'] = 'Not Set'
                else:
                    tmp_dict['remark'] = request.data.get('remark')
                file_serializer = self.get_workshop_file_serializer()(data=tmp_dict)
                if file_serializer.is_valid():
                    print(file_serializer.validated_data)
                    file_serializer.save(workshop = workshop)
                    # file_serializer.save()
                else:
                    print('file_serializer_errors: {0}'.format(file_serializer.errors))
                    self.errors.append({'file_serializer': file_serializer.errors})
        else:
            print('workshop_serializer_errors: {0}'.format(workshop_serializer.errors))
            self.errors.append({'workshop_errors': workshop_serializer.errors})
            return JsonResponse({'received data': request.POST, 'errors': self.errors}, safe=False, status=status.HTTP_400_BAD_REQUEST)
 
        return JsonResponse({'received data': request.POST, 'errors': self.errors}, safe=False, status=status.HTTP_201_CREATED)

    def put(self, request, uuid, format=None, *args, **kwargs):
        print(request.data)
        print(uuid)
        workshop = get_object_or_404(self.model, pk=uuid)
        workshop_serializer = self.get_workshop_serializer()(workshop, data=request.data, partial=True)
        if workshop_serializer.is_valid():
            workshop = workshop_serializer.save()
            # set body serializer
            if workshop.body is not None:
                body = workshop.body
                body_serializer = self.get_course_body_serializer()(body, data=request.data, partial=True)
            else:
                # body = CourseBody(description=request.data.get('description'))
                body_serializer = self.get_course_body_serializer()(data= request.data)
            # save body serializer
            if body_serializer.is_valid():
                body = body_serializer.save()
                workshop_serializer.save(body=body)
            else:
                print('body_serializer_errors: {0}'.format(body_serializer.errors))
                self.errors.append({'body_serializer': body_serializer.errors})

            # price
            # if workshop.price is not None:
            #     price = workshop.price
            #     price_serializer = self.get_price_serializer()(body, data=request.data, partial=True)
            # else:
            #     price_serializer = self.get_price_serializer()(data= request.data)
            # if price_serializer.is_valid():
            #     price = price_serializer.save()
            #     workshop_serializer.save(price=price)
            # else:
            #     print('price_serializer_errors: {0}'.format(price_serializer.errors))
            #     self.errors.append({'price_serializer': price_serializer.errors})

            # file serializer            
            print(request.data.getlist('file'))
            files = request.data.getlist('file')
            for file in files:
                tmp_dict = {}
                tmp_dict['file'] = file
                if None == request.data.get('remark'):
                    tmp_dict['remark'] = 'Not Set'
                else:
                    tmp_dict['remark'] = request.data.get('remark')
                file_serializer = self.get_workshop_file_serializer()(data=tmp_dict)
                if file_serializer.is_valid():
                    print(file_serializer.validated_data)
                    file_serializer.save(workshop = workshop)
                else:
                    print('file_serializer_errors: {0}'.format(file_serializer.errors))
                    self.errors.append({'file_serializer': file_serializer.errors})
        else:
            print('workshop_serializer_errors: {0}'.format(workshop_serializer.errors))
            self.errors.append({'workshop_errors': workshop_serializer.errors})
            return JsonResponse({'received data': request.POST, 'errors': self.errors}, safe=False, status=status.HTTP_400_BAD_REQUEST)
 
        return JsonResponse({'received data': request.POST, 'errors': self.errors}, safe=False, status=status.HTTP_201_CREATED)

    def delete(self, request, uuid, format=None, *args, **kwargs):
        # delete an object and send a confirmation response
        from django.db.models import ProtectedError
        try:
            get_object_or_404(self.model, pk=uuid).delete()            
            return JsonResponse({'deleted data': uuid}, safe=False, status=200)
        except ProtectedError:
            error_message = "This object can't be deleted!!"
            return JsonResponse(error_message, status=500)
        except Exception as e:
            error_message = {'errors': [str(val)] for val in e}
            return JsonResponse(error_message, safe=False, status=500)

    def get_workshop_serializer(self):
        if 'get' == self.request.method:
            # for read
            return WS
        else:
            # for write
            return WS
    def get_workshop_file_serializer(self):
        if 'get' == self.request.method:
            return WFS
        else:
            return WFS
    def get_course_body_serializer(self):
        if 'get' == self.request.method:
            return CBS
        else:
            return CBS
    def get_price_serializer(self):
        if 'get' == self.request.method:
            return PS
        else:
            return PS