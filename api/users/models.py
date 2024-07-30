from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class CustomManager(BaseUserManager):
    def create_user(self, name, email, password=None):
        if not email:
            raise ValueError('User must haven an email address')
        
        user = self.model(
            email = self.normalize_email(email),
            name = name
        ) 

        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user
    
    def create_superuser(self, name, email, password=None):

        user = self.create_user(
            email = self.normalize_email(email),
            name = name,
            password=password,
        )
        
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superadmin = True
        user.save(using=self._db)
        
        return user
    


class CustomUser(AbstractBaseUser):
    name = models.CharField(max_length = 100)
    email = models.EmailField(max_length = 100, unique = True)

    #required 
    date_joined = models.DateTimeField(auto_now_add = True)
    is_admin = models.BooleanField(default = False)
    is_staff = models.BooleanField(default = False)
    is_active = models.BooleanField(default = False)
    is_superadmin = models.BooleanField(default = False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = CustomManager()

    class Meta:
        db_table = "Users"
        verbose_name = "Users"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True
    