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
from education.models import Discount, PersonalDiscount, DateDiscount, RaceDiscount
from django.shortcuts import get_object_or_404
from commons import serializers as cserializers




class DiscountSerializer(cserializers.DynamicFieldsModelSerializer):
    class Meta:
        model = Discount
        fields = ('id', 'percent', 'price')

class PersonalDiscountSerializer(DiscountSerializer):
    class Meta:
        model = PersonalDiscount
        fields = ('id', 'percent', 'price', 'coupon_text', 'person', 'start_data', 'end_date')

class DateDiscountSerializer(DiscountSerializer):
    class Meta:
        model = DateDiscount
        fields = ('id', 'percent', 'price', 'start_date', 'end_date')

class RaceDiscountSerializer(DateDiscountSerializer):
    class Meta:
        model = RaceDiscount
        fields = ('id', 'percent', 'price', 'start_date', 'end_date', 'coupon_text', 'limit')