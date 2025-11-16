from django.shortcuts import render,redirect,get_object_or_404
from products.models import Product
from .models import CartItem,Cart
from django.contrib.auth.decorators import login_required

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_to_cart(request,product_id):
    product = Product.objects.get(id = product_id)
    
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
        
    cart.save()
    
    try:
        cart_item = CartItem.objects.get(product = product,cart = cart)
        cart_item.quantity +=1
        cart_item.save()
        
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            user = request.user,
            product = product,
            cart = cart,

        )
        cart_item.save()
    
    return redirect('cart')


def cart(request,total = 0,quantity = 0 , cart_items = None):
    tax=0
    grand_total=0
    cart = Cart.objects.get(cart_id =_cart_id(request))
    count  = CartItem.objects.count()
    cart_items = CartItem.objects.filter(cart = cart,is_active= True)
    for cart_item in cart_items:
        total+= (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
        
        
    if total > 0:
        tax = (2 *total)/100
        grand_total = (total + tax)
    
    context = {
        'cart_items'  : cart_items,
        'total' :total,
        'quantity' : quantity,
        'tax' : tax,
        'grand_total' : grand_total,
        'count' : count,
    }
    return render (request,'products/cart.html',context)


def remove_cart(request,product_id):

    cart = Cart.objects.get(cart_id = _cart_id(request))
    product  = get_object_or_404(Product,id =product_id)
    
    cart_item = CartItem.objects.get(cart = cart , product = product)
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


def remove_item(request,product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product  = get_object_or_404(Product,id =product_id)
    
    cart_item = CartItem.objects.get(cart = cart , product = product)
    cart_item.delete()
    
    return redirect('cart')

@login_required(login_url='login')
def checkout(request,total = 0,quantity = 0 , cart_items = None):
    tax=0
    grand_total=0
    cart = Cart.objects.get(cart_id =_cart_id(request))
    
    count  = CartItem.objects.count()
    cart_items = CartItem.objects.filter(cart = cart,is_active= True)
    for cart_item in cart_items:
        total+= (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
        
        
    if total > 0:
        tax = (2 *total)/100
        grand_total = (total + tax)
    
    context = {
        'cart_items'  : cart_items,
        'total' :total,
        'quantity' : quantity,
        'tax' : tax,
        'grand_total' : grand_total,
        'count' : count,
    }
    return render (request,'products/checkout.html',context)
