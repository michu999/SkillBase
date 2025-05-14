from django import forms
from .models import User, Skill

class UserForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),  # Initially all skills
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'skills']

class CityForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['city']
        widgets = {
            'city': forms.TextInput(attrs={'class': 'form-control'}),
        }