# cotisations/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Cotisation

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmer le mot de passe")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        labels = {
            'username': "Nom d'utilisateur",
            'first_name': 'Prénom',
            'last_name': 'Nom de famille',
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Les mots de passe ne correspondent pas.')
        return cd['password2']

class CotisationForm(forms.ModelForm):
    class Meta:
        model = Cotisation
        fields = ['montant', 'methode_paiement', 'description']
        labels = {
            'montant': 'Montant (F CFA)',
            'methode_paiement': 'Méthode de paiement',
            'description': 'Description (optionnel)',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }