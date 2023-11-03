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
            **extra_fields
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

    # TO DO : add automatisation of deactivation of expired contracts
    def deactivate_expired_contracts(self):
        expired_users = self.filter(is_active=True, end_contract__lte=datetime.now())
        expired_users.update(is_active=False)


class User(AbstractBaseUser, PermissionsMixin):
    uid = models.CharField(max_length=100, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    birthday = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    end_contract = models.DateTimeField(null=False, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    job = models.CharField(max_length=100, null=True, blank=True)
    manager = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True, related_name='managed_by')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'birthday']

    def generate_uid(self):
        first_initial = self.first_name[0].upper()
        last_initial = self.last_name[:5].upper()
        birthday = self.birthday.strftime('%d')

        base_uid = first_initial + last_initial + birthday

        uid = base_uid
        counter = 0
        while User.objects.filter(uid=uid).exists():
            counter += 1
            uid = base_uid + str(counter)
        return uid

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = self.generate_uid()
        super().save(*args, **kwargs)
