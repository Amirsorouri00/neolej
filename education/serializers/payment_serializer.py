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
from education.models import WorkshopPayment, WorkshopInvoice
from django.shortcuts import get_object_or_404
from commons import serializers as cserializers


'''
8888888b.     d8888 Y88b   d88P 888b     d888 8888888888 888b    888 88888888888 
888   Y88b   d88888  Y88b d88P  8888b   d8888 888        8888b   888     888     
888    888  d88P888   Y88o88P   88888b.d88888 888        88888b  888     888     
888   d88P d88P 888    Y888P    888Y88888P888 8888888    888Y88b 888     888     
8888888P" d88P  888     888     888 Y888P 888 888        888 Y88b888     888     
888      d88P   888     888     888  Y8P  888 888        888  Y88888     888     
888     d8888888888     888     888   "   888 888        888   Y8888     888     
888    d88P     888     888     888       888 8888888888 888    Y888     888     
'''                                                                                                                                                               

from education.serializers.discount_serializer import DiscountTypeSerializer
from education.models import AbstractInvoice, AbstractPayment
class AbstractPaymentSerializer(cserializers.DynamicFieldsModelSerializer):
    discount_type = DiscountTypeSerializer(source='*')
    class Meta:
        model = AbstractPayment
        fields = ('id', 'uuid', 'user', 'discount_type', 'pending')

class WorkshopPaymentSerializer(cserializers.DynamicFieldsModelSerializer):
    discount_type = DiscountTypeSerializer(source='*', required=False)
    class Meta:
        model = WorkshopPayment
        fields = ('id', 'uuid', 'user', 'discount_type', 'pending', 'workshop')
        read_only_fields = ['pending', 'id', 'uuid', 'discount_type']
        extra_kwargs = {'discount_type': {'required': False}}



'''
8888888 888b    888 888     888  .d88888b. 8888888 .d8888b.  8888888888 
  888   8888b   888 888     888 d88P" "Y88b  888  d88P  Y88b 888        
  888   88888b  888 888     888 888     888  888  888    888 888        
  888   888Y88b 888 Y88b   d88P 888     888  888  888        8888888    
  888   888 Y88b888  Y88b d88P  888     888  888  888        888        
  888   888  Y88888   Y88o88P   888     888  888  888    888 888        
  888   888   Y8888    Y888P    Y88b. .d88P  888  Y88b  d88P 888        
8888888 888    Y888     Y8P      "Y88888P" 8888888 "Y8888P"  8888888888 
'''

class AbstractInvoiceSerializer(cserializers.DynamicFieldsModelSerializer):
    class Meta:
        model = AbstractInvoice
        fields = ('id', 'uuid', 'amount_to_pay', 'index', 'due_date', 'payed_or_not', 'created_by')


class WorkshopInvoiceSerializer(AbstractInvoiceSerializer):
    payment = WorkshopPaymentSerializer(read_only = True)
    class Meta:
        model = WorkshopInvoice
        fields = ('id', 'uuid', 'amount_to_pay', 'index', 'due_date', 'payed_or_not', 'created_by', 'payment', 'logs', 'authority', 'ref_id')
        read_only_fields = ['payed_or_not', 'id', 'uuid', 'created_by', 'payment']