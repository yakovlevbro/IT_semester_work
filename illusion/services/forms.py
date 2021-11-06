from django import forms
from .models import Service, Feedback


class ServiceForm(forms.ModelForm):

    class Meta:
        model = Service
        fields = '__all__'


class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback
        fields = ['rating', 'text']