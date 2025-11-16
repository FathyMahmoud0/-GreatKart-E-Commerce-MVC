from django.shortcuts import render,get_object_or_404
from .models import Product
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Varition
from carts.models import Cart
from django.http import HttpResponse


def store(request):
    
    products = Product.objects.filter(is_available = True)
    products_count = Product.objects.count()
    
    paginator = Paginator(products,3)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    

        

    context = {'products' : page_obj , 
               'products_count' : products_count}
    return render(request,'products/store.html',context)

def home(request,category_slug):
    
    if category_slug != None:
        categories = get_object_or_404(Category,slug=category_slug)
        products = Product.objects.filter(category = categories)
        products_count = Product.objects.count()
          
    else:
        products = Product.objects.all().filter(is_available=True)
        products_count = Product.objects.count()
    
    context = {'products' : products , 
               'products_count' : products_count}
    return render(request,'products/store.html',context)


def product_detail(request,category_slug,product_slug):
    try:
        product = Product.objects.get(category__slug =category_slug,slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id = _cart_id(request)).exists()
        variants = Varition.objects.all()
        
        if request.method == 'GET':
            variant_id = request.GET.get("varition_value")
            print(variant_id)
            print('fathy')
        
        
    except Exception as e:
        raise e
    
    context ={
        'product' : product,
        'in_cart' : in_cart,
        'variants' : variants,
    }
    
    return render(request,'products/product_detail.html',context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.filter(Q(discription__icontains=keyword) | Q(name__icontains = keyword))
            product_count = products.count()
            
    elif request.method == 'GET':
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        size = request.GET.get("size")
        
        if min_price:
            products = Product.objects.filter(price__gte = min_price)
        if max_price:
            products = Product.objects.filter(price__lte = max_price)
        if size:
            products = Varition.objects.filter(varition_value=size)
            
        product_count = products.count()
    context = {
        'products' : products,
        'product_count' : product_count,
    }
    return render(request,'products/store.html',context)




