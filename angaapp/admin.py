from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
#from .models import CustomUser
from .models import*

admin.site.register(Societe)
admin.site.register(Heure_d)
admin.site.register(Destination)
admin.site.register(Reservations)
#admin.site.register(CustomUser, UserAdmin)