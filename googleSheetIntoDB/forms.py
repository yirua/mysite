#mysite/mysite/forms.py

from django import forms

from .models import Metadata

class GoogleSheetForm(forms.ModelForm):

    class Meta:

        model = Metadata

        fields = ('title','trial_year','trial', 'treatment', 'city','farm')


class PathForm(forms.Form):
    json_path = forms.CharField(label='Your json file path', max_length = 200)
    trial_year = forms.IntegerField(label='Trial year')