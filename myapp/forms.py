from django import forms
from .models import AppUser,Paciente,HistoriaClinica, AnalisisFinal, AppUser
from django.forms.models import inlineformset_factory
import re
from django.core.exceptions import ValidationError


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



class PerfilForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input-nex', 
            'placeholder': 'Dejar en blanco para no cambiar'
        }),
        required=False,
        label="Nueva Contraseña"
    )

    class Meta:
        model = AppUser
        fields = ['first_name', 'last_name', 'email', 'password']
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo Electrónico',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input-nex'}),
            'last_name': forms.TextInput(attrs={'class': 'input-nex'}),
            'email': forms.EmailInput(attrs={'class': 'input-nex'}),
        }

    def clean_password(self):
        """
        Valida que la contraseña cumpla con los requisitos de seguridad
        solo si el usuario ha ingresado algo.
        """
        password = self.cleaned_data.get('password')

        # Si el campo está vacío, significa que NO quiere cambiar la contraseña.
        # Retornamos None o vacío y salimos sin validar.
        if not password:
            return None

        # --- APLICANDO REGLAS DE SEGURIDAD (Idénticas al registro) ---

        # 1. Longitud: al menos 8 caracteres.
        if len(password) < 8:
            raise ValidationError('La contraseña debe tener al menos 8 caracteres.')
        
        # 2. Al menos 2 letras mayúsculas
        if len(re.findall(r'[A-Z]', password)) < 2:
            raise ValidationError('La contraseña debe incluir al menos 2 letras mayúsculas.')
        
        # 3. Al menos 2 letras minúsculas
        if len(re.findall(r'[a-z]', password)) < 2:
            raise ValidationError('La contraseña debe incluir al menos 2 letras minúsculas.')
        
        # 4. Al menos 3 números
        if len(re.findall(r'\d', password)) < 3:
            raise ValidationError('La contraseña debe incluir al menos 3 números.')
        
        # 5. Al menos 1 carácter especial
        if not re.search(r'[^\w\s]', password):
            raise ValidationError('La contraseña debe incluir al menos 1 carácter especial.')

        return password