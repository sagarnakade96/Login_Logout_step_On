from django.http import request, response
from django.shortcuts import redirect, render
from rest_framework.views import APIView
from myapp.serializers import AccountSerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from .models import Account
from .forms import AccountForm
import jwt, datetime
import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
class RegisterView(APIView):
    def post(self,request):
        serializer = AccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


def createUser(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        if pass1 == pass2:
            password = pass1
        data = {
            'name':name,
            'email':email,
            'password':password,
            'username':username,
            
        }

        headers = {'Content-Type': 'application/json'}
        read = requests.post('http://localhost:8000/api/register', json=data, headers=headers)
        messages.success(request, 'Registration Successfull!')
        return render(request,'login.html')
    else:
        return render(request,'login.html')


class LoginView(APIView):
       def post(self,request):
           username=request.data['username']
           password = request.data['password']

           user = Account.objects.filter(username=username).first()

           if user is None:
               raise AuthenticationFailed('User Not Found!!!')
            
           if not user.check_password(password):
               raise AuthenticationFailed('Incorrect Password!!!')
           
           payload={
               'id':user.id,
               'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
               'iat':datetime.datetime.utcnow()
           }

           token = jwt.encode(payload,'secret', algorithm='HS256')

           response = Response()
           
           response.data={
                   "username":username,
                   "jwt":token
               }
             
           response.set_cookie(key='jwt', value=token, httponly=True)
           return response

def profile(request):
    form = AccountForm()
    context = {'form':form}
    if request.method == 'POST':
        form=AccountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('loginUser')
    return render(request,'profile.html',context)

def updateUser(request,pk):
    pass

def loginUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('userpassword')
       
        data = {
            
            'username':username,
            'password':password,            
        }

        headers = {'Content-Type': 'application/json'}
        read = requests.post('http://localhost:8000/api/login', json=data, headers=headers)
        user = authenticate(username=username , password=password)
        login(request,user)
        messages.success(request, 'Logged in successfully!')
        return render(request,'login.html',data)
    else:
        return render(request,'register.html')
    return HttpResponse('404 Not Found')


class Userview(APIView):
    def get(self,request):
        token = request.COOKIES.get('jwt')
        
        if not token:
            raise AuthenticationFailed('User Authentication Failed!!!')
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        
        user = Account.objects.filter(id = payload['id']).first()
        serializer = AccountSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response

def logoutUser(request):
    if request.method == "GET":
        read = requests.get('http://localhost:8000/api/logout')
        logout(request)
        messages.success(request, 'Logged out successfully!')
        return render(request,'login.html')
    else:
        return render(request,'register.html')
    return HttpResponse('404 Not Found')

def home(request):
    return render(request,'register.html')

def loginPage(request):
    return render(request,'login.html')

