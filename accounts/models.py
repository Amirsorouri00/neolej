from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager ## A new class is imported. ##
from django.utils.translation import ugettext_lazy as _


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




