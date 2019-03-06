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
from education.models import Course, CourseBody, CostUnit, Price, Workshop, WorkshopFile
from file_app.serializers.file_serializer import FileSerializer
from commons import serializers as cserializers
from education.serializers.price_serializer import PriceSerializer

'''
 .d8888b.   .d88888b.  888     888 8888888b.   .d8888b.  8888888888       .d8888b.  8888888888 8888888b.  8888888        d8888 888      8888888 8888888888P 8888888888 8888888b.  
d88P  Y88b d88P" "Y88b 888     888 888   Y88b d88P  Y88b 888             d88P  Y88b 888        888   Y88b   888         d88888 888        888         d88P  888        888   Y88b 
888    888 888     888 888     888 888    888 Y88b.      888             Y88b.      888        888    888   888        d88P888 888        888        d88P   888        888    888 
888        888     888 888     888 888   d88P  "Y888b.   8888888          "Y888b.   8888888    888   d88P   888       d88P 888 888        888       d88P    8888888    888   d88P 
888        888     888 888     888 8888888P"      "Y88b. 888                 "Y88b. 888        8888888P"    888      d88P  888 888        888      d88P     888        8888888P"  
888    888 888     888 888     888 888 T88b         "888 888                   "888 888        888 T88b     888     d88P   888 888        888     d88P      888        888 T88b   
Y88b  d88P Y88b. .d88P Y88b. .d88P 888  T88b  Y88b  d88P 888             Y88b  d88P 888        888  T88b    888    d8888888888 888        888    d88P       888        888  T88b  
 "Y8888P"   "Y88888P"   "Y88888P"  888   T88b  "Y8888P"  8888888888       "Y8888P"  8888888888 888   T88b 8888888 d88P     888 88888888 8888888 d8888888888 8888888888 888   T88b 
                                                                                                                                                                                                                                                                                     
'''                                                                                                                            

class CourseBodySerializer(cserializers.DynamicFieldsModelSerializer):
    class Meta:
        model = CourseBody
        fields = ('id', 'description', )
        extra_kwargs = {}


class CourseSerializer(cserializers.DynamicFieldsModelSerializer):
    description = CourseBodySerializer(source='body', read_only=True)
    price = PriceSerializer(required=False, read_only=True)
    # discount = serializers.SerializerMethodField(read_only=True)
    teacher = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Course
        fields = ('id', 'uuid', 'title', 'instructor', 'rate', 'body', 'timestamp', 'price', 'online')
        read_only_fields = ()
        extra_kwargs = {'instructor': {'write_only': True}, 'timestamp': {'write_only': True}}

    def get_teacher(self, obj):
        return US(obj.instructor, fields=('email', 'email')).data
    # def get_discount(self, obj):
    #     # today = datetime.date.now()
    #     if obj.price:
    #     else:
    #         return {}