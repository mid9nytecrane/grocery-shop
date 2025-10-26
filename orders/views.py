from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
from django.http import JsonResponse
from .models import Order, OrderItem
from .forms import CheckoutForm
from cart.cart import Cart 
from payment.paystack import Paystack

from core.models import Product
from orders.models import Order 
from payment.models import Payment 


import uuid
from django.urls import reverse
from .paystack import checkout
from django.contrib import messages



def Checkout_view(request):
    cart = Cart(request)

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user 

            #set initial order status 
            order.status = "pending"
            order.order_number = f"ORD-{uuid.uuid4().hex[:12].upper()}"
            order.save()

            #create order items 
            # print()
            # print(type(cart.get_prods()))
            # print(callable(cart.get_prods))

            for product in cart.get_prods():
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=cart.get_quants()[str(product.id)],
                    price = product.price,
                )
            
            print(f"\n cart total: {cart.cart_total()}")
           
            payment = Payment.objects.create(
                amount=cart.cart_total(),
                email=request.user.email,
                user=request.user,
                reference=order.order_number,
                
            )

            payment.save()
            paystack_pub_key = settings.PAYSTACK_PUBLIC_SECRET_KEY   

            context = {
                'form':form,
                'cart':cart,
                'payment':payment,
                'amount_value':payment.amount_value(),
                'paystack_pub_key': paystack_pub_key,
                
            }

            return render(request, 'checkout/makepayment.html',context)
        else:
            form_errors = form.errors.as_text()
            messages.warning(request, f'Error: Invalid Data. Details: {form_errors}')
            return redirect('orders:checkout')
        
    else:
        form = CheckoutForm()
        context = {'form':form}
        return render(request, 'checkout/checkout.html',context)


def make_payment(request):
    

    return render(request, "checkout/makepayment.html")


# def order_success(request, order_id):

#     order = get_object_or_404(Order, pk=order_id)

#     context = {'order':order}

#     return render(request,"checkout/order-success.html",context)


# @login_required
# def create_paystack_checkout_session(request, order_id):

#     """ create a paystack session for existing order"""
#     try:
#         cart = Cart(request)
#         order = get_object_or_404(Order, pk=order_id)

#         # verify if user is currently logged in 
#         if request.user.is_authenticated and order.user != request.user:
#             messages.error(request, "you don't have permission to access this !!!.".title())
#             return redirect('orders:checkout')
        
#         amount = cart.product_subtotal()

#          # /payment-success/2/
#         payment_success_url = reverse('orders:order-success', kwargs={"order_id":order.id})

#         # http://domain.com/payment-success/2/ 
#         callback_url = f"{request.scheme}://{request.get_host()}{payment_success_url}"

#         checkout_data = {
#             "email": request.user.email,
#             "amount": (amount) * 100,  # i
#             "currency": "GHS",
#             "channels": ["card", "bank_transfer", "bank", "ussd", "qr", "mobile_money"],
#             "reference": order.order_id, # 
#             "callback_url": callback_url,
#             "metadata": {
#                 "order_id": order.id,
#                 "user_id": request.user.id if request.user.is_authenticated else None,
#                 "order_number": order.order_id,
#             },
#             "label": f"Order #{order.order_id}"
#         }
#         status, check_out_session_url_or_error_message = checkout(checkout_data)

#         if status:
#             #updating order with payment reference
#             order.paystack_reference = checkout_data['reference']
#             order.save()
#             return redirect(check_out_session_url_or_error_message)
#         else:
#             messages.error(request, check_out_session_url_or_error_message)
#             return redirect('orders:checkout')
        
#     except Exception as e:
#         messages.error(request,f"An error occured: {str(e)}")
#         print(f"An error occured: {str(e)}")
#         return redirect("orders:checkout")
    
    
    


    #my codes 
    # cart = Cart(request)
    # #order = get_object_or_404(Order,pk=order.id)
    # products = cart.get_prods()
    # amount = cart.product_subtotal()
    # #product = get_object_or_404(Product, id=product_id)
    # purchase_id = f"purchase_{uuid.uuid4()}"

    #  # /payment-success/2/
    # payment_success_url = reverse('order-success')

    # # http://domain.com/payment-success/2/ 
    # callback_url = f"{request.scheme}://{request.get_host()}{payment_success_url}"

    # checkout_data = {
    #     "email": request.user.email,
    #     "amount": (amount) * 100,  # i
    #     "currency": "GHS",
    #     "channels": ["card", "bank_transfer", "bank", "ussd", "qr", "mobile_money"],
    #     "reference": purchase_id, # generated by developer
    #     "callback_url": callback_url,
    #     "metadata": {
    #         "product_id": "98794",
    #         "user_id": request.user.id,
    #     },
    #     "label": f"Checkout For testing cart "
    # }

    
    # status, check_out_session_url_or_error_message = checkout(checkout_data)

    # if status:
    #     return redirect(check_out_session_url_or_error_message)
    # else:
    #     messages.error(request, check_out_session_url_or_error_message)
    #     return redirect('pricing')

    

# def order_success(request, order_id):
#     """Handle successful payment callback"""
#     try:
#         order = get_object_or_404(Order, pk=order_id)
        
#         # Verify payment with Paystack
#         from .paystack import verify_payment  # You'll need to implement this
        
#         if order.paystack_reference:
#             # Verify the payment
#             verification_status, verification_data = verify_payment(order.paystack_reference)
            
#             if verification_status and verification_data.get('status') == 'success':
#                 # Payment verified successfully
#                 order.payment_status = 'completed'
#                 order.save()
                
#                 # Clear the cart
#                 cart = Cart(request)
#                 cart.clear()
                
#                 messages.success(request, "Payment completed successfully!")
#             else:
#                 # Payment verification failed
#                 order.payment_status = 'failed'
#                 order.save()
#                 messages.warning(request, "Payment verification pending.")
#         else:
#             messages.warning(request, "No payment reference found.")
        
#         return render(request, 'checkout/order-success.html', {'order': order})
        
#     except Exception as e:
#         messages.error(request, f"Error processing order: {str(e)}")
#         return redirect('orders:checkout')
    


# @login_required
# def payment_webhook(request):
#     """handle payment webhook for payment verification"""
#     if request.method == 'POST':
#         import json
#         from django.views.decorators.csrf import csrf_exempt
#         from django.http import HttpResponse

#         try:
#             payload = json.loads(request.body)
#             data = payload.get('data')
#             event = payload.get('event')
#             status = payload.get("status_code")

#             if event == "charge.success":
#                 reference = data.get("reference")

#                 # find order by reference
#                 try:
#                     order = Order.objects.get(order_number=reference)
#                     order.status = "completed"
#                     order.is_paid = True
#                     order.save()

#                     cart = Cart(request)
#                     cart.clear()

#                 except Order.DoesNotExist:
#                     pass 
#             return HttpResponse(status==200)
#         except Exception as e:
#             return HttpResponse(status == 400)


