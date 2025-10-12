from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from .models import Order, OrderItem
from .forms import CheckoutForm
from cart.cart import Cart 



def Checkout_view(request):
    cart = Cart(request)
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user 
            order.save()

            #create order items 
            for product in cart.get_prods:
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=cart.get_quants[str(product.id)],
                    price = product.price,
                )
            
            return render(request, 'checkout/checkout.html', {
                'form':form,
                'cart':cart
            })
    else:
        form = CheckoutForm()
    return render(request, 'checkout/checkout.html', {
        'form':form,
        'cart':cart
    })


