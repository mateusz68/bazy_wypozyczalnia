from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import (
    authenticate,
    get_user_model
)
from accounts.models import Uzytkownik, MyAccountManager

User = get_user_model()

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Powtórz hasło', widget=forms.PasswordInput)

    class Meta:
        model = Uzytkownik
        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = Uzytkownik.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Adres email jest zajęty")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Hasłą nie pasują!")
        return password2


class UserAdminCreationForm(forms.ModelForm):
    #Tworzenie nowego użytkownika
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Uzytkownik
        fields = ('email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Hasła nie pasują!")
        return password2


    def save(self, commit=True):
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    #Aktualizanie dnaych użytkownika
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Uzytkownik
        fields = ('email', 'password', 'active', 'rola')

    def clean_password(self):
        return self.initial["password"]

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