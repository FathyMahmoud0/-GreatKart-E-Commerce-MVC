from django.db import models
from products.models import Product
from accounts.models import Accounts
# Create your models here.


class Cart (models.Model):
    cart_id = models.CharField(max_length=30)
    date_added = models.DateField(auto_now_add=True)
    
class CartItem(models.Model):
    
    user = models.ForeignKey(Accounts,on_delete=models.CASCADE , null =True , blank=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    
    def total_price(self):
        return  self.product.price * self.quantity 
    
    