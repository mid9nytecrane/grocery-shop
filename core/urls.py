from django.urls import path 
from django.conf import settings 
from django.conf.urls.static import static
from core import views


urlpatterns = [
    path('', views.home, name='home'),
    path('details/<int:pk>/', views.detail, name='detail'),

    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),

    path('userprofile_page/',views.userprofile, name='userprofile'),
    path('profile_update/',views.user_profile_update, name='profile_update')
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
