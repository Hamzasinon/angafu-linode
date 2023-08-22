#from django.contrib.auth.models import AbstractUser, BaseUserManager
#from django.contrib.auth.models import Group,Permission
#from django.utils.translation import gettext_lazy as _
#from django.core import validators
from django.db import models
import datetime
from twilio.rest import Client
class Destination(models.Model):
    nom=models.CharField(max_length=40)
    date_created= models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = ("Destination")
        verbose_name_plural = ("Destinations")
    def __str__(self):
        return self.nom
class Societe(models.Model):
    destination=models.ForeignKey(Destination, on_delete=models.CASCADE)
    nom=models.CharField(max_length=80, blank=True)
    img=models.ImageField()
    create_date=models.DateField(auto_now_add=True)
    class Meta:
        verbose_name_plural=('Societe')
    def __str__(self):
        return self.nom
class Heure_d(models.Model):
    time=models.TimeField()
class Reservations(models.Model):
    code_reservation = models.CharField(max_length=100, unique=True, editable=False)
    societe=models.ManyToManyField(Societe,)
    nom=models.CharField(max_length=80, blank=True)
    prenom=models.CharField(max_length=80, blank=True)
    date=models.DateField()
    time=models.ForeignKey(Heure_d, on_delete=models.CASCADE)
    destination=models.ForeignKey(Destination, on_delete=models.CASCADE)
    tel=models.CharField(max_length=80, blank=True)
    num_trans=models.CharField(max_length=80, blank=True)
    confirm = models.BooleanField(default=False)
    val = models.BooleanField(default=False)
    create_date= models.DateField(auto_now_add=True)
    
    class Meta:
            
            verbose_name =('Reservation')
            verbose_name_plural=('Reservations')
            db_table='reservations'
            ordering = ['-create_date']
    def generate_code(self):
        date_part = datetime.datetime.now().strftime("%d%m%Y")
        last_reservation = Reservations.objects.order_by('-id').first()
        if last_reservation:
            last_code_reservation = int(last_reservation.code_reservation[-1])
            new_code_reservation = last_code_reservation + 1
        else:
            new_code_reservation = 1
        code_reservation = f"{self.prenom[:1]}{self.nom[:1]}{date_part}{str(new_code_reservation).zfill(4)}"
        return code_reservation
    def save(self, *args, **kwargs):
        if not self.code_reservation:
            self.code_reservation = self.generate_code()
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.nom} {self.prenom}"
class Confirme(models.Model):
    reservation = models.ManyToManyField(Reservations,)
    num_trans=models.CharField(max_length=80,)
    trans_id= models.CharField(max_length=150,)
    montant_paye = models.DecimalField(max_digits=10, decimal_places=2)
    date_paiement = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.num_trans
class Valide(models.Model):
    confirmation = models.ManyToManyField(Confirme,)
    numticket = models.CharField(max_length=80,)
    numchaise = models.CharField(max_length=80, null=True, blank=True)
    def __str__(self):
        return self.numticket