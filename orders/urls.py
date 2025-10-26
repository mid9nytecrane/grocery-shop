from django.urls import path 

from . import views 
from payment.views import verify_payment

app_name = 'orders'

urlpatterns = [
    path('',views.Checkout_view, name='checkout'),
    path('make_payment/', views.make_payment, name='make-payment'),
    path('verify_payment/<str:reference>/', verify_payment, name='verify-payment'),
    #path('orders_success/<int:order_id>/', views.order_success, name='order-success'),
]
