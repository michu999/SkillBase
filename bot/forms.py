from django import forms
from .models import User, City

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['skills', 'city']

class CityForm(forms.Form):
    city_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your city'})
    )
    # Custom validation for city name, ensures it is not empty
    def clean_city_name(self):
        city_name = self.cleaned_data.get('city_name')
        if not city_name:
            raise forms.ValidationError("City name is required.")
        return city_name



