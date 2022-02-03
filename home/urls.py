from django.urls import path
from . import views


urlpatterns = [
    path('', views.signin, name='signin'), 
    path('home/', views.home, name='home'),    
    path('register/', views.signup, name='signup'),   
    path('logout/', views.signout, name='signout'),     
    path('delete_other/<str:email>', views.delete_other),
    path('delete_own/<str:username>', views.delete_own),    
    path('edit/<str:email>', views.edit),
    path('update/<str:email>', views.update),
    path('password_change/', views.password_change, name='password_change'),     
    
    
]
