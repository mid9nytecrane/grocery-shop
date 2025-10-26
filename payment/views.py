from django.shortcuts import render,get_object_or_404,redirect, HttpResponse
from cart.cart import Cart 
from payment.paystack import Paystack
from .models import Payment 
from orders.models import Order 
from django.http import JsonResponse
from django.contrib import messages

from cart.models import CartItem

# Create your views here.


def verify_payment(request, reference):
    try:
        cart = Cart(request)
        payment = Payment.objects.get(reference=reference)
        verified = payment.verify_payment()

        if verified:
            last_order = Order.objects.latest('created_at')
            
            if last_order:
                order = get_object_or_404(Order, pk=last_order.id)
                order.is_paid = True 
                if order.is_paid:
                    order.status = "On Delivery"
                order.save()

                total_cost = cart.cart_total()
                order_info = {
                    'id': order.id,
                    'total_cost':total_cost,
                }

                context = {
                    'order_info': order_info,
                    'payment': payment,
                    'order':order,
                }

                
                cart.clear_cart()
                return render(request, 'checkout/order-success.html', context)
                #return HttpResponse("successfull payment!!..")
            else:
                messages.success(request, "Ooops order id not found")
                return JsonResponse({"error": "order id not found!!!"})
        else:
            messages.success(request, "Ooops, your order is not processed.")
            return redirect('/')

    except Payment.DoesNotExist:
        messages.success(request, 'payment not found for this reference')
        return JsonResponse({"Error_message": "Payment not found."})
    