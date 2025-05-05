from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.forms import ValidationError

class UserManager(BaseUserManager):
    
    def create_user(self,email,username,password=None,**extra_fields):
        
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,username,password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
    
        return self.create_user(email,username,password,**extra_fields)
    
class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.username
    
class Url(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    original_url = models.URLField(max_length=2048)
    short_url = models.CharField(max_length=255,blank=True,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    click_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['short_url'])
        ]
        
    def __str__(self):
        return self.original_url

        
    
class ClickEvent(models.Model):
    short_url = models.ForeignKey(
        Url,on_delete=models.CASCADE
    )
    accessed_at = models.DateTimeField(auto_now_add=True)
    ip_adress = models.GenericIPAddressField(blank=True,null=True)
    user_agent = models.TextField(blank=True,null=True)
    
    def __str__(self):
        return self.short_url