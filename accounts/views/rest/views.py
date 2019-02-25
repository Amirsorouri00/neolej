from accounts.serializers.admin_serializer import AdminSerializer as AS
from django.http import HttpResponse, JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, \
    parser_classes, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from accounts.models import User


'''
888      .d88888b.   .d8888b.  8888888 888b    888        d88P 888      .d88888b.   .d8888b.   .d88888b.  888     888 88888888888 
888     d88P" "Y88b d88P  Y88b   888   8888b   888       d88P  888     d88P" "Y88b d88P  Y88b d88P" "Y88b 888     888     888     
888     888     888 888    888   888   88888b  888      d88P   888     888     888 888    888 888     888 888     888     888     
888     888     888 888          888   888Y88b 888     d88P    888     888     888 888        888     888 888     888     888     
888     888     888 888  88888   888   888 Y88b888    d88P     888     888     888 888  88888 888     888 888     888     888     
888     888     888 888    888   888   888  Y88888   d88P      888     888     888 888    888 888     888 888     888     888     
888     Y88b. .d88P Y88b  d88P   888   888   Y8888  d88P       888     Y88b. .d88P Y88b  d88P Y88b. .d88P Y88b. .d88P     888     
88888888 "Y88888P"   "Y8888P88 8888888 888    Y888 d88P        88888888 "Y88888P"   "Y8888P88  "Y88888P"   "Y88888P"      888     
'''


from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return JsonResponse({
                'token': token.key,
                'user_uuid': user.uuid,
                # 'user_uuid': user.uuid_user.user_uuid.hex,
                'email': user.email
            }, safe=False, status = status.HTTP_202_ACCEPTED)
        else: return JsonResponse({'received data': request.POST, 'errors': serializer.errors}, safe=False, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def token_base_logout(request):
    if request.user.is_authenticated == False:
        return HttpResponse('User is already logged out')
    else:
        user = User.objects.get(email = request.user)
        Token.objects.filter(user=user).delete()
        token, created = Token.objects.get_or_create(user=user)

        return JsonResponse({
            'token': token.key,
            'user_id': user.uuid.hex,
            'email': user.email
        })

# @parser_classes((JSONParser,))
def test2(request, format=None):
    print(request.POST)
    serializer = AS(data = request.POST)

    print(serializer)
    print(serializer.is_valid())
    print(serializer.errors)
    print(serializer.validated_data)
    serializer.save()

    return JsonResponse({'received data': request.POST}, safe=False, status=200)
    