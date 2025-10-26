from django.shortcuts import render,redirect,get_object_or_404, HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.db.models import Q

from .forms import SignUpForm,UpdateProfileForm

from core.models import Product,Category
from orders.models import Order,OrderItem




def home(request):
    products = Product.objects.filter(is_sold=False)[:12]
    categories = Category.objects.all()
    
    
    context={
        'products': products,
        'categories': categories,
    }

    return render(request, 'core/home.html', context)

# category page > list products
def list_of_category_products(request, slug):
    q = request.GET.get('q', None)
    category = get_object_or_404(Category, slug=slug)
    category_products = Product.objects.filter(category=category, is_sold=False)
    if q is None or q == '':
        category_products = Product.objects.filter(category=category, is_sold=False)
    else:
        category_products = Product.objects.filter(
            Q(category=category) & Q(name__contains=q),
            is_sold=False
        )
        
    

    
    return render(request, 'core/category_list.html', {
        'category': category,
        'category_products':category_products,
    })


def detail(request,pk):
    product = get_object_or_404(Product,id=pk)
    related_products = Product.objects.filter(category=product.category, is_sold=False).exclude(pk=pk)[0:4]
    context = {
        'product':product,
        'related_products': related_products,
    }
    return render(request,'core/details.html', context)


    

 # sign up page
def user_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request,"you're logged in")
                return redirect('home')
        else:
            HttpResponse('form is invalid and not saved.')

            return render(request, 'core/auth/signup.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'core/auth/signup.html', {'form': form})


# login in user with username and password
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request,f"you're logged in as {user}")
            return redirect('/')
        else:
            messages.success(request,"incorrect password or username")
    return render(request, 'core/auth/login.html')


def user_logout(request):
    logout(request)

    messages.success(request, "you been logged out !!!")
    return redirect('/')



def userprofile(request):
    profile = request.user.profile
    orders = Order.objects.filter(user=request.user).order_by("-created_at")[:5]

    # order_items = OrderItem.objects.all()
    # for order_item in order_items:
    #     print(f"full_name: {order_item.order.full_name}")
    #     print(f"order number: {order_item.order.order_number}")
    #     print(f"user: {order_item.order.user}")

    order_items = OrderItem.objects.select_related('order', 'order__user').filter(order__user=request.user)[:5]

    for order_item in order_items:
        print(f"full_name: {order_item.order.full_name}")
        print(f"order number: {order_item.order.order_number}")
        print(f"user: {order_item.order.user}")
        print(f"order status: {order_item.order.status}")
        print(f"total price: {order_item.total_price}\n")


    
    # for order in orders:
    #     for order_item in order.order_items.all():
    #         print(f"order item: {order_item}")
    #         print(f"user: {order_item}")
    #         print(f"product: {order_item.product}")
    #         print(f"produce price: {order_item.price}")
    #         print(f"product quantity: {order_item.quantity}")
    #         print(f"total_price: {order_item.total_price}\n")

    # for order in orders:
    #     order_items = order.order_items.all()
            
    
    context = {
        'profile': profile,
        'orders':orders,
        'order_items':order_items,
       
    }
    return render(request, 'core/userprofile.html', context)


def user_profile_update(request):
    profile = request.user.profile 
    form = UpdateProfileForm(instance=profile)
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('userprofile')
    # else:
    #     form = UpdateProfileForm(instance=profile)
        

    return render(request, 'core/profile_update.html', {'form': form,
                                                        'profile': profile})
    
    