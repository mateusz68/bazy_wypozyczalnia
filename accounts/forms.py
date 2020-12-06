from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm, UserChangeForm
from django.contrib.auth import (
    authenticate,
    get_user_model
)
from django.contrib.auth import forms as auth_forms
from accounts.models import Uzytkownik, MyAccountManager

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = Uzytkownik
        fields = '__all__'


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Uzytkownik
        fields = '__all__'


class RegisterFormFir(forms.ModelForm):
    password2 = forms.CharField(label='Powtórz hasło', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Powtórz hasło', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    nazwa_firmy = forms.CharField(required=True,  widget=forms.TextInput(attrs={'class': 'form-control'}))
    numer_nip = forms.IntegerField(required=True,  widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Uzytkownik
        fields = ['nazwa_firmy', 'numer_nip', 'ulica', 'miasto', 'kod_pocztowy', 'numer_telefonu', 'email', 'password']
        widgets = {
            'ulica': forms.TextInput(attrs={'class': 'form-control'}),
            'miasto': forms.TextInput(attrs={'class': 'form-control'}),
            'kod_pocztowy': forms.TextInput(attrs={'class': 'form-control'}),
            'numer_telefonu': forms.NumberInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_password(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Hasła nie pasują!")
        return password1

    def clean_numer_telefonu(self):
        numer = self.cleaned_data.get('numer_telefonu')
        if len(str(numer)) != 9:
            raise forms.ValidationError("Numer telefonu musi zawierać 9 cyfr!")
        return numer

    def clean_numer_nip(self):
        numer = self.cleaned_data.get('numer_nip')
        if len(str(numer)) != 10:
            raise forms.ValidationError("Numer nip musi zawierać 10 cyfr!")
        return numer


class RegisterFormPry(forms.ModelForm):
    password2 = forms.CharField(label='Powtórz hasło', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Powtórz hasło', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    imie = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    nazwisko = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Uzytkownik
        fields = ['imie', 'nazwisko', 'ulica', 'miasto', 'kod_pocztowy', 'numer_telefonu', 'email', 'password']
        widgets = {
            'ulica': forms.TextInput(attrs={'class': 'form-control'}),
            'miasto': forms.TextInput(attrs={'class': 'form-control'}),
            'kod_pocztowy': forms.TextInput(attrs={'class': 'form-control'}),
            'numer_telefonu': forms.NumberInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_password(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Hasła nie pasują!")
        return password1

    def clean_numer_telefonu(self):
        numer = self.cleaned_data.get('numer_telefonu')
        if len(str(numer)) != 9:
            raise forms.ValidationError("Numer telefonu musi zawierać 9 cyfr!")
        return numer


class UserLoginForm(forms.Form):
    email = forms.EmailField(label='Adres email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Hasło',widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError("Użytkownik nie istnieje")
            if not user.is_active:
                raise forms.ValidationError("Użytkownik nie aktywny")
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    #Formularz rejestracji
    email = forms.EmailField(label='Adres email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Hasło', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Powtórz hasło', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = [
            'email',
            'password1',
            'password2',
        ]
        # labels = {
        #     'pesel': 'Numer Pesel',
        #     'imie': 'Imię',
        #     'nazwisko': 'Nazwisko'
        # }
        #
        # widgets = {
        #     'pesel': forms.NumberInput(attrs={'class': 'form-control'}),
        #     'imie': forms.TextInput(attrs={'class': 'form-control'}),
        #     'nazwisko': forms.TextInput(attrs={'class': 'form-control'}),
        # }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Hasła nie pasują!")
        return password2

    def clean_pesel(self):
        pesel = self.cleaned_data.get("pesel")
        if len(str(pesel)) != 11:
            raise forms.ValidationError("Pesel musi zawierać 11 cyfr!")
        return pesel