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

class UnitField(serializers.Field):
    def to_representation(self, instance):
        # for client use

        ret = []
        # print(instance['email'])
        # for value in instance.unit.all:
        #     # print(value)
        #     tmp = {
        #         "unit_id": value.unit_id,
        #         "unit_name": value.get_id_display()
        #     }
        #     ret.append(tmp)
        return ret

    def to_internal_value(self, data):
        # For server-side use
        data = data.strip('[').rstrip(']')
        cost_unit = CostUnit.objects.create(unit_id = int(data)).save()
        unit = {'unit': cost_unit}
        return unit

class PriceSerializer(cserializers.DynamicFieldsModelSerializer):
    unit = UnitField(source='*')
    price = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Price
        fields = ('id', 'uuid', 'online', 'unit', 'cost', 'price')
        read_only_fields = ('uuid', 'price')
        extra_kwargs = {'cost': {'write_only': True}, 'cost': {'write_only': True}}
    
    def get_price(self, obj):
        return {'cost':obj.get_price('unit'), 'unit': 'Rial'}


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


'''
888       888  .d88888b.  8888888b.  888    d8P   .d8888b.  888    888  .d88888b.  8888888b.        .d8888b.  8888888888 8888888b.  8888888        d8888 888      8888888 8888888888P 8888888888 8888888b.  
888   o   888 d88P" "Y88b 888   Y88b 888   d8P   d88P  Y88b 888    888 d88P" "Y88b 888   Y88b      d88P  Y88b 888        888   Y88b   888         d88888 888        888         d88P  888        888   Y88b 
888  d8b  888 888     888 888    888 888  d8P    Y88b.      888    888 888     888 888    888      Y88b.      888        888    888   888        d88P888 888        888        d88P   888        888    888 
888 d888b 888 888     888 888   d88P 888d88K      "Y888b.   8888888888 888     888 888   d88P       "Y888b.   8888888    888   d88P   888       d88P 888 888        888       d88P    8888888    888   d88P 
888d88888b888 888     888 8888888P"  8888888b        "Y88b. 888    888 888     888 8888888P"           "Y88b. 888        8888888P"    888      d88P  888 888        888      d88P     888        8888888P"  
88888P Y88888 888     888 888 T88b   888  Y88b         "888 888    888 888     888 888                   "888 888        888 T88b     888     d88P   888 888        888     d88P      888        888 T88b   
8888P   Y8888 Y88b. .d88P 888  T88b  888   Y88b  Y88b  d88P 888    888 Y88b. .d88P 888             Y88b  d88P 888        888  T88b    888    d8888888888 888        888    d88P       888        888  T88b  
888P     Y888  "Y88888P"  888   T88b 888    Y88b  "Y8888P"  888    888  "Y88888P"  888              "Y8888P"  8888888888 888   T88b 8888888 d88P     888 88888888 8888888 d8888888888 8888888888 888   T88b 
                                                                                                                                                                                                                                                                                                                                                                                                              
'''

class WorkshopFileSerializerR(FileSerializer):
    class Meta:
        model = WorkshopFile
        fields = ('file', 'workshop_id', 'remark', 'timestamp')
        # extra_kwargs = {'workshop_id': {'write_only': True}}  

class WorkshopSerializer(CourseSerializer):
    workshop_files = WorkshopFileSerializerR(many = True, read_only = True)
    # files = serializers.SerializerMethodField(read_only=True)
    # workshop_files = serializers.SlugRelatedField(
    #     queryset = WorkshopFile.objects.all(),
    #     many=True,
    #     slug_field='workshop_id',
    #     allow_null = True
    # )
    class Meta:
        model = Workshop
        fields= ('id', 'uuid', 'title', 'instructor', 'rate', 'body', 'description', 'workshop_files', 'timestamp'
        , 'price', 'start_date', 'end_date', 'start_time', 'end_time', 'teacher', 'buyers')
        extra_kwargs = {'instructor': {'write_only': True}}

    # def get_files(self, obj):
    #     print(obj.workshop_files)
    #     return 'Null'
    #     # return WorkshopFileSerializer(obj.workshop_files, many=True)

class WorkshopFileSerializer(FileSerializer):
    workshop = WorkshopSerializer(read_only = True)
    class Meta:
        model = WorkshopFile
        fields = ('file', 'remark', 'timestamp', 'workshop')
        # extra_kwargs = {'workshop_id': {'write_only': True}}  
