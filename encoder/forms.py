from django import forms
from .models import Encoder

class EncoderForm(forms.ModelForm):
    class Meta:
        model = Encoder
        fields = '__all__'
