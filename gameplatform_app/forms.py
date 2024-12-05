from django import forms
from django.contrib.auth.hashers import make_password, check_password
from .models import UsuarioNaoAdministrativo

class CadastroForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput, label="Senha")
    confirmar_senha = forms.CharField(widget=forms.PasswordInput, label="Confirmar Senha")

    class Meta:
        model = UsuarioNaoAdministrativo
        fields = ['nome', 'enderecoEmail', 'foto', 'senha']

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get('senha')
        confirmar_senha = cleaned_data.get('confirmar_senha')

        if senha != confirmar_senha:
            raise forms.ValidationError("As senhas não coincidem.")

        # Hash da senha antes de salvar
        cleaned_data['senha'] = make_password(senha)
        return cleaned_data


class LoginForm(forms.Form):
    enderecoEmail = forms.EmailField(label="Email")
    senha = forms.CharField(widget=forms.PasswordInput, label="Senha")

    def authenticate(self):
        email = self.cleaned_data.get('enderecoEmail')
        senha = self.cleaned_data.get('senha')
        try:
            usuario = UsuarioNaoAdministrativo.objects.get(enderecoEmail=email)
            if check_password(senha, usuario.senha):
                return usuario
        except UsuarioNaoAdministrativo.DoesNotExist:
            pass
        return None

from django import forms

class AvaliacaoForm(forms.Form):
    estrelas = forms.IntegerField(min_value=0, max_value=5, label='Estrelas')
    review = forms.CharField(widget=forms.Textarea, label='Review')

class DenunciaForm(forms.Form):
    detalhes = forms.CharField(widget=forms.Textarea, label='Detalhes da Denúncia')

class RelatarBugsForm(forms.Form):
    detalhes = forms.CharField(widget=forms.Textarea, label='Detalhes do Bug')
