from django import forms
from django.utils.translation import ugettext_lazy as _
from games.models import Game, Gamer, CharacterRace, CharacterClass, GENDER_CHOICES


class GamerForm(forms.ModelForm):
    class Meta:
        model = Gamer
        fields = ['status', 'level', 'bonus', 'gender', 'race_slot_1', 'race_slot_2', 'class_slot_1', 'class_slot_2']
    status = forms.CharField(label=_('Status'), required=False)
    level = forms.IntegerField(label=_('Level'), initial=1, min_value=1)
    bonus = forms.IntegerField(label=_('Bonus'), initial=0)
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    race_slot_1 = forms.ModelChoiceField(queryset=CharacterRace.objects.all(), required=False, label=_('Race'))
    race_slot_2 = forms.ModelChoiceField(queryset=CharacterRace.objects.all(), required=False)
    class_slot_1 = forms.ModelChoiceField(queryset=CharacterClass.objects.all(), required=False, label=_('Class'))
    class_slot_2 = forms.ModelChoiceField(queryset=CharacterClass.objects.all(), required=False)

    def clean(self):
        cleaned_data = super(GamerForm, self).clean()

        race1 = cleaned_data['race_slot_1']
        race2 = cleaned_data['race_slot_2']
        class1 = cleaned_data['class_slot_1']
        class2 = cleaned_data['class_slot_2']

        if class2 is not None and class1 is None:
            cleaned_data['class_slot_1'] = class2
            cleaned_data['class_slot_2'] = None
            self.class_slot_1 = class2
            self.class_slot_2 = None

        if race2 is not None and race1 is None:
            cleaned_data['race_slot_1'] = race2
            cleaned_data['race_slot_2'] = None

        return cleaned_data
