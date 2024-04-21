from .models import User
from .forms import RegisterForm, LoginForm
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
    context_object_name = 'confirm_user'
    template_name = 'users/confirm_user.html'
    def post(self,request, *args, **kwargs):
        if 'code' in request.post:
            user = User.objects.filter(code = request.POST('code'))
            if user.exists():
                user.update(is_active = True)
                user.update(code = None)

            else:
                return render(self.request, template_name='wrong_code.html')
            return redirect('login')


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