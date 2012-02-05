from django import forms

class CriarPlanilha(forms.Form):
    nome_planilha = forms.CharField()
    colaborador = forms.ComboField()
    usuario_pmo = forms.CharField()
    senha_pmo = forms.CharField(widget=forms.PasswordInput(render_value=True))