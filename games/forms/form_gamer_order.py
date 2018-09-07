from django import forms
from .form_gamer import GamerForm
from django.utils.translation import ugettext_lazy as _
from games.models.model_gamer import Gamer


class GamerOrderForm(GamerForm):
    class Meta(GamerForm.Meta):
        model = Gamer
        fields = GamerForm.Meta.fields + ['order']
    order = forms.IntegerField(label=_('Order'), initial=1, min_value=1, required=False)

    def clean(self):
        cleaned_data = super(GamerOrderForm, self).clean()
        order = self.cleaned_data['order']

        gamers = self.instance.game.gamers.all()
        error = False
        for gamer in gamers:
            if gamer.id is not self.instance.id and order is not None and gamer.order == order:
                error = True
        if error is True:
            raise forms.ValidationError(_('This order has already been taken :('))
        return cleaned_data
