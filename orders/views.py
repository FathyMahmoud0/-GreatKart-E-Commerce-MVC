from django.shortcuts import get_object_or_404, render,redirect
from carts.models import Cart,CartItem
from carts.views import _cart_id
from .models import Order,OrderItem,Payment
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
import json

def order_payment(request):
    return render(request, 'orders/payment.html')
@login_required(login_url = 'login')
def create_order(request, total = 0,quantity = 0 , cart_items = None):
    current_user = request.user
    tax=0
    grand_total=0
    
    count  = CartItem.objects.count()
    
    if count<=0:
        return redirect('home')
    
    cart = Cart.objects.get(cart_id =_cart_id(request))
    cart_items = CartItem.objects.filter(cart = cart,is_active= True)
    for cart_item in cart_items:
        total+= (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity       
    if total > 0:
        tax = (2 *total)/100
        grand_total = (total + tax)
           
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        # return HttpResponse(first_name)
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        street = request.POST.get('street')
        
        order = Order.objects.create(
            user = current_user,
            first_name = first_name,
            last_name = last_name,
            phone = phone,
            email = email,
            country = country,
            state = state,
            city = city,
            street = street,
            total = total,
            grand_total = grand_total,
            tax = tax,
            status = 'new',
        )
        order.save()
        
    # for cart_item in cart_items:   
    #     order = Order.objects.get(user = request.user)
    #     order_item = OrderItem.objects.create(
                
    #             product = cart_item.product,
    #             quantity = cart_item.quantity,
                
    #         ) 
    #     order_item.save()
            
        return redirect('order_payment')
        
        
    context = {
        'cart_items'  : cart_items,
        'total' :total,
        'quantity' : quantity,
        'tax' : tax,
        'grand_total' : grand_total,
        'count' : count,
    }
            
    return render(request,'orders/place_order.html',context)


def order_detail(request):
    orders = Order.objects.filter(user = request.user).order_by('-created_at')
    context = {
        'orders' : orders,
    }
    return render(request,'orders/orders_details.html',context)

def order_complete(request, total = 0,quantity = 0 , cart_items = None):
    total = 0
    tax=0
    grand_total = 0
    
    cart = Cart.objects.get(cart_id = _cart_id(request))
    cartitems = CartItem.objects.filter(cart = cart)
    order = Order.objects.get(user = request.user)
    
    
    for cart_item in cartitems:
        total+= (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
        
    if total > 0:
        tax = (2 * total)/100
        grand_total = (total + tax)
    
    context = {
       'order' :order,
       'cartitems' : cartitems,
       'total' : total,
       'grand_total' : grand_total,
       'tax' : tax,
    }
    return render (request,'orders/order_completed.html',context)