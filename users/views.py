from .models import User
from .forms import RegisterForm
from django.views.generic.edit import CreateView,UpdateView
from django.shortcuts import render,redirect

class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'users/signup.html'
    success_url = '/users/confirm_user'



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
                return  render(self.request, template_name='wrong_code.html')
            return redirect('users/login')

