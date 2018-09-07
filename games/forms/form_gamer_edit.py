from .form_gamer import GamerForm
from django.utils.translation import ugettext_lazy as _
from games.models.model_gamer import Gamer


class GamerEditForm(GamerForm):
    class Meta(GamerForm.Meta):
        model = Gamer

    def __init__(self, *args, **kwargs):
        super(GamerEditForm, self).__init__(*args, **kwargs)
        self.fields.pop('status')
