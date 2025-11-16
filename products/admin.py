from django.contrib import admin
from .models import Product
# Register your models here.
from.models import Varition


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}
    list_display = ('name' , 'price' , 'category', 'stock' ,'created_at' , 'is_available' , 'modifaied_at')


admin.site.register(Product,ProductAdmin)

admin.site.register(Varition)
