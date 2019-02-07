import datetime
from django.contrib.auth import get_user_model
from rest_framework import serializers
from education.models import Course, CostUnit, Price, Workshop, WorkshopFile
from file_app.serializers.file_serializer import FileSerializer
from commons import serializers as cserializers


'''
 ██████╗ ██████╗ ██╗   ██╗██████╗ ███████╗███████╗    ███████╗███████╗██████╗ ██╗ █████╗ ██╗     ██╗███████╗███████╗██████╗ 
██╔════╝██╔═══██╗██║   ██║██╔══██╗██╔════╝██╔════╝    ██╔════╝██╔════╝██╔══██╗██║██╔══██╗██║     ██║╚══███╔╝██╔════╝██╔══██╗
██║     ██║   ██║██║   ██║██████╔╝███████╗█████╗      ███████╗█████╗  ██████╔╝██║███████║██║     ██║  ███╔╝ █████╗  ██████╔╝
██║     ██║   ██║██║   ██║██╔══██╗╚════██║██╔══╝      ╚════██║██╔══╝  ██╔══██╗██║██╔══██║██║     ██║ ███╔╝  ██╔══╝  ██╔══██╗
╚██████╗╚██████╔╝╚██████╔╝██║  ██║███████║███████╗    ███████║███████╗██║  ██║██║██║  ██║███████╗██║███████╗███████╗██║  ██║
 ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝    ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚══════╝╚═╝╚══════╝╚══════╝╚═╝  ╚═╝
'''                                                                                                                            

class CourseBodySerializer(cserializers.DynamicFieldsModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'description', )
        extra_kwargs = {'id': {'write_only': True}}

class UnitField(serializers.Field):
    def to_representation(self, instance):
        # for client use

        ret = []
        # print(instance['email'])
        for value in instance.units.all():
            # print(value)
            tmp = {
                "unit_id": value.unit_id,
                "unit_name": value.get_id_display()
            }
            ret.append(tmp)
        return ret

    def to_internal_value(self, data):
        # For server-side use

        data = data.strip('[').rstrip(']')
        units = {'units': [CostUnit(unit_id = int(val)) for val in data.split(',')]}
        return units

class PriceSerializer(cserializers.DynamicFieldsModelSerializer):
    unit = UnitField(source='*')
    price = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Price
        fields = ('id', 'uuid', 'unit', 'cost', 'price')
        read_only_fields = ('uuid', 'price')
        extra_kwargs = {'id': {'write_only': True}, 'cost': {'write_only': True}, 'cost': {'write_only': True}}
    
    def get_price(self, obj):
        return {'cost':obj.get_price(), 'unit': 'Rial'}

class CourseSerializer(cserializers.DynamicFieldsModelSerializer):
    body = CourseBodySerializer(source='*')
    price = PriceSerializer(read_only=True)
    teacher = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Course
        fields = ('id', 'uuid', 'title', 'instructor', 'rate', 'body', 'timestamp', 'price' )
        read_only_fields = ()
        extra_kwargs = {'id': {'write_only': True}, 'instructor': {'write_only': True}, 'timestamp': {'write_only': True}}

    def get_teacher(self, obj):
        return obj.instructor.uuid


'''
██╗    ██╗ ██████╗ ██████╗ ██╗  ██╗███████╗██╗  ██╗ ██████╗ ██████╗     ███████╗███████╗██████╗ ██╗ █████╗ ██╗     ██╗███████╗███████╗██████╗ 
██║    ██║██╔═══██╗██╔══██╗██║ ██╔╝██╔════╝██║  ██║██╔═══██╗██╔══██╗    ██╔════╝██╔════╝██╔══██╗██║██╔══██╗██║     ██║╚══███╔╝██╔════╝██╔══██╗
██║ █╗ ██║██║   ██║██████╔╝█████╔╝ ███████╗███████║██║   ██║██████╔╝    ███████╗█████╗  ██████╔╝██║███████║██║     ██║  ███╔╝ █████╗  ██████╔╝
██║███╗██║██║   ██║██╔══██╗██╔═██╗ ╚════██║██╔══██║██║   ██║██╔═══╝     ╚════██║██╔══╝  ██╔══██╗██║██╔══██║██║     ██║ ███╔╝  ██╔══╝  ██╔══██╗
╚███╔███╔╝╚██████╔╝██║  ██║██║  ██╗███████║██║  ██║╚██████╔╝██║         ███████║███████╗██║  ██║██║██║  ██║███████╗██║███████╗███████╗██║  ██║
 ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝         ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚══════╝╚═╝╚══════╝╚══════╝╚═╝  ╚═╝
'''


class WorkshopFileSerializer(serializers.ModelSerializer, FileSerializer):
    class Meta:
        model = WorkshopFile
        fields = ('file', 'workshop', )
        extra_kwargs = {'id': {'write_only': True}, 'workshop': {'write_only': True}}  

class WorkshopSerializer(cserializers.DynamicFieldsModelSerializer):
    files = WorkshopFileSerializer(many = True, read_only = True)
    class Meta:
        model: Workshop
        fields= ('id', 'uuid', 'city', 'start_date', 'end_date', 'start_time', 'end_time', 'workshop', 'files')                    
        read_only_fields = ()
        extra_kwargs = {'id': {'write_only': True}, 'workshop': {'write_only': True}}  

                                                                                                        
'''
                               888               888                        
                               888               888                        
                               888               888                        
888  888  888  .d88b.  888d888 888  888 .d8888b  88888b.   .d88b.  88888b.  
888  888  888 d88""88b 888P"   888 .88P 88K      888 "88b d88""88b 888 "88b 
888  888  888 888  888 888     888888K  "Y8888b. 888  888 888  888 888  888 
Y88b 888 d88P Y88..88P 888     888 "88b      X88 888  888 Y88..88P 888 d88P 
 "Y8888888P"   "Y88P"  888     888  888  88888P' 888  888  "Y88P"  88888P"  
                                                                   888      
                                                                   888      
                                                                   888                                                                                                              
'''                                                                   