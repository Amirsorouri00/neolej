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
import datetime
from django.contrib.auth import get_user_model
from rest_framework import serializers
from accounts.serializers.user_serializer import UserSerializer as US
from education.serializers.workshop_serializer import WorkshopSerializer as WS
from commons import serializers as cserializers

'''
888       888                  888               888                             8888888b.           888                  .d8888b.                   d8b          888 d8b                           
888   o   888                  888               888                             888   Y88b          888                 d88P  Y88b                  Y8P          888 Y8P                           
888  d8b  888                  888               888                             888    888          888                 Y88b.                                    888                               
888 d888b 888  .d88b.  888d888 888  888 .d8888b  88888b.   .d88b.  88888b.       888   d88P  8888b.  888888 .d88b.        "Y888b.    .d88b.  888d888 888  8888b.  888 888 88888888  .d88b.  888d888 
888d88888b888 d88""88b 888P"   888 .88P 88K      888 "88b d88""88b 888 "88b      8888888P"      "88b 888   d8P  Y8b          "Y88b. d8P  Y8b 888P"   888     "88b 888 888    d88P  d8P  Y8b 888P"   
88888P Y88888 888  888 888     888888K  "Y8888b. 888  888 888  888 888  888      888 T88b   .d888888 888   88888888            "888 88888888 888     888 .d888888 888 888   d88P   88888888 888     
8888P   Y8888 Y88..88P 888     888 "88b      X88 888  888 Y88..88P 888 d88P      888  T88b  888  888 Y88b. Y8b.          Y88b  d88P Y8b.     888     888 888  888 888 888  d88P    Y8b.     888     
888P     Y888  "Y88P"  888     888  888  88888P' 888  888  "Y88P"  88888P"       888   T88b "Y888888  "Y888 "Y8888        "Y8888P"   "Y8888  888     888 "Y888888 888 888 88888888  "Y8888  888     
                                                                   888                                                                                                                              
                                                                   888                                                                                                                              
                                                                   888
'''

from education.models import WorkshopRates

class RateWorkshopSerializer(cserializers.DynamicFieldsModelSerializer):
    user = US(read_only=True)
    workshop = WS(read_only=True)
    class Meta:
        model = WorkshopRates
        fields('id', 'uuid', 'user', 'workshop', 'rate')