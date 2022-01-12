from django.urls import path
from .views import RegisterView, LoginView, Userview, LogoutView
from . import views

urlpatterns = [
    path('register',RegisterView.as_view()),
    path('login',LoginView.as_view()),
    path('user',Userview.as_view()),
    path('logout',LogoutView.as_view()),
    path('',views.home,name="home"),
    path('registerForm',views.home,name='registerform'),
    path('createUser',views.createUser,name='createUser'),
    path('loginUser',views.loginUser,name='loginUser'),
    path('loginUserProfile',views.createUser,name='createUser'),
    path('logoutUser',views.logoutUser,name='logoutUser'),
    path('updateUser/<str:username>/',views.updateUser,name='updateUser'),
    path('loginPage',views.loginPage,name='loginPage'),
    path('profile',views.profile,name='profile'),
    

]