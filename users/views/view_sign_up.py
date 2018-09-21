from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import redirect
from users.forms.form_custom_user_creation import CustomUserCreationForm


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super(SignUp, self).dispatch(request, *args, **kwargs)
