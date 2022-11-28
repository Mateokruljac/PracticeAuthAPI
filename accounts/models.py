from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name,username, password=None,password2 = None):
        """
        Creates and saves a User with the given email, first_name,
        last_name, username and password.
        """
        if not email or not username:
            raise ValueError('Users must have an email address and username!')

        user = self.model(
            first_name = first_name,
            last_name = last_name,
            username = username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, username, password=None,password2 = None):
        """
        Creates and saves a User with the given email, first_name,
        last_name, username and password.
        """
        user = self.create_user(
            email = email,
            first_name = first_name,
            last_name = last_name,
            username = username,
            password = password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


#Custom User Model
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(verbose_name="First name",max_length = 255)
    last_name = models.CharField(verbose_name="Last name",max_length = 255)
    username = models.CharField(verbose_name="Username",max_length = 255, unique = True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name',"last_name","username"]

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin