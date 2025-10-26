from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse
from django.contrib import messages

from core.models import Product
from .cart import Cart 
from .models import CartItem

# Create your views here.

def cart_summary(request):
    cart = Cart(request)

    cart_products = cart.get_prods
    
    quantities = cart.get_quants
    cart_total = cart.cart_total()

    items = cart.__len__()
    
   
    product_subtotals = cart.product_subtotal()
  

    return render(request,'cart/cart.html',{
        'cart_products': cart_products, 
        'quantities':quantities,
        'cart_total':cart_total,
        'product_subtotals': product_subtotals,
        #'subtotal':subtotal,
 
    })

def cart_add(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        #lookup in DB
        product = get_object_or_404(Product, id=product_id)

        
        
        #save product in session
        cart.add(product=product,quantity=product_qty)
        
        
        
       
        #Get cart quantity
        cart_quantity = cart.__len__()


        #Return response
        response = JsonResponse({"qty": cart_quantity,
                                 
                                 })
        messages.success(request, f"{product} is added to cart".title())
        return response

def cart_update(request):
    cart = Cart(request)

    

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        product = get_object_or_404(Product, id=product_id)

        cart.update(product=product_id, quantity=product_qty)
        
        item_total = product.price * product_qty

        response = JsonResponse({'qyt': product_qty,
                                 'item_total': format(item_total,".2f")
                                 })
        
        messages.success(request, f"{product} quantity has been updated".title())

        return response


def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))

        product = get_object_or_404(Product, id=product_id)

        cart.delete(product=product_id)

        response = JsonResponse({'product':product_id})
        messages.success(request, f"{product} has been deleted from cart".title())
        return response
    

def clear_cart(request):
    cart = Cart(request)
    cart.clear_cart()

    messages.succes("your cart is cleared...")
    return redirect('home')

def checkout(request):
    return render(request, 'cart/checkout.html', {})