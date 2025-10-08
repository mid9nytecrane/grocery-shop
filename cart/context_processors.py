from .cart import Cart 

#create context processor so it can work on all pages
def cart(request):
    #return default data from cart class
    return {'cart':Cart(request)}