from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission
from django.utils.translation import gettext_lazy as _
from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='customuser_set', 
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='customuser_set',  
        related_query_name='user',
    )
    def __str__(self):
        return self.email