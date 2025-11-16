from posixpath import split
from urllib.parse import urlparse
from django.shortcuts import render,redirect,get_object_or_404
from .models import Registar,Accounts
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login as auth_login ,logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages,auth
from .forms import RegistrationForm,EditProfileForm
from carts.views import _cart_id
from carts.models import Cart,CartItem
from orders.models import Order,Payment


# verifecation email 

from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator


def registar(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email= form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            phone = form.cleaned_data['phone']
            confirm_password = form.cleaned_data['confirm_password']
            
            if password != confirm_password:
                messages.error(request,'passwords is not match')
                return redirect('registar')
            
            user = Accounts.objects.create_user(
                first_name = first_name,
                last_name = last_name,
                email = email,
                username = username,
                password = password
                )
            
            user.phone = phone
            user.save()
            
            domain = get_current_site(request)
            email_subject = 'please activate your email.'
            message = render_to_string('accounts/verifecation_email.html',{
                'user' :user,
                'domain' : domain,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
            }) 
            
            
            to_send = email
            send_email = EmailMessage(email_subject, message ,to=[to_send])
            send_email.send()
            
            messages.success(request,"registration sucessful")
    else:
        form = RegistrationForm()
    context ={
            'form' : form
        }
    return render(request,'accounts/registar.html',context)
    

def login(request):
    if request.method == 'POST':
        
        email = request.POST.get('email')
        password = request.POST.get('password')

        # user = Accounts.objects.get(email = email)
        
        user = auth.authenticate(email=email , password=password)
        
        # if check_password(password,user.password):
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id = _cart_id(request))
                cart_items_ex = CartItem.objects.filter(cart=cart).exists() 
                if cart_items_ex:
                    cart_items = CartItem.objects.filter(cart = cart)
                    for item in cart_items:
                        item.user = user
                        item.save()
            except:
                pass
            auth_login(request , user)
            messages.success(request,'login sucessful')
            url = request.META.get('HTTP_REFERER')  
            try:
                query = request.utils.urlparse(url).query
                phars = dict(x.split('=') for x in query)
                
                if 'next' in phars:
                    nextPage = phars['next']
                    return redirect(nextPage)
            except:
                return redirect('home')
        else:
            messages.error(request,'email or password is not valid')
            return redirect('login')

    return render(request,'accounts/signin.html')

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')

def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Accounts._default_manager.get(pk=uid)
        
    except(ValueError,TypeError,OverflowError,Accounts.DoesNotExist):
        user = None
        
        
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request,"activated sucessful")
        return redirect('login')
        
    else:
        return redirect('registar')
    
@login_required(login_url='login')        
def dashboard(request):

    return render(request,'accounts/dashboard.html')


def forget(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = Accounts.objects.get(email = email)
        
        if user is not None:
            domain = get_current_site(request)
            email_subject = 'reset your passwords'
            message = render_to_string('accounts/reset_password_validate.html',{
                
                'user' :user,
                'domain' : domain,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
            }) 

            to_send = email
            send_email = EmailMessage(email_subject, message ,to=[to_send])
            send_email.send()
            messages.success(request,'sucessful,send your email')
        else :
            messages.error(request,'email is not valid')
            return redirect('forget')
        
    return render(request,'accounts/forget_password.html')

def reset_password_validate(request, uidb64 ,token):
    
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = Accounts._default_manager.get(pk=uid)
            
        except(ValueError,TypeError,OverflowError,Accounts.DoesNotExist):
            user = None
        
            
        if user is not None and default_token_generator.check_token(user,token):
            request.session['uid'] = uid
            messages.success(request,'sucess')
            return redirect('reset')

        else:
            messages.error(request,'user is not found')
            return redirect('registar')


def reset(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        

                
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Accounts.objects.get(pk = uid)
            user.password = make_password(password)
            user.save()
            messages.success(request,"you change password sucessful")
            return redirect('login')
        else:
            messages.error(request,'password are not match')
            return redirect('reset_password')
    return render(request,'accounts/reset_password.html')

@login_required(login_url='login')
def edit_profile(request):
    if request.method == 'POST':
        
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
            
        user = Accounts.objects.get(email = request.user)
        if user:   
            
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.phone = phone
            
            
            user.save()
            return redirect('dashboard')
        
    context = {
        'edit_profile' : edit_profile,

    }
    return render(request,'accounts/edit_profile.html',context)

def change_password(request):
    if request.method == 'POST':
        # return HttpResponse('Password changed')
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        # return HttpResponse("ff")
        user = Accounts.objects.get(email=request.user)
        # return HttpResponse(user)
        if check_password(old_password,user.password):
            if new_password == confirm_password:
                user.password = make_password(new_password)
                user.save()
                return redirect('login')
            else:
                messages.error(request,'new password is not equel confirm password')
                return redirect('change_password')
        else:
            messages.error(request,'old password is not valid')
            return redirect('change_password')


    return render(request,'accounts/change_password.html')

# def registar(request):
#     user = None
#     if request.method == 'POST':
        
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         email = request.POST.get('email')
#         gender = request.POST.get('gender')
#         city = request.POST.get('city')
#         country = request.POST.get('country')
#         password = request.POST.get('password')
#         repeat_password = request.POST.get('repeat_password')
        
#         if password != repeat_password:
#             messages.error(request, "❌ Password does not match")
#             return redirect('registar')
#         else:
#             user = Registar.objects.create(
#                 first_name = first_name,
#                 last_name = last_name,
#                 email = email,
#                 gender = gender,
#                 city = city,
#                 country = country,
#                 password = make_password(password),
#                 repeat_password = make_password(repeat_password),
#             )
#             messages.success(request, "✅ Registration successful!")
#             return redirect('home')
#     return render(request,'accounts/registar.html',{'users' : user})


# def login(request): 
#     context = {}
#     if request.method == 'POST':   
#         email = request.POST.get('email')
#         password =request.POST.get('password')
        
#         try:
#             user = Registar.objects.get(email = email) 
#             if check_password(password , user.password):
#                 return redirect('home')
#             else:
#                 messages.error(request,'❌ Password Or Email is wrong')
#                 return redirect('login')
             
#         except Registar.DoesNotExist:
            
#             messages.error(request,'❌ Password Or Email does not exist')
#             return redirect('login')
        
#     return render(request,'accounts/signin.html',context)

# def forget(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         try:      
#             user = Registar.objects.get(email = email)
            
#             if user!=None:
#                 messages.success(request, "✅ Login successful!")
#                 return redirect('reset')
           
#             else:
#                 messages.error(request," ❌ Email does not exist.")
#                 return redirect('forget')
#         except Registar.DoesNotExist:
#             messages.error(request," ❌ Email does not exist")
#     return render(request,'accounts/forget_password.html')
    
# def reset_password(request):
#     if request.method == 'POST':
#         password = request.POST.get('password')
#         confirm_password = request.POST.get('confirm_password')
#         email = request.POST.get('email')
        
#         if password != confirm_password:
#             messages.error(request,'password does not match')
#             return redirect('reset')
#         else:
#             user =Registar.objects.get(email = email)
#             user.password = make_password(password)
#             user.save() 
#             messages.success(request,'updated  sucessful')
#             return redirect('login')
            
#             # messages.error(request,'password does not match.')
#             # return redirect('reset')

        
#     return render(request,'accounts/reset_password.html')