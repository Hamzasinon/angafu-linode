from django.urls import path
from compte.views import*

urlpatterns = [
    path('connecte/',connecte, name='connecte'),
    path('deconnecte/',deconnecte, name='deconnecte'),
    path('register_user/',register_user, name='register_user'),
    path('admin/', admin_view, name='admin-view'),
    path('manager/', manager_view, name='manager-view'),
    path('access-denied/', access_denied, name='access-denied'),
]