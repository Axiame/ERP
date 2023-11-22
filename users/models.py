from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from datetime import datetime


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, birthday, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not first_name:
            raise ValueError('The first_name field must be set')
        if not last_name:
            raise ValueError('The last_name field must be set')
        if not birthday:
            raise ValueError('The birthday field must be set')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            birthday=birthday,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, birthday, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, first_name, last_name, birthday, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    birthday = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_professor = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['is_professor','first_name','last_name','birthday']


