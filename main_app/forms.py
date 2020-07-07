from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

class RegisterForm(forms.ModelForm):

    password2 = forms.CharField(min_length=8, widget=forms.PasswordInput(attrs={'class':'form-control'}), required=True)

    class Meta:
        model = User
        fields = ('username',  'email', 'password')

        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        data = super().clean()
        if data.get('password') != data.get('password2'):
            raise forms.ValidationError('Password must be exact.')
        return data

class AuthForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                                required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                required=True)

    def clean(self):
        data = super().clean()
        try:
            user = User.objects.get(username=data.get('username'))
            if not check_password(data.get('password'), user.password):
                self.add_error('username', f'User {data.get("username")} doesn\'t exist or password is invalid.')
                raise forms.ValidationError('Invalid password.')
        except User.DoesNotExist:
            self.add_error('username', f'User {data.get("username")} doesn\'t exist or password is invalid.')
            raise forms.ValidationError(f'User {data.get("username")} doesn\'t exist.')
        self.user = user
        return data