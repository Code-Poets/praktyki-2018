from django.views import generic
from users.models import CustomUser
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.utils.translation import gettext as _


NO_USER_FOUND_MESSAGE = "No user found"


class DeleteUserView(generic.DeleteView):
    model = CustomUser
    template_name = 'users/delete_user.html'
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            raise Http404(NO_USER_FOUND_MESSAGE)
        else:
            if self.get_object() != self.request.user:
                raise Http404(NO_USER_FOUND_MESSAGE)
        return super(DeleteUserView, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        request.session['user_id'] = None
        return super(DeleteUserView, self).delete(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            return HttpResponseRedirect(reverse('edit_profile'))
        else:
            return super(DeleteUserView, self).post(request, *args, **kwargs)
