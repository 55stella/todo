from django.urls import path
from .import views
urlpatterns = [
    


    path('signup/', views.signup),
    path('changepassword/', views.change_password),
    path('login/', views.user_login),
    path('profile/', views.profile),
    path('users/<int:user_id>/', views.user_detail)

    
]