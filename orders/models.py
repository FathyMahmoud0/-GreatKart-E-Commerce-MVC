from django.db import models
from accounts.models import Accounts
from django.utils import timezone
from products.models import Product,Varition
import datetime
import uuid
# Create your models here.

class Payment(models.Model):
    payment_method = models.CharField(max_length=30)
    user = models.ForeignKey(Accounts,on_delete=models.SET_NULL , null=True,blank=True)
    payment_id = models.CharField(max_length=60)
    created_at = models.DateTimeField(default=timezone.now)
    payment_amount = models.CharField(max_length=60)
    status = models.CharField(max_length=30)
    
    
    def __str__(self):
        return self.payment_id
status = {
    'new' : 'new',
    'completed' : 'completed',
    'accpected' :'accpected',
    'canceled' : 'canceled',
}
    
class Order(models.Model):
    
    payment = models.ForeignKey(Payment,models.CASCADE , null=True , blank=True)
    user = models.ForeignKey(Accounts,models.CASCADE)
    order_number= models.CharField(max_length=30,auto_created=True)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    phone = models.CharField(max_length=60)
    email = models.EmailField(max_length=60)
    country = models.CharField(max_length=30)
    state = models.CharField(max_length=60)
    street = models.CharField(max_length=60)
    city = models.CharField(max_length=90)
    status = models.CharField(max_length=30,choices=status)
    created_at = models.DateTimeField(default=timezone.now)
    is_orderd = models.BooleanField(default=False)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    

    def save(self, *args, **kwargs):
        if not self.order_number:
            today = datetime.date.today().strftime("%Y%m%d")
            unique_id = uuid.uuid4().hex[:5].upper()  # random part
            self.order_number = f"{today}{unique_id}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number

class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    varitions = models.ForeignKey(Varition,on_delete=models.CASCADE )
    order = models.ForeignKey(Order,on_delete=models.CASCADE )
    quantity = models.IntegerField(max_length=30)
    created_at = models.TimeField(default=timezone.now)
    updated_at = models.TimeField(default=timezone.now)
    
    
    
    

