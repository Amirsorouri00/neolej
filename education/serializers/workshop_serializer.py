import datetime
from django.contrib.auth import get_user_model
from rest_framework import serializers
from accounts.serializers.user_serializer import UserSerializer as US
from education.models import Course, CourseBody, CostUnit, Price, Workshop, WorkshopFile
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
        model = CourseBody
        fields = ('id', 'description', )
        extra_kwargs = {}

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
        fields = ('id', 'uuid', 'online_or_workshop', 'unit', 'cost', 'price')
        read_only_fields = ('uuid', 'price')
        extra_kwargs = {'cost': {'write_only': True}, 'cost': {'write_only': True}}
    
    def get_price(self, obj):
        return {'cost':obj.get_price(), 'unit': 'Rial'}

class CourseSerializer(cserializers.DynamicFieldsModelSerializer):
    description = CourseBodySerializer(source='body', read_only=True)
    price = PriceSerializer(required=False, read_only=True)
    teacher = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Course
        fields = ('id', 'uuid', 'title', 'instructor', 'rate', 'body', 'timestamp', 'price' )
        read_only_fields = ()
        extra_kwargs = {'instructor': {'write_only': True}, 'timestamp': {'write_only': True}}

    def get_teacher(self, obj):
        return US(obj.instructor, fields=('email', 'email')).data


'''
██╗    ██╗ ██████╗ ██████╗ ██╗  ██╗███████╗██╗  ██╗ ██████╗ ██████╗     ███████╗███████╗██████╗ ██╗ █████╗ ██╗     ██╗███████╗███████╗██████╗ 
██║    ██║██╔═══██╗██╔══██╗██║ ██╔╝██╔════╝██║  ██║██╔═══██╗██╔══██╗    ██╔════╝██╔════╝██╔══██╗██║██╔══██╗██║     ██║╚══███╔╝██╔════╝██╔══██╗
██║ █╗ ██║██║   ██║██████╔╝█████╔╝ ███████╗███████║██║   ██║██████╔╝    ███████╗█████╗  ██████╔╝██║███████║██║     ██║  ███╔╝ █████╗  ██████╔╝
██║███╗██║██║   ██║██╔══██╗██╔═██╗ ╚════██║██╔══██║██║   ██║██╔═══╝     ╚════██║██╔══╝  ██╔══██╗██║██╔══██║██║     ██║ ███╔╝  ██╔══╝  ██╔══██╗
╚███╔███╔╝╚██████╔╝██║  ██║██║  ██╗███████║██║  ██║╚██████╔╝██║         ███████║███████╗██║  ██║██║██║  ██║███████╗██║███████╗███████╗██║  ██║
 ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝         ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚══════╝╚═╝╚══════╝╚══════╝╚═╝  ╚═╝
'''


class WorkshopFileSerializer(FileSerializer):
    class Meta:
        model = WorkshopFile
        fields = ('file', 'workshop', )
        extra_kwargs = {'workshop': {'write_only': True}}  

class WorkshopSerializer(CourseSerializer):
    # workshop_files = WorkshopFileSerializer(many = True, read_only = True)
    # files = serializers.SerializerMethodField(read_only=True)
    workshop_files = serializers.SlugRelatedField(
        queryset = WorkshopFile.objects.all(),
        many=True,
        slug_field='workshop_id',
        allow_null = True
    )
    class Meta:
        model = Workshop
        fields= ('id', 'uuid', 'title', 'instructor', 'rate', 'body', 'description', 'timestamp'
        , 'price', 'start_date', 'end_date', 'workshop_files', 'start_time', 'end_time', 'teacher')
        extra_kwargs = {'instructor': {'write_only': True}}
    
    # def get_files(self, obj):
    #     print(obj.workshop_files)
    #     return 'Null'
    #     # return WorkshopFileSerializer(obj.workshop_files, many=True)