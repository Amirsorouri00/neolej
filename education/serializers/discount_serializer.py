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
from django.http import JsonResponse, HttpResponse
from education.models import Discount, PersonalDiscount, DateDiscount, RaceDiscount
from django.shortcuts import get_object_or_404
from commons import serializers as cserializers



'''
8888888b. 8888888 .d8888b.   .d8888b.   .d88888b.  888     888 888b    888 88888888888 
888  "Y88b  888  d88P  Y88b d88P  Y88b d88P" "Y88b 888     888 8888b   888     888     
888    888  888  Y88b.      888    888 888     888 888     888 88888b  888     888     
888    888  888   "Y888b.   888        888     888 888     888 888Y88b 888     888     
888    888  888      "Y88b. 888        888     888 888     888 888 Y88b888     888     
888    888  888        "888 888    888 888     888 888     888 888  Y88888     888     
888  .d88P  888  Y88b  d88P Y88b  d88P Y88b. .d88P Y88b. .d88P 888   Y8888     888     
8888888P" 8888888 "Y8888P"   "Y8888P"   "Y88888P"   "Y88888P"  888    Y888     888     
'''                                                                                       
                                                                                       
from education.models import Discount, PersonalDiscount, RaceDiscount, DateDiscount                                                                                    
class DiscountSerializer(cserializers.DynamicFieldsModelSerializer):
    class Meta:
        model = Discount
        fields = ('id', 'uuid', 'percent')

class PersonalDiscountSerializer(DiscountSerializer):
    class Meta:
        model = PersonalDiscount
        fields = ('id', 'uuid', 'percent', 'coupon_text', 'person', 'start_date', 'end_date')

class DateDiscountSerializer(DiscountSerializer):
    class Meta:
        model = DateDiscount
        fields = ('id', 'uuid', 'percent', 'start_date', 'end_date')

class RaceDiscountSerializer(DiscountSerializer):
    class Meta:
        model = RaceDiscount
        fields = ('id', 'uuid', 'percent', 'coupon_text', 'limit')