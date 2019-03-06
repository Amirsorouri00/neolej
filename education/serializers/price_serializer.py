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
from education.models import Price
from commons import serializers as cserializers

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
        extra_kwargs = {'cost': {'write_only': True}, 'unit': {'write_only': True}}
    
    def get_price(self, obj):
        return {'cost':obj.get_price('unit'), 'unit': 'Rial'}