from django.urls import path,include
from . import views

app_name = 'userprofile'

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('delete/<int:id>/', views.user_delete, name='delete'),
    #path('password-reset/', include('password_reset.urls')),
]