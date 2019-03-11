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
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

'''
 .d8888b.           888    8888888b.          d8b                  
d88P  Y88b          888    888   Y88b         Y8P                  
888    888          888    888    888                              
888         .d88b.  888888 888   d88P 888d888 888  .d8888b .d88b.  
888  88888 d8P  Y8b 888    8888888P"  888P"   888 d88P"   d8P  Y8b 
888    888 88888888 888    888        888     888 888     88888888 
Y88b  d88P Y8b.     Y88b.  888        888     888 Y88b.   Y8b.     
 "Y8888P88  "Y8888   "Y888 888        888     888  "Y8888P "Y8888  
'''                                                                   

from education.models import WorkshopDiscount
def get_price(user, workshop):
    cost = workshop.price.get_price('rial')
    discounts = WorkshopDiscount.objects.filter(workshops__id=workshop.id)
    user_discount = None
    discount_type = None
    for discount in discounts:
        if hasattr(discount, 'limit'):
            if discount.used_count < discount.limit:
                user_discount = discount
                discount_type = 'race'
            else:
                user_discount = None
            break
            print('race discount')
        elif hasattr(discount, 'person'):
            break
            print('personal discount')
        else:
            break
            print('date discount')
    response = {'cost': cost, 'discount': user_discount, 'discount_type' = discount_type}
    return response



                                                                   