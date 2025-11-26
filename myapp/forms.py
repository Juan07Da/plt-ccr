from django import forms
from .models import AppUser,Paciente,HistoriaClinica, AnalisisFinal
from django.forms.models import inlineformset_factory

class AppUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = AppUser
        fields = ['first_name', 'last_name', 'email', 'password']

class PacienteForm(forms.ModelForm):
    pais_nacimiento = forms.CharField(
        initial='Colombia',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        label="País de Nacimiento"
    )
    
    class Meta:
        model = Paciente
        exclude = ('edad',)
        
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-control custom-select'

class HistoriaClinicaForm(forms.ModelForm):
    class Meta:
        model = HistoriaClinica
        fields = [
            'sintomas_actuales', 
            'tratamientos_actuales', 
            'diagnostico_principal', 
            'otras_comorbilidades'
        ]
        
        # Opcional: Widgets para que se vean mejor (ej. con clases de Bootstrap)
        widgets = {
            'sintomas_actuales': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tratamientos_actuales': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'diagnostico_principal': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'otras_comorbilidades': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
        labels = {
            'diagnostico_principal': 'Diagnóstico del Profesional',
        }


class AnalisisFinalForm(forms.ModelForm):
    class Meta:
        model = AnalisisFinal
        fields = ['paciente', 'predicciones_nlp', 'diagnostico_final']
        
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-select'}),
            # El JSONField se renderiza como un área de texto por defecto, aquí le damos formato
            'predicciones_nlp': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Datos JSON generados por el modelo...'}),
            'diagnostico_final': forms.Select(attrs={'class': 'form-select'}),
        }