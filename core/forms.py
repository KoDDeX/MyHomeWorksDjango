from django import forms
from .models import Review, Master

class ReviewForm(forms.ModelForm):

    master = forms.ModelChoiceField(queryset = Master.objects.all())

    class Meta:
        model = Review
        fields = ['client_name', 'text', 'rating', 'master', 'photo']