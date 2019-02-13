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
from accounts.serializers.user_serializer import UserSerializer as US
from django.http import JsonResponse
from accounts.models import User


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
    users = User.objects.all()
    users_serializer = US(users, many = True)
    print('user serialized result = {0}'.format(users_serializer))
    return JsonResponse({'received data': users_serializer.data}, safe=False, status=200)

def test1(request, format=None):
    print(request.POST)
    serializer = US(data = request.POST)
    print(serializer)
    print(serializer.is_valid())
    print(serializer.errors)
    print(serializer.validated_data)
    serializer.save()
    return JsonResponse({'received data': request.POST}, safe=False, status=200)



'''
888     888  .d8888b.  8888888888 8888888b.              d8888 8888888b. 8888888 
888     888 d88P  Y88b 888        888   Y88b            d88888 888   Y88b  888   
888     888 Y88b.      888        888    888           d88P888 888    888  888   
888     888  "Y888b.   8888888    888   d88P          d88P 888 888   d88P  888   
888     888     "Y88b. 888        8888888P"          d88P  888 8888888P"   888   
888     888       "888 888        888 T88b          d88P   888 888         888   
Y88b. .d88P Y88b  d88P 888        888  T88b        d8888888888 888         888   
 "Y88888P"   "Y8888P"  8888888888 888   T88b      d88P     888 888       8888888 
                                                                                   
'''
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404

@method_decorator([require_http_methods(["GET", "POST", "PUT", "DELETE"])], name='dispatch')
class UserAPI(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = US
    model = User
    errors = []

    def get(self, request, format=None, *args, **kwargs):
        user_serialized = 'user_serialized temp'
        if request.GET.get('field'):
            field = request.GET.get('field')
            if 'all' == field:
                users = User.objects.all()
                user_serialized = self.serializer_class(users, many=True)
            elif 'uuid' == field:
                user_serialized = self.serializer_class(get_object_or_404(self.model, uuid = request.GET.get('uuid')))
            elif 'email' == field:
                user_serialized = self.serializer_class(get_object_or_404(self.model, email = request.GET.get('email')))
            else:
                return JsonResponse({'error': "This url doesn't provide information based on your request information."}, safe=False, status=400)
        else:
            user_serialized = self.serializer_class(get_object_or_404(self.model, uuid = request.GET.get('uuid')))
        return JsonResponse({'response': user_serialized.data}, safe=False, status=200)

    def post(self, request, format=None, *args, **kwargs):
        print(request.data)
        user_serializer = self.serializer_class(data = request.POST)
        if user_serializer.is_valid():
            user = user_serializer.save()
            return JsonResponse({'received data': request.POST, 'errors': self.errors}, safe=False, status=200)    
        else:
            print('user_serializer_errors: {0}'.format(user_serializer.errors))
            self.errors.append({'user_serializer': user_serializer.errors})
            return JsonResponse({'received data': request.POST, 'errors': self.errors}, safe=False, status=500)
 
        return JsonResponse({'received data': request.POST, 'errors': self.errors}, safe=False, status=200)
    
    def put(self, request, uuid, format=None, *args, **kwargs):
        print(request.data)
        print(uuid)
        user = get_object_or_404(self.model, pk=uuid)
        user_serializer = self.serializer_class(user, data=request.POST, partial=True)
        if user_serializer.is_valid():
            user = user_serializer.save()
            return JsonResponse({'received data': request.POST, 'errors': self.errors}, safe=False, status=200)    
        else:
            print('user_serializer_errors: {0}'.format(user_serializer.errors))
            self.errors.append({'user_serializer': user_serializer.errors})
            return JsonResponse({'received data': request.POST, 'errors': self.errors}, safe=False, status=500)
 
        return JsonResponse({'received data': request.POST, 'errors': self.errors}, safe=False, status=200)

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


'''
 .d8888b. 8888888 888b    888  .d8888b.  888      8888888888      888     888  .d8888b.  8888888888 8888888b.  
d88P  Y88b  888   8888b   888 d88P  Y88b 888      888             888     888 d88P  Y88b 888        888   Y88b 
Y88b.       888   88888b  888 888    888 888      888             888     888 Y88b.      888        888    888 
 "Y888b.    888   888Y88b 888 888        888      8888888         888     888  "Y888b.   8888888    888   d88P 
    "Y88b.  888   888 Y88b888 888  88888 888      888             888     888     "Y88b. 888        8888888P"  
      "888  888   888  Y88888 888    888 888      888             888     888       "888 888        888 T88b   
Y88b  d88P  888   888   Y8888 Y88b  d88P 888      888             Y88b. .d88P Y88b  d88P 888        888  T88b  
 "Y8888P" 8888888 888    Y888  "Y8888P88 88888888 8888888888       "Y88888P"   "Y8888P"  8888888888 888   T88b 
                                                                                                               
                    
'''

@method_decorator([require_http_methods(["GET", "POST", "PUT", "DELETE"])], name='dispatch')
class SingleUser(APIView):
    serializer_class = US
    model = User

    def get(self, request, *args, **kwargs):
        user_serialized = self.serializer_class(get_object_or_404(self.model, uuid = request.GET.get('uuid')))
        return JsonResponse({'response': user_serialized.data}, safe=False, status=200)

    def post(self, request, uuid = None, *args, **kwargs):
        serializer = None
        if uuid:
            user = get_object_or_404(self.model, uuid = uuid)
            serializer = self.serializer_class(user, data = request.POST, partial=True)
        else:
            serializer = self.serializer_class(data = request.POST)
        if serializer.is_valid():
            serializer.save()
            # <process serializer cleaned data>
            # return HttpResponseRedirect('/success/')
            return JsonResponse({'received data': serializer.data}, safe=False, status=200)
        else:
            return JsonResponse({'received data': request.POST, 'errors': serializer.errors}, safe=False, status=500)

    def put(self, request, uuid, *args, **kwargs):
        user = get_object_or_404(self.model, uuid = uuid)
        serializer = self.serializer_class(user, data = request.POST, partial=True)
        if serializer.is_valid():
            # <process serializer cleaned data>
            # return HttpResponseRedirect('/success/')
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


'''
888     888  .d8888b.  8888888888 8888888b.       888      8888888 .d8888b. 88888888888 
888     888 d88P  Y88b 888        888   Y88b      888        888  d88P  Y88b    888     
888     888 Y88b.      888        888    888      888        888  Y88b.         888     
888     888  "Y888b.   8888888    888   d88P      888        888   "Y888b.      888     
888     888     "Y88b. 888        8888888P"       888        888      "Y88b.    888     
888     888       "888 888        888 T88b        888        888        "888    888     
Y88b. .d88P Y88b  d88P 888        888  T88b       888        888  Y88b  d88P    888     
 "Y88888P"   "Y8888P"  8888888888 888   T88b      88888888 8888888 "Y8888P"     888     
                                                                                                    
'''
from rest_framework import generics
# from rest_framework.permissions import IsAdminUser, IsAuthenticated

class UserListCreate(generics.ListCreateAPIView):
    ''' Used for read-write endpoints to represent a collection of model instances.
    Provides get and post method handlers. '''

    queryset = User.objects.all()
    serializer_class = US
    # permission_classes = (IsAdminUser, IsAuthenticated)

    def get_queryset(self):
        # user = User.objects.filter(id = 3)
        # print(self.request.data.get('all'))
        filter_role = {}
        # queryset = self.get_queryset()
        if self.request.data.get('all'):
            return User.objects.all()
        elif self.request.data.get('fields'):
            #change
            data = self.request.data.get('fields').strip('[').rstrip(']')
            filter_role['id'] = [{int(val) for val in data.split(',')}]
            print(filter_role)
            # return User.objects.filter(id in filter_role)
            return get_object_or_404(User.objects.all(), *filter_role)

        else: return JsonResponse({'error': 'no user specified to show.'})

    def perform_create(self, serializer):
        serializer.save(data=self.request.data)

    def perform_update(self, serializer):
        serializer.save(data=self.request.data)

    # def get_object(self):
    #     queryset = self.get_queryset()
    #     filter = {}
    #     for field in self.multiple_lookup_fields:
    #         filter[field] = self.kwargs[field]

    #     obj = get_object_or_404(queryset, **filter)
    #     self.check_object_permissions(self.request, obj)
    #     return obj


def login(self, request, *args, **kwargs):
    return True
