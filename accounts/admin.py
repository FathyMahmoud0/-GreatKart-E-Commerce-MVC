from django.contrib import admin
from .models import Accounts,Registar
# Register your models here.

from django.contrib.auth.admin import UserAdmin

# class AccountsAdmin(UserAdmin):

#     list_display = ('email','username','password','first_name','last_name','is_admin','is_active','is_superadmin')
#     list_display_links = ('email','username')
#     list_filter = ('first_name','is_staff')
#     search_fields = ('username', 'first_name', 'last_name', 'email')
    
#     filter_horizontal = ()
    
#     ordering = [('is_joined')]

admin.site.register(Accounts)

class RegistarAdmin(admin.ModelAdmin):
    list_display = ('first_name' , 'last_name' , 'email','gender', 'city','created_at')
    list_display_links = ('email',)
    filter_horizontal = ()
    ordering = [('created_at')]

admin.site.register(Registar,RegistarAdmin)