from django.shortcuts import render,redirect,get_object_or_404, HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

from .forms import SignUpForm,UpdateProfileForm

from core.models import Product


# Create your views here.

def home(request):
    products = Product.objects.all()

    context={
        'products': products,
    }

    return render(request, 'core/home.html', context)


def detail(request,pk):
    product = get_object_or_404(Product,id=pk)
    context = {
        'product':product,
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
    return render(request, 'core/userprofile.html', {'profile': profile})


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
    
    