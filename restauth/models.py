from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class EmailAccountManager(UserManager):
    def create_user(self, first_name, last_name, email, password = None):
        if not email:
            raise ValueError('User must have an eamil to register')
        
        user = self.model(
            email = self.normalize_email(email)
        )
        user.set_password(password)
        user.first_name = first_name
        user.last_name = last_name
        user.save(using = self._db)
        return user
    
    def create_superuser(self, email, password):
        user = self.model(
            email = self.normalize_email(email)
        )
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using = self._db)
        return user


class EmailAccount(AbstractUser, models.Model):
    username = models.NOT_PROVIDED
    email = models.EmailField('Email Address', unique = True)
    phone_number = models.CharField(max_length = 15, null = True, blank = True)
    address = models.CharField(max_length = 255, null = True, blank = True)
    
    USERNAME_FIELD: 'email'
    REQUIRED_FIELDS: None
    
    objects = EmailAccountManager()
    
    def __str__(self):
        return self.email