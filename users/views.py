import os
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, reverse
from django.views.generic import FormView
from django.views import View
from django.urls import reverse_lazy
from . import forms
# Create your views here.

class LoginView(FormView):

    form_class = forms.LoginForm
    template_name = "users/login.html"
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)




def log_out(request):
    logout(request)
    return redirect("core:home")

class SignUpView(FormView):

    form_class = forms.SignUpForm
    template_name = "users/signup.html"
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        print(username, password)
        user = authenticate(self.request, username=username, password=password)
        print(user)
        if user is not None:
            login(self.request, user)
            print("login~~~")
        return super().form_valid(form)

def login_github(request):
    

def login_github_callback(request):
    pass

def login_kakao(request):
    pass

def login_kakao_callback(request):
    pass









class LoginView_가내수공업(View):
    
    def get(self, request):
        form = forms.LoginForm(initial={"username":"songys"})
        return render(request, "users/login.html", context={"form":form})

    def post(self, request):
        """
        work flow - form 인스턴스를 먼저 만들고 is_valid과정에서 form.clean()으로 넘어감
        """
        form = forms.LoginForm(request.POST)
        print("------------")
        if form.is_valid():
            print("valid")
            username = form.cleaned_data.get("username")
            print(username)
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                
            return redirect(reverse("core:home"))
        return render(request, "users/login.html", {"form":form})
