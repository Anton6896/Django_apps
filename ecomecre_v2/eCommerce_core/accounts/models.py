from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, username=None, active=True, staff=False, admin=False):
        if not email or password:
            raise ValueError("Must have an Email and Password!!")

        user_obj = self.model(
            email=self.normalize_email(email)
        )
        if username:
            # unique true so if any duplicate the db will show hte error
            user_obj.username = username
        user_obj.active = active
        user_obj.staff = staff
        user_obj.admin = admin
        user_obj.set_password(password)  # encode raw password
        user_obj.save(using=self._db)
        return user_obj

    def create_staff(self, email, password=None):
        user = self.create_user(email, password, staff=True)
        return user


class User(AbstractBaseUser):
    objects = MyUserManager()
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=50, unique=True, blank=True, null=True)
    full_name = models.CharField(max_length=200, blank=True, null=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    # email_confirmed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_active(self):
        return self.active

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        ...
