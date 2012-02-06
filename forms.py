from django import forms
from horasdsconapp.pmo.pmo import Pmo
import settings

class CriarPlanilha(forms.Form):
    nome_planilha = forms.CharField(widget=forms.TextInput(attrs={'value':settings.NOME_PLANILHA_HORAS, 'readonly':'readonly', 'style':'background:#eee none; color:#222;'}))
    usuario_pmo = forms.CharField(required=True)
    senha_pmo = forms.CharField(required=True, widget=forms.PasswordInput(render_value=True))

    def clean(self):
        pmo = Pmo()
        user = self.cleaned_data.get('usuario_pmo')
        password = self.cleaned_data.get('senha_pmo')
        try:
            cookies = pmo.login(user, password)

        except Exception, err:
            raise forms.ValidationError(err.message)
        return self.cleaned_data
