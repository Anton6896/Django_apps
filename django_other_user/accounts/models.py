from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not (email or password):
            raise ValueError("Must have an Email and Password!!")

        user_obj = self.model(
            email=self.normalize_email(email)
        )
        user_obj.set_password(password)

        user_obj.save(using=self._db)
        return user_obj

    def create_staff_user(self, email, password):
        user = self.create_user(email, password)
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    objects = MyUserManager()
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=50, unique=True, blank=True, null=True)
    full_name = models.CharField(max_length=200, blank=True, null=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)  # superuser
    active = models.BooleanField(default=True)
    email_confirmed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.full_name if self.full_name else self.email

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
        return self.full_name if self.full_name else self.email

    def get_short_name(self):
        ...

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
