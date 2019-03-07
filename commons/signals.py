import uuid
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from accounts.models import User
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

@receiver(pre_save)
def all_models_validation(instance, *args, **kwargs):
#    instance.full_clean()
    print('all_models_are_validated')

'''
8888888888 8888888b.  888     888  .d8888b.        d8888 88888888888 8888888 .d88888b.  888b    888 
888        888  "Y88b 888     888 d88P  Y88b      d88888     888       888  d88P" "Y88b 8888b   888 
888        888    888 888     888 888    888     d88P888     888       888  888     888 88888b  888 
8888888    888    888 888     888 888           d88P 888     888       888  888     888 888Y88b 888 
888        888    888 888     888 888          d88P  888     888       888  888     888 888 Y88b888 
888        888    888 888     888 888    888  d88P   888     888       888  888     888 888  Y88888 
888        888  .d88P Y88b. .d88P Y88b  d88P d8888888888     888       888  Y88b. .d88P 888   Y8888 
8888888888 8888888P"   "Y88888P"   "Y8888P" d88P     888     888     8888888 "Y88888P"  888    Y888 
'''                                                                                                    
                                                                                                    
from education.models import Price, WorkshopRates, WorkshopPersonalDiscount, WorkshopDateDiscount, WorkshopRaceDiscount                                                                                                     

@receiver(post_save, sender=WorkshopRates)
def create_workshop_rate_UUID(sender, instance=None, created=True, **kwargs):
    if created:
        instance.uuid = uuid.uuid5(uuid.NAMESPACE_DNS, str(instance.id))
        instance.save()

@receiver(post_save, sender=Price)
def create_price_UUID(sender, instance=None, created=True, **kwargs):
    if created:
        instance.uuid = uuid.uuid5(uuid.NAMESPACE_DNS, str(instance.id))
        instance.save()

@receiver(post_save, sender=WorkshopPersonalDiscount)
def create_workshop_personal_discount_UUID(sender, instance=None, created=True, **kwargs):
    if created:
        instance.uuid = uuid.uuid5(uuid.NAMESPACE_DNS, str(instance.id))
        instance.save()

@receiver(post_save, sender=WorkshopDateDiscount)
def create_workshop_date_discount_UUID(sender, instance=None, created=True, **kwargs):
    if created:
        instance.uuid = uuid.uuid5(uuid.NAMESPACE_DNS, str(instance.id))
        instance.save()

@receiver(post_save, sender=WorkshopRaceDiscount)
def create_workshop_race_discount_UUID(sender, instance=None, created=True, **kwargs):
    if created:
        instance.uuid = uuid.uuid5(uuid.NAMESPACE_DNS, str(instance.id))
        instance.save()

from education.models import Workshop, WorkshopInvoice, WorkshopPayment, WorkshopRates

@receiver(post_save, sender=Workshop)
def create_workshop_UUID(sender, instance=None, created=True, **kwargs):
    if created:
        instance.uuid = uuid.uuid5(uuid.NAMESPACE_DNS, str(instance.id))
        instance.save()

@receiver(post_save, sender=WorkshopInvoice)
def create_workshop_invoice_UUID(sender, instance=None, created=True, **kwargs):
    if created:
        instance.uuid = uuid.uuid5(uuid.NAMESPACE_DNS, str(instance.id))
        instance.save()

@receiver(post_save, sender=WorkshopPayment)
def create_workshop_payment_UUID(sender, instance=None, created=True, **kwargs):
    if created:
        instance.uuid = uuid.uuid5(uuid.NAMESPACE_DNS, str(instance.id))
        instance.save()

# @receiver(post_save, sender=WorkshopRates)
# def create_workshop_UUID(sender, instance=None, created=True, **kwargs):
#     if created:
#         instance.uuid = uuid.uuid5(uuid.NAMESPACE_DNS, str(instance.id))
#         instance.save()

'''
888     888  .d8888b.  8888888888 8888888b.  
888     888 d88P  Y88b 888        888   Y88b 
888     888 Y88b.      888        888    888 
888     888  "Y888b.   8888888    888   d88P 
888     888     "Y88b. 888        8888888P"  
888     888       "888 888        888 T88b   
Y88b. .d88P Y88b  d88P 888        888  T88b  
 "Y88888P"   "Y8888P"  8888888888 888   T88b 
'''

@receiver(post_save, sender=User)
def create_user_UUID(sender, instance=None, created=False, **kwargs):
    if created:
        instance.uuid = uuid.uuid5(uuid.NAMESPACE_DNS, str(instance.id))
        instance.save()
