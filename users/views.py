from .models import User
from .forms import RegisterForm, LoginForm, CodeForm
from django.views.generic.edit import CreateView,UpdateView,FormView
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout

class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'users/signup.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RegisterForm
        return context

    def post(self,request, *args,**kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit= False)
            user.is_active = False
            user.save()
        return redirect('users:confirm_user', request.POST['username'])


class ConfirmUser(UpdateView):
    model = User
    template_name = 'users/confirm_user.html'
    form_class = CodeForm
    def post(self,request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            code = form.save(commit=False)
            username = self.kwargs.get('username')
            # print('Username:',username)
            # print('Form:',form)
            # print('Code:',code.code)
            user= User.objects.get(username = username)
            if code.code == user.code:
                user.is_active = True
                user.save()
                return redirect('users:login')
            else:
                return redirect('users:signup')



    def get_object(self):
        username = self.kwargs.get('username')
        user = User.objects.get(username=username)
        print('Выводим пользователя',user)
        return user

class LoginView(FormView):
    model = User
    form_class = LoginForm
    template_name = 'users/login.html'
    success_url = '/'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)