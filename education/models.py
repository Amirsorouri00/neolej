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
from django.core.validators import MaxValueValidator, MinValueValidator



'''
 .d8888b.   .d88888b.  888     888 8888888b.   .d8888b.  8888888888 .d8888b.  
d88P  Y88b d88P" "Y88b 888     888 888   Y88b d88P  Y88b 888       d88P  Y88b 
888    888 888     888 888     888 888    888 Y88b.      888       Y88b.      
888        888     888 888     888 888   d88P  "Y888b.   8888888    "Y888b.   
888        888     888 888     888 8888888P"      "Y88b. 888           "Y88b. 
888    888 888     888 888     888 888 T88b         "888 888             "888 
Y88b  d88P Y88b. .d88P Y88b. .d88P 888  T88b  Y88b  d88P 888       Y88b  d88P 
 "Y8888P"   "Y88888P"   "Y88888P"  888   T88b  "Y8888P"  8888888888 "Y8888P"  
                                                                              
'''

class CostUnit(models.Model):
    '''
    The CONSTUNIT entries are managed by the system,
    automatically created via a Django data migration.
    '''
    RIAL = 1
    DOLLOR = 2
    EURO = 3
    
    UNIT_CHOICES = (
        (RIAL, 'Rial'),
        (DOLLOR, 'Dollor'),
        (EURO, 'Euro'),
    )
    id = models.AutoField(primary_key=True)
    unit_id = models.PositiveSmallIntegerField(default=1, choices=UNIT_CHOICES)
    def __str__(self):
        return self.get_id_display()
    
    def get_id_display(self):
        for key, value in self.UNIT_CHOICES:
            if self.unit_id == key:
                return value
        return 'unknown unit.'

    def get_role(self):
        for key, value in self.UNIT_CHOICES:
            if self.unit_id == value:
                return {'unit_id':key, 'unit_name': value}
        return 'unknown unit.'

class Price(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(db_index=True, unique=True, blank=True, null=True)
    online = models.BooleanField(default=True, blank=False, null=False) 
    unit = models.ForeignKey(CostUnit, blank=True, null=True, on_delete=models.SET_NULL)
    cost = models.DecimalField(max_digits=10, decimal_places=3)

    def get_price(self, unit, user_uuid=None):
        # workshop = self.workshop_set.get()
        return self.cost

class CourseBody(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.TextField(blank=True, null=True) 

def get_sentinel_user():
    return get_user_model().objects.get_or_create(email = 'deleted',username='deleted', password=123456)[0]

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(db_index=True, unique=True, blank=True, null=True)
    title = models.CharField(max_length=511, blank=True, null=True)
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET(get_sentinel_user), related_name='course_instructor')
    rate = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(100), MinValueValidator(1)]
    )
    rate_numbers = models.IntegerField(default=0, blank=False, null=False)
    body = models.OneToOneField(CourseBody, blank=True, null=True, on_delete=models.SET_NULL)
    online = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    prepayment = models.BooleanField(default=False) # installment or not
    prepayment_percent = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(100), MinValueValidator(1)]
    )
    price = models.ForeignKey(Price, blank=True, null=True, on_delete=models.SET_NULL) 
    buyers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    # could have installement or not

    class Meta:
        db_table = 'education_course'
        managed = True
        verbose_name = u'Course'
        verbose_name_plural = u'Courses'

# def percentage_validator(val):
#     if val.endswith("%"):
#        return float(val[:-1])/100
#     else:
#        try:
#           return float(val)
#        except ValueError:          
#           raise ValidationError(
#               _('%(value)s is not a valid pct'),
#                 params={'value': value},
#            ) 




'''
888       888  .d88888b.  8888888b.  888    d8P   .d8888b.  888    888  .d88888b.  8888888b.        .d8888b.   .d88888b.  888     888 8888888b.   .d8888b.  8888888888 
888   o   888 d88P" "Y88b 888   Y88b 888   d8P   d88P  Y88b 888    888 d88P" "Y88b 888   Y88b      d88P  Y88b d88P" "Y88b 888     888 888   Y88b d88P  Y88b 888        
888  d8b  888 888     888 888    888 888  d8P    Y88b.      888    888 888     888 888    888      888    888 888     888 888     888 888    888 Y88b.      888        
888 d888b 888 888     888 888   d88P 888d88K      "Y888b.   8888888888 888     888 888   d88P      888        888     888 888     888 888   d88P  "Y888b.   8888888    
888d88888b888 888     888 8888888P"  8888888b        "Y88b. 888    888 888     888 8888888P"       888        888     888 888     888 8888888P"      "Y88b. 888        
88888P Y88888 888     888 888 T88b   888  Y88b         "888 888    888 888     888 888             888    888 888     888 888     888 888 T88b         "888 888        
8888P   Y8888 Y88b. .d88P 888  T88b  888   Y88b  Y88b  d88P 888    888 Y88b. .d88P 888             Y88b  d88P Y88b. .d88P Y88b. .d88P 888  T88b  Y88b  d88P 888        
888P     Y888  "Y88888P"  888   T88b 888    Y88b  "Y8888P"  888    888  "Y88888P"  888              "Y8888P"   "Y88888P"   "Y88888P"  888   T88b  "Y8888P"  8888888888 
                                                                                                                                                                                                                                                                                                                     
'''                                                                                                                          

class Workshop(Course):
    city = models.CharField(max_length=255)
    start_date = models.DateField(help_text=u'Start Day of the Workshop')
    end_date = models.DateField(help_text=u'End Day of the Workshop', blank=True, null=True)
    start_time = models.TimeField(help_text=u'Start Time of the Workshop')
    end_time = models.TimeField(help_text=u'End Time of the Workshop', blank=True, null=True)
    
    # from django.contrib.gis.geos import Point
    # from location_field.models.spatial import LocationField
    # location = LocationField(based_fields=['city'], zoom=7, default=Point(1.0, 1.0))
    # objects = models.GeoManager()

from file_app.models import File
def workshop_file_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/file_<remark>/<filename>
    return 'workshop_{0}/{1}'.format(instance.workshop.uuid, filename)
    # return 'workshop_{0}/{1}'.format('instance.workshop.uuid', filename)

class WorkshopFile(File):
    file = models.FileField(upload_to=workshop_file_directory_path, blank=False, null=False)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name='workshop_files')
                                                 






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

class AbstractDiscount(models.Model):
    # percent = models.CharField(validators=[percentage_validator])
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(db_index=True, unique=True, blank=True, null=True)
    percent = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(100), MinValueValidator(1)]
    )
    amount = models.IntegerField(
        default=0,
    )
    used = models.BooleanField(default=False)
    # price = models.ForeignKey(Price, blank=True, null=True, on_delete=models.CASCADE, related_name='price_discount')

class WorkshopDiscount(AbstractDiscount):
    workshops = models.ManyToManyField(Workshop, blank=True)
    active = models.BooleanField(default=False)

class WorkshopPersonalDiscount(WorkshopDiscount):
    coupon_text = models.CharField(max_length=15, blank=False, null=False)
    person = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=False, on_delete=models.SET(get_sentinel_user))
    start_date = models.DateField(help_text=u'Start Day of the Discount', blank=True, null=True)
    end_date = models.DateField(help_text=u'End Day of the Discount', blank=True, null=True)

class WorkshopDateDiscount(WorkshopDiscount):
    start_date = models.DateField(help_text=u'Start Day of the Discount')
    end_date = models.DateField(help_text=u'End Day of the Discount', blank=True, null=True)
    # Models.many to many for workshop or online courses

class WorkshopRaceDiscount(WorkshopDiscount):
    coupon_text = models.CharField(max_length=15, blank=True, null=True)
    limit = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    used_count = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    # Models. foreignkey field for workhsop or online courses

class DiscountType(models.Model):
    '''
    The CONSTUNIT entries are managed by the system,
    automatically created via a Django data migration.
    '''
    RACEDISCOUNT = 1
    DATEDISCOUNT = 2
    PERSONALDISCOUNT = 3
    
    DISCOUNT_CHOICES = (
        (RACEDISCOUNT, 'RaceDiscount'),
        (DATEDISCOUNT, 'DateDiscount'),
        (PERSONALDISCOUNT, 'PersonalDiscount'),
    )
    id = models.AutoField(primary_key=True)
    type_id = models.PositiveSmallIntegerField(default=1, choices=DISCOUNT_CHOICES)
    def __str__(self):
        return self.get_id_display()
    
    def get_id_display(self):
        for key, value in self.DISCOUNT_CHOICES:
            if self.type_id == key:
                return value
        return 'unknown unit.'

    def get_role(self):
        for key, value in self.DISCOUNT_CHOICES:
            if self.type_id == value:
                return {'discount_type_id':key, 'discount_type': value}
        return 'unknown unit.'



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

class AbstractPayment(models.Model):
    uuid = models.UUIDField(db_index=True, unique=True, blank=True, null=True)
    discount_type = models.ForeignKey(DiscountType, blank=True, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=False, on_delete=models.SET(get_sentinel_user)) # SetNull
    pending = models.BooleanField(default=True)


class WorkshopPayment(AbstractPayment):
    workshop = models.ForeignKey(Workshop, blank=False, null=False, on_delete = models.CASCADE)



'''
8888888                            d8b                  
  888                              Y8P                  
  888                                                   
  888   88888b.  888  888  .d88b.  888  .d8888b .d88b.  
  888   888 "88b 888  888 d88""88b 888 d88P"   d8P  Y8b 
  888   888  888 Y88  88P 888  888 888 888     88888888 
  888   888  888  Y8bd8P  Y88..88P 888 Y88b.   Y8b.     
8888888 888  888   Y88P    "Y88P"  888  "Y8888P "Y8888  
'''

class AbstractInvoice(models.Model):
    uuid = models.UUIDField(db_index=True, unique=True, blank=True, null=True)
    amount_to_pay = models.DecimalField(max_digits=10, decimal_places=3)
    index = models.IntegerField(default=1, blank=False, null=False)
    due_date = models.DateField(help_text=u'The day that user must pay.') # what's next if he doesn't pay in the day??!!
    payed_or_not = models.BooleanField(default=False)     
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL) # SetNull                                                  
                                                        
class WorkshopInvoice(AbstractInvoice):
    payment = models.ForeignKey(WorkshopPayment, blank=True, null=True, db_index=True, related_name='invoice', on_delete=models.SET_NULL) # If the workshop price doesn't match the total added 
    logs = models.CharField(max_length=127, blank=True, null=True)
    authority = models.CharField(max_length=127, blank=True, null=True)
    ref_id = models.CharField(max_length=127, blank=True, null=True)
    discount_amount = models.IntegerField(
        default=0,
    )






# '''
# 888                            888888b.                              
# 888                            888  "88b                             
# 888                            888  .88P                             
# 888      .d88b.   .d88b.       8888888K.  888  888 888  888 .d8888b  
# 888     d88""88b d88P"88b      888  "Y88b 888  888 888  888 88K      
# 888     888  888 888  888      888    888 888  888 888  888 "Y8888b. 
# 888     Y88..88P Y88b 888      888   d88P Y88b 888 Y88b 888      X88 
# 88888888 "Y88P"   "Y88888      8888888P"   "Y88888  "Y88888  88888P' 
#                       888                               888          
#                  Y8b d88P                          Y8b d88P          
#                   "Y88P"                            "Y88P"               
# '''

# class BoughtCourses(models.Model):
#     id = models.AutoField(primary_key=True)
#     payment = models.ForeignKey(Payment, blank = True, null = True)
#     buyers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)                                                                                                                                    
                                                                                 



'''
888     888                                8888888b.           888                     
888     888                                888   Y88b          888                     
888     888                                888    888          888                     
888     888 .d8888b   .d88b.  888d888      888   d88P  8888b.  888888 .d88b.  .d8888b  
888     888 88K      d8P  Y8b 888P"        8888888P"      "88b 888   d8P  Y8b 88K      
888     888 "Y8888b. 88888888 888          888 T88b   .d888888 888   88888888 "Y8888b. 
Y88b. .d88P      X88 Y8b.     888          888  T88b  888  888 Y88b. Y8b.          X88 
 "Y88888P"   88888P'  "Y8888  888          888   T88b "Y888888  "Y888 "Y8888   88888P' 
'''

class WorkshopRates(models.Model):
    uuid = models.UUIDField(db_index=True, unique=True, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=False, on_delete=models.CASCADE, related_name='user_rate')
    workshop = models.ForeignKey(Workshop, blank=False, null=False, db_index=True, on_delete=models.CASCADE, related_name='course_user_rate')
    rate = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(100), MinValueValidator(1)],
        blank=False,
        null=False
    )

# class CourseRates(models.Model):
#     uuid = models.UUIDField(db_index=True, unique=True, blank=True, null=True)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=False, on_delete=models.CASCADE, related_name='user_rate')
#     course = models.ForeignKey(Workshop, blank=False, null=False, on_delete=models.CASCADE, related_name='course_user_rate')
#     rate = models.IntegerField(
#         default=0,
#         validators=[MaxValueValidator(100), MinValueValidator(1)],
#         blank=False,
#         null=False
#     )



'''
 .d88888b.  888b    888 888      8888888 888b    888 8888888888       .d8888b.   .d88888b.  888     888 8888888b.   .d8888b.  8888888888 
d88P" "Y88b 8888b   888 888        888   8888b   888 888             d88P  Y88b d88P" "Y88b 888     888 888   Y88b d88P  Y88b 888        
888     888 88888b  888 888        888   88888b  888 888             888    888 888     888 888     888 888    888 Y88b.      888        
888     888 888Y88b 888 888        888   888Y88b 888 8888888         888        888     888 888     888 888   d88P  "Y888b.   8888888    
888     888 888 Y88b888 888        888   888 Y88b888 888             888        888     888 888     888 8888888P"      "Y88b. 888        
888     888 888  Y88888 888        888   888  Y88888 888             888    888 888     888 888     888 888 T88b         "888 888        
Y88b. .d88P 888   Y8888 888        888   888   Y8888 888             Y88b  d88P Y88b. .d88P Y88b. .d88P 888  T88b  Y88b  d88P 888        
 "Y88888P"  888    Y888 88888888 8888888 888    Y888 8888888888       "Y8888P"   "Y88888P"   "Y88888P"  888   T88b  "Y8888P"  8888888888 
                                                                                                                                         
'''

# def online_course_file_directory_path(instance, filename):
#     # file will be uploaded to MEDIA_ROOT/file_<remark>/<filename>
#     return 'onlineCourse_{0}/{1}'.format(instance.CourseUUID, filename)

# class Online(Course, File):

#     file = models.FileField(upload_to=online_course_file_directory_path, blank=False, null=False)
#     course = models.ForeignKey(Online, on_delete=models.CASCADE)

                                                                                       