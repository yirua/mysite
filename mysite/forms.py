#mysite/mysite/forms.py

from django import forms

from .models import Metadata

class GoogleSheetForm(forms.ModelForm):

    class Meta:

        model = Metadata

        fields = ('trial', 'Treatment', 'City','Farm')


class PathForm(forms.Form):
    your_path = forms.CharField(label='Your path', max_length = 200)