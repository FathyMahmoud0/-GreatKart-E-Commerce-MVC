from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class AccountManger(BaseUserManager):
    def create_user(self,first_name,last_name,username ,email, password=None):
        if not email:
            raise ValueError("The Email field must be set")
        
        if not username:
            raise ValueError("The username field must be set")
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name=last_name,
            
        )
        user.set_password(password) 
        user.save(using=self._db)
        return user
    
    def create_superuser(self,first_name,last_name,username ,email, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password=password,
            first_name = first_name,
            last_name=last_name,
        )
        
        user.is_active = True
        user.is_admin = True
        user.is_staff = True
        user.is_superadmin = True
        
        user.save(using=self._db)
        return user





class Accounts(AbstractBaseUser):
    
    email = models.EmailField(max_length=300,unique=True)
    username = models.CharField(max_length=60)
    first_name = models.CharField(max_length=90)
    last_name = models.CharField(max_length=60)
    phone = models.CharField(max_length=15)
    
    
    is_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    
    
    USERNAME_FIELD  = 'email'    
    REQUIRED_FIELDS = ['username','first_name','last_name'] 
    
    objects = AccountManger()
    
    class Meta:
        verbose_name = 'account'
        verbose_name_plural = 'accounts'
    
    def __str__(self):
        return self.email
    
    def has_perm(self,perm,obj=None):
        return self.is_admin
    
    def has_module_perms(self,add_label):
        return True
    
class Registar(models.Model):
    first_name = models.CharField(max_length=30,blank=False)
    last_name = models.CharField(max_length=30,blank=False)
    
    email = models.EmailField(max_length=90,unique=True,blank=False,null=False)
    
    gender = models.CharField(max_length=30)
    city = models.CharField(max_length=60)
    country = models.CharField(max_length=80)
    
    password = models.CharField(max_length=60,unique=True,blank=False,null=False)
    repeat_password = models.CharField(max_length=60,unique=True,blank=False,null=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = 'Registar'
        verbose_name_plural = 'Registars'
    



