from django.shortcuts import redirect
from users.forms.form_custom_user_change import  CustomUserChangeForm
from django.shortcuts import render


def CustomUser_update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('edit_profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {
        'user_form': form,
    })
