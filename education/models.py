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

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class CourseBody(models.Model):
    description = models.TextField(blank=True, null=True) 

class Course(models.Model):
    uuid = models.UUIDField(db_index=True, unique=True, blank=True, null=True)
    title = models.CharField(max_length=511, blank=True, null=True)
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET(get_sentinel_user)) 
    rate = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(100), MinValueValidator(1)]
    )
    body = models.OneToOneField(CourseBody, blank=False, null=False, to_field=id)
    timestamp = models.DateTimeField(auto_now_add=True)
    price = models.ForeignKey() #see

    class Meta:
        db_table = 'education_course'
        managed = True
        verbose_name = u'Course'
        verbose_name_plural = u'Courses'

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
    uuid = models.UUIDField(db_index=True, unique=True, blank=True, null=True)
    unit = models.ForeignKey(CostUnit)
    cost = models.DecimalField(max_digits=10, decimal_places=3)

    def get_price(self, unit):
        return 1000

def percentage_validator(val):
    if val.endswith("%"):
       return float(val[:-1])/100
    else:
       try:
          return float(val)
       except ValueError:          
          raise ValidationError(
              _('%(value)s is not a valid pct'),
                params={'value': value},
           ) 

class Discount(models.Model):
    start_date = models.DateField(help_text=u'Start Day of the Discount')
    end_date = models.DateField(help_text=u'End Day of the Discount', blank=True, null=True)
    percent = models.StringField(validators=[percentage_validator])
    price = models.ForeignKey(Price, blank=True, null=True)



'''
██╗    ██╗ ██████╗ ██████╗ ██╗  ██╗███████╗██╗  ██╗ ██████╗ ██████╗      ██████╗ ██████╗ ██╗   ██╗██████╗ ███████╗███████╗
██║    ██║██╔═══██╗██╔══██╗██║ ██╔╝██╔════╝██║  ██║██╔═══██╗██╔══██╗    ██╔════╝██╔═══██╗██║   ██║██╔══██╗██╔════╝██╔════╝
██║ █╗ ██║██║   ██║██████╔╝█████╔╝ ███████╗███████║██║   ██║██████╔╝    ██║     ██║   ██║██║   ██║██████╔╝███████╗█████╗  
██║███╗██║██║   ██║██╔══██╗██╔═██╗ ╚════██║██╔══██║██║   ██║██╔═══╝     ██║     ██║   ██║██║   ██║██╔══██╗╚════██║██╔══╝  
╚███╔███╔╝╚██████╔╝██║  ██║██║  ██╗███████║██║  ██║╚██████╔╝██║         ╚██████╗╚██████╔╝╚██████╔╝██║  ██║███████║███████╗
 ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝          ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝
'''                                                                                                                          


class Workshop(Course):
    uuid = models.UUIDField(db_index=True, unique=True, blank=True, null=True)
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
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)



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
#     uuid = models.UUIDField(db_index=True, unique=True, blank=True, null=True)

#     file = models.FileField(upload_to=online_course_file_directory_path, blank=False, null=False)
#     course = models.ForeignKey(Online, on_delete=models.CASCADE)

    



