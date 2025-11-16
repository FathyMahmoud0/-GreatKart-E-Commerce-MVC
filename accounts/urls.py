from django.urls import path
from . import views

urlpatterns = [
    path('registar/',views.registar,name='registar'),
    path('login/',views.login,name = 'login'),
    path('forget/',views.forget,name = 'forget'),
    path('logout/',views.logout_view,name='logout'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('change_password/',views.change_password,name='change_password'),
    path('reset/',views.reset,name='reset'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('activate/<uidb64>/<token>/',views.activate,name='activate'),
    path('reset_password/<uidb64>/<token>/',views.reset_password_validate,name='reset_password_validate'),

]
