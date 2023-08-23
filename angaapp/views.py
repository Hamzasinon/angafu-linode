from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import*
from django.http import HttpResponse
from rest_framework import generics
from .serializers import *
from twilio.rest import Client
from django.db.models import Q

def is_venter(user):
    return user.role == 'venter'

def is_achat(user):
    return user.role == 'achat'


#@user_passes_test(is_venter, is_achat)
def home(request):
    return render(request, 'index.html',)
#@user_passes_test(is_venter)
def home2(request, ):
    destination=Destination.objects.all()
    return render(request, 'index2.html', {'destination':destination})
def dest(request, destination_id):
    destination=get_object_or_404(Destination, id=destination_id)
    societe=destination.societe_set.all()
    context={
        'destination':destination,
        'societe':societe
    }
    return render(request, 'dest.html', context)

def reserve(request, societe_id):
    
    societe =get_object_or_404(Societe, id=societe_id)
    
    time=Heure_d.objects.all()
    destination=Destination.objects.all()
    context={
        
        'societe':societe,
        'time':time,
        'destination':destination,
    }
    return render(request, 'reservation.html', context)

def addreserve(request, societe_id):
    societe = Societe.objects.get(id=societe_id)
    time=Heure_d.objects.all()
    destination=Destination.objects.all()
    if request.method=="POST":
        societe_nom = [x.nom for x in Societe.objects.all()]
        societe_ids=[Societe.objects.get(id=societe_id)]
        
        nom = request.POST.get('nom') 
        prenom = request.POST.get('prenom')
        date=request.POST.get('date')
        time_pk=request.POST.get('time')
        time=Heure_d.objects.get(pk=time_pk)
        tel = request.POST.get('tel')
        num_trans=request.POST.get('num_trans')
        destination_pk=request.POST.get('destination')
        destination=Destination.objects.get(pk=destination_pk)
        
        reservation = Reservations.objects.create(nom=nom, prenom=prenom,date=date,
                                                        time=time, tel=tel, num_trans=num_trans ,destination=destination)
        
        reservation.societe.add(Societe.objects.get(id=societe_id))
        reservation.save()
        request.session['reservation_id'] = reservation.id
        return redirect('home2')
    return render(request, 'reservation.html',{'societe':societe})

class SocieteListView(generics.ListAPIView):
    queryset = Societe.objects.all()
    serializer_class = SocieteSerializer
    
class ReservationsListView(generics.ListAPIView):
    queryset = Reservations.objects.all()
    serializer_class = ReservationsSerializer

class HeurListView(generics.ListAPIView):
    queryset = Heure_d.objects.all()
    serializer_class = HeurSerializer
    
class DetinationListView(generics.ListAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    
def affreserve(request):
    query = request.GET.get('query') 
    if query:
        lis_reserver = Reservations.objects.filter(Q(nom__icontains=query) | Q(prenom__icontains=query) | Q(num_trans__icontains=query))
    else:
        lis_reserver = Reservations.objects.filter(val=False)
    return render(request, 'affreserve.html', {'lis_reserver': lis_reserver, 'query': query})
def affconfirme(request, reservation_id):
    reservation = get_object_or_404(Reservations, id=reservation_id)
    return render(request,'confirme.html',{'reservation': reservation})
#def confirme(request, reservation_id):
#    if request.method == 'POST':
 #       num_trans = request.POST.get('num_trans') 
 #       trans_id = request.POST.get('trans_id')
 #       montant_paye = request.POST.get('montant_paye')
 #       reservation = Reservations.objects.get(id=reservation_id)
 #       if num_trans == reservation.num_trans or (trans_id and montant_paye == '10000'):
 #           confirme_instance = Confirme.objects.create(num_trans=num_trans,trans_id=trans_id,montant_paye=montant_paye)
 #           reservation.confirm = True
 #           reservation.save()
 #           reservation.confirme_set.add(confirme_instance)
 #       return redirect('affreserve')
 
def confirme(request, reservation_id):
    if request.method == 'POST':
        num_trans = request.POST.get('num_trans') 
        trans_id = request.POST.get('trans_id')
        montant_paye = request.POST.get('montant_paye')
        reservation = Reservations.objects.get(id=reservation_id)
        
        # Vérifier si les conditions de num_trans et montant_paye sont remplies
        if num_trans == reservation.num_trans and montant_paye in ['10000', '15000', '20000']:
            confirme_instance = Confirme.objects.create(num_trans=num_trans, trans_id=trans_id, montant_paye=montant_paye)
            reservation.confirm = True
            reservation.save()
            reservation.confirme_set.add(confirme_instance)
        
        return redirect('affreserve')


def affdest(request):
    destination=Destination.objects.all()
    context={
        'destination':destination,
    }
    return render(request, 'affdest.html',context)

def aff_a_valid(request, destination_id):
    destination=get_object_or_404(Destination, id=destination_id)
    societe=destination.societe_set.all()
    context={
        'destination':destination,
        'societe':societe
    }
    return render(request, 'affavalid.html',context)
def affvalid(request,reservation_id):
    reservation=get_object_or_404(Reservations, id=reservation_id)
    confirme_lis = reservation.confirme_set.all()
    
    return render(request, 'confirmv.html',{'confirme_lis':confirme_lis,'reservation':reservation})

#def valide(request, reservation_id):
 #   if request.method == 'POST':
 #       numticket = request.POST.get('numticket')
 #       numchaise = request.POST.get('numchaise')

  #      reservation = get_object_or_404(Reservations, id=reservation_id)

   #     try:
    #        confirme_instance = reservation.confirm.get()
     #   except Confirme.DoesNotExist:
      #      print("Aucune instance Confirme associée à cette réservation.")
       #     Valide.objects.create(confirmation=confirme_instance, numticket=numticket, numchaise=numchaise)

        # Envoi du SMS
        #account_sid = 'ACf039fa8809fc1dbe5f6a20ad139f8c20'
        #auth_token = 'a015f30efef3355999c3de439c9e9a68'
        #client = Client(account_sid, auth_token)

        #message = client.messages.create(
          #  body=f"Votre réservation a été validée avec succès. Votre numéro de ticket est {numticket} et votre numéro de chaise est {numchaise}.",
         #   from_='+14782493931',
           # to=confirme_instance.num_trans  # Utilisez confirme_instance au lieu de confirme
        #)

        #print(message.sid)  # Cela imprime l'ID du message Twilio (pour vérification)

    #return redirect('aff_a_valid')
def affichv(request, confirme_id):
    confirme=get_object_or_404(Confirme, id=confirme_id)
    
    return render(request, 'valide.html',{'confirme':confirme})



#def valide(request, confirme_id):
#    confirme = Confirme.objects.get(id=confirme_id)
    
#    if request.method == 'POST':
#        numticket = request.POST.get('numticket')
#        numchaise = request.POST.get('numchaise')
        
        
#        account_sid = 'ACf039fa8809fc1dbe5f6a20ad139f8c20'
#        auth_token = 'a015f30efef3355999c3de439c9e9a68'
#        twilio_phone_number = '+14782493931'
        
#        client = Client(account_sid, auth_token)
        
#        message = f'Votre ticket est validé avec succès pour la destination {", ".join(str(res.destination) for res in confirme.reservation.all())} à la gare de {", ".join(str(res.societe.first().nom) for res in confirme.reservation.all())}. Numéro du ticket : {numticket}, chaise : {numchaise}.'
        
        
#        message = client.messages.create(
#            to=confirme.num_trans,
#            from_=twilio_phone_number,
#            body=message
#        )
        
#        valid = Valide.objects.create(numticket=numticket, numchaise=numchaise)
#        valid.confirmation.add(confirme)
#        valid.save()
        
      
#        for reservation in confirme.reservation.all():
 #           reservation.val = True
 #           reservation.save()
        
  #      return redirect('home')
    
#    return render(request, 'valide.html', {'confirme': confirme})


import requests

#def valide(request, confirme_id):
 #   confirme = Confirme.objects.get(id=confirme_id)
    
  #  if request.method == 'POST':
  #      numticket = request.POST.get('numticket')
  #      numchaise = request.POST.get('numchaise')
        
        # Paramètres nécessaires pour l'API 3mi
   #     url = 'https://www.lesmsbus.com:7170/ines.smsbus/smsbusMt'
   #     params = {
   #         'to': confirme.num_trans,  # Numéro du destinataire
   #         'text': f'Votre ticket est validé avec succès pour la destination {", ".join(str(res.destination) for res in confirme.reservation.all())} à la gare de {", ".join(str(res.societe.first().nom) for res in confirme.reservation.all())} à {", ".join(str(res.time.time) for res in confirme.reservation.all())}. Numéro du ticket : {numticket}, chaise : {numchaise}.',
   #         'username': 'seydou',
   #         'password': 'Fer60153982',
   #         'from': '226',
   #         'dlr': '1',  # Demande d'accusé de réception
   #     }
        
   #     response = requests.get(url, params=params)
        
   #     if response.status_code == 200:
   #         # Mettez à jour le champ 'val' de la réservation associée
   #         reservation = confirme.reservation
   #         reservation.val = True
   #         reservation.save()
            
   #         return redirect('home')
   #     else:
            # Gérer le cas d'échec de l'envoi du SMS
            # (par exemple, en affichant un message d'erreur)
    #        pass
        
    #return render(request, 'valide.html', {'confirme': confirme})
def valide(request, confirme_id):
    confirme = get_object_or_404(Confirme, id=confirme_id)

    if request.method == 'POST':
        numticket = request.POST.get('numticket')
        numchaise = request.POST.get('numchaise')
        url = 'https://www.lesmsbus.com:7170/ines.smsbus/smsbusMt'
        params = {
            'to': confirme.num_trans, 
            'text': f'Votre ticket est validé avec succès pour la destination {", ".join(str(res.destination) for res in confirme.reservation.all())} à la gare de {", ".join(str(res.societe.first().nom) for res in confirme.reservation.all())} à {", ".join(str(res.time.time) for res in confirme.reservation.all())}. Numéro du ticket : {numticket}, chaise : {numchaise}.',
            'username': 'seydou',
            'password': 'Fer60153982',
            'from': '226',
            'dlr': '1',
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:

            valid = Valide.objects.create(numticket=numticket, numchaise=numchaise)
            valid.confirmation.add(confirme)
            valid.save()

            
            reservation = confirme.reservation.first()
            reservation.val = True
            reservation.save()

        

        return redirect('home')

    return render(request, 'valide.html', {'confirme': confirme})

def rejeter(request, reservation_id):
    reservation = get_object_or_404(Reservations, id=reservation_id)
    reservation.confirm = False
    reservation.save()
    return redirect('affavalid')
def affdes(request, societe_id):
    societe = get_object_or_404(Societe, id=societe_id)
    reservations_confirmees_non_valides = societe.reservations_set.filter(confirm=True, val=False)
    return render(request, 'hu.html', {'reservations_confirmees_non_valides': reservations_confirmees_non_valides, 'societe': societe})

def destination(request, destination_id):
    try:
        societe_id = int(request.GET.get('societe_id'))  # Récupérez l'ID de la société depuis le paramètre de requête
        
        # Obtenez toutes les réservations associées à la destination spécifiée et à la société spécifiée
        reservations = Reservations.objects.filter(destination_id=destination_id, societe__id=societe_id, confirm=True)
        
        context = {
            'reservations': reservations,
        }
        
        return render(request, 'hu.html', context)
        
    except Reservations.DoesNotExist:
        return render(request, 'hu.html', {'reservations': []})
    
def success(request):
    valides = Reservations.objects.filter(val=True)
    return render(request, 'success.html',{'valides': valides})


#def register_user(request):
 #   if request.method == 'POST':
 #       form = UserCreationForm(request.POST)
 #       if form.is_valid():
   #         user = form.save()
  #          return redirect('home')  # Redirigez vers la page d'accueil ou une autre page
   # else:
   #     form = UserCreationForm()
    
    #return render(request, 'register_user.html', {'form': form})

#def register_superuser(request):
 #   if request.method == 'POST':
  #      form = UserCreationForm(request.POST)
   #     if form.is_valid():
    #        user = form.save(commit=False)
     #       user.is_staff = True
      #      user.save()
       #     return redirect('home')  # Redirigez vers la page d'accueil ou une autre page
    #else:
     #   form = UserCreationForm()
    
#    return render(request, 'register_superuser.html', {'form': form})
