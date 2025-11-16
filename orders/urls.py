from django.urls import path
from . import views

urlpatterns = [
    path('create_order/',views.create_order,name='create_order'),
    path('order_complete/',views.order_complete,name='order_complete'),
    path('order_payment/',views.order_payment,name='order_payment'),
    path('orders_detail/',views.order_detail,name='orders_details'),

]
