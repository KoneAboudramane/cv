from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CV, Experience, Education, Skill, Language, Interest, ModeleCV



# ==== Formulaires Utilisateur ====

from django import forms
from .models import UtilisateurSite

class InscriptionForm(forms.ModelForm):
    password = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400'
        })
    )
    confirm_password = forms.CharField(
        label='Confirmer le mot de passe',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400'
        })
    )

    class Meta:
        model = UtilisateurSite
        fields = ['nom_complet', 'email', 'photo']
        widgets = {
            'nom_complet': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return cleaned_data



# ==== Formulaires CV ====

# Formulaire pour le CV
class CVForm(forms.ModelForm):
    class Meta:
        model = CV
        fields = ['titre', 'full_name', 'title', 'email', 'phone', 'summary', 'photo', 'version']
    modele = forms.ModelChoiceField(queryset=ModeleCV.objects.all(), required=False)

# Formulaire pour l'expérience
class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['position', 'company', 'date', 'description']

# Formulaire pour l'éducation
class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['degree', 'institution', 'date', 'description']

# Formulaire pour les compétences
class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'level']

# Formulaire pour les langues
class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ['name', 'level']

# Formulaire pour les intérêts
class InterestForm(forms.ModelForm):
    class Meta:
        model = Interest
        fields = ['name']
