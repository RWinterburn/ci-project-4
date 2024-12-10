from django import forms
from .models import Beat

class BeatForm(forms.ModelForm):
    class Meta:
        model = Beat
        fields = ['title', 'producer', 'price', 'cover_image', 'audio_file', 'description', 'release_date']
