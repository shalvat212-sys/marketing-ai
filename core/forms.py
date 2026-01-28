from django import forms
from .models import MarketingPlan

class MarketingPlanForm(forms.ModelForm):
    class Meta:
        model = MarketingPlan
        fields = ['business_name', 'strengths']
        widgets = {
            'business_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'მაგ: შესაფუთი მასალები'
            }),
            'strengths': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'ჩამოწერეთ თქვენი უპირატესობები...'
            }),
        }