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
from django.contrib.auth.models import AbstractUser, BaseUserManager ## A new class is imported. ##
from django.utils.translation import ugettext_lazy as _


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

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class Role(models.Model):
    '''
    The Role entries are managed by the system,
    automatically created via a Django data migration.
    '''
    STUDENT = 1
    TEACHER = 2
    SUPERVISOR = 3
    ADMIN = 4
    ROLE_CHOICES = (
        (STUDENT, 'student'),
        (TEACHER, 'teacher'),
        (SUPERVISOR, 'supervisor'),
        (ADMIN, 'admin'),
    )
    role_id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES)

    def __str__(self):
        return self.get_id_display()
    
    def get_id_display(self):
        for key, value in self.ROLE_CHOICES:
            if self.role_id == key:
                return value
        return 'unknown role.'

    def get_role(self):
        for key, value in self.ROLE_CHOICES:
            if self.role_id == value:
                return {'role_id':key, 'role_name': value}
        return 'unknown role.'

class User(AbstractUser):
    uuid = models.UUIDField(db_index=True, unique=True, blank=True, null=True)
    # username = None
    email = models.EmailField(_('email address'), unique=True)
    cell_phone = models.CharField(max_length=31, blank=True, null=True)
    roles = models.ManyToManyField(Role)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['cell_phone']

    objects = UserManager() 

    class Meta:
        db_table = 'accounts_user'
        managed = True
        verbose_name = u'User'
        verbose_name_plural = u'Users'
        # permissions = (("can_deliver_pizzas", "Can deliver pizzas"),)
        # Latest by priority descending, order_date ascending.
        # get_latest_by = ['-priority', 'order_date']
        # indexes = [
        #     models.Index(fields=['last_name', 'first_name']),
        #     models.Index(fields=['first_name'], name='first_name_idx'),
        # ]
        
    @property
    def popularity(self):
        likes = 12
        time = 12 #hours since created
        return likes / time if time > 0 else likes




