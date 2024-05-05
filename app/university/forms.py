from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from university.models import student_model, group_model


# Create your forms here.

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(), )

    def login(self):
        data = self.cleaned_data
        user = authenticate(username=data['username'], password=data['password'])
        return user


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit: user.save()
        return user


class ProfileForm(forms.ModelForm):
    group = forms.ModelChoiceField(queryset=group_model.objects.all())

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance and instance.group:
            self.fields.pop('group')

    class Meta:
        model = student_model
        fields = ['last_name', 'first_name', 'patronymic', 'birthday', 'group']

        widgets = {
            'birthday': forms.TextInput(attrs={'type': 'date'}),
        }
