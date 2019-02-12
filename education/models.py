from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator


'''
 ██████╗ ██████╗ ██╗   ██╗██████╗ ███████╗███████╗
██╔════╝██╔═══██╗██║   ██║██╔══██╗██╔════╝██╔════╝
██║     ██║   ██║██║   ██║██████╔╝███████╗█████╗  
██║     ██║   ██║██║   ██║██╔══██╗╚════██║██╔══╝  
╚██████╗╚██████╔╝╚██████╔╝██║  ██║███████║███████╗
 ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝
'''                                               


class CourseBody(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.TextField(blank=True, null=True) 

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
    online_or_workshop = models.BooleanField(default=True, blank=False, null=False) 
    unit = models.ForeignKey(CostUnit, blank=True, null=True, on_delete=models.SET_NULL)
    cost = models.DecimalField(max_digits=10, decimal_places=3)

    def get_price(self, unit):
        return self.cost


def get_sentinel_user():
    return get_user_model().objects.get_or_create(email = 'deleted',username='deleted', password=123456)[0]

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(db_index=True, unique=True, blank=True, null=True)
    title = models.CharField(max_length=511, blank=True, null=True)
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET(get_sentinel_user)) 
    rate = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(100), MinValueValidator(1)]
    )
    body = models.OneToOneField(CourseBody, blank=True, null=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)
    price = models.ForeignKey(Price, blank=True, null=True, on_delete=models.SET_NULL) 

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

class Discount(models.Model):
    # percent = models.CharField(validators=[percentage_validator])
    id = models.AutoField(primary_key=True)
    percent = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(100), MinValueValidator(1)]
    )
    price = models.ForeignKey(Price, blank=True, null=True, on_delete=models.CASCADE)

class PersonalDiscount(Discount):
    coupon_text = models.CharField(max_length=15, blank=False, null=False)
    person = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=False, on_delete=models.SET(get_sentinel_user))
    start_date = models.DateField(help_text=u'Start Day of the Discount', blank=True, null=True)
    end_date = models.DateField(help_text=u'End Day of the Discount', blank=True, null=True)

class DateDiscount(Discount):
    start_date = models.DateField(help_text=u'Start Day of the Discount')
    end_date = models.DateField(help_text=u'End Day of the Discount', blank=True, null=True)

class RaceDiscount(DateDiscount):
    coupon_text = models.CharField(max_length=15, blank=True, null=True)
    limit = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])



'''
██╗    ██╗ ██████╗ ██████╗ ██╗  ██╗███████╗██╗  ██╗ ██████╗ ██████╗      ██████╗ ██████╗ ██╗   ██╗██████╗ ███████╗███████╗
██║    ██║██╔═══██╗██╔══██╗██║ ██╔╝██╔════╝██║  ██║██╔═══██╗██╔══██╗    ██╔════╝██╔═══██╗██║   ██║██╔══██╗██╔════╝██╔════╝
██║ █╗ ██║██║   ██║██████╔╝█████╔╝ ███████╗███████║██║   ██║██████╔╝    ██║     ██║   ██║██║   ██║██████╔╝███████╗█████╗  
██║███╗██║██║   ██║██╔══██╗██╔═██╗ ╚════██║██╔══██║██║   ██║██╔═══╝     ██║     ██║   ██║██║   ██║██╔══██╗╚════██║██╔══╝  
╚███╔███╔╝╚██████╔╝██║  ██║██║  ██╗███████║██║  ██║╚██████╔╝██║         ╚██████╗╚██████╔╝╚██████╔╝██║  ██║███████║███████╗
 ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝          ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝
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
    return 'workshop_{0}/{1}'.format(instance.workshopUUID, filename)

class WorkshopFile(models.Model):
    file = models.FileField(upload_to=workshop_file_directory_path, blank=False, null=False)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name='workshop_files')



'''
 ██████╗ ███╗   ██╗██╗     ██╗███╗   ██╗███████╗     ██████╗ ██████╗ ██╗   ██╗██████╗ ███████╗███████╗
██╔═══██╗████╗  ██║██║     ██║████╗  ██║██╔════╝    ██╔════╝██╔═══██╗██║   ██║██╔══██╗██╔════╝██╔════╝
██║   ██║██╔██╗ ██║██║     ██║██╔██╗ ██║█████╗      ██║     ██║   ██║██║   ██║██████╔╝███████╗█████╗  
██║   ██║██║╚██╗██║██║     ██║██║╚██╗██║██╔══╝      ██║     ██║   ██║██║   ██║██╔══██╗╚════██║██╔══╝  
╚██████╔╝██║ ╚████║███████╗██║██║ ╚████║███████╗    ╚██████╗╚██████╔╝╚██████╔╝██║  ██║███████║███████╗
 ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚═╝╚═╝  ╚═══╝╚══════╝     ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝
'''

# def online_course_file_directory_path(instance, filename):
#     # file will be uploaded to MEDIA_ROOT/file_<remark>/<filename>
#     return 'onlineCourse_{0}/{1}'.format(instance.CourseUUID, filename)

# class Online(Course, File):

#     file = models.FileField(upload_to=online_course_file_directory_path, blank=False, null=False)
#     course = models.ForeignKey(Online, on_delete=models.CASCADE)

'''
888                            888888b.                              
888                            888  "88b                             
888                            888  .88P                             
888      .d88b.   .d88b.       8888888K.  888  888 888  888 .d8888b  
888     d88""88b d88P"88b      888  "Y88b 888  888 888  888 88K      
888     888  888 888  888      888    888 888  888 888  888 "Y8888b. 
888     Y88..88P Y88b 888      888   d88P Y88b 888 Y88b 888      X88 
88888888 "Y88P"   "Y88888      8888888P"   "Y88888  "Y88888  88888P' 
                      888                               888          
                 Y8b d88P                          Y8b d88P          
                  "Y88P"                            "Y88P"               
'''

class BoughtCourses(models.Model):
    id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=False, on_delete=models.DO_NOTHING) 




