from django.contrib import admin
from .models import AppUser, Paciente, HistoriaClinica, AnalisisFinal

@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    # Campos que se mostrarán en la lista de usuarios en el admin
    list_display = ('email', 'first_name', 'last_name', 'verification_code')
    
    # Campos por los que se puede buscar
    search_fields = ('email', 'first_name', 'last_name')
    
    # Filtros laterales
    list_filter = ('verification_code',) 
    
    # Para la edición individual:
    # Agrupa los campos para que la vista de edición sea más limpia
    fieldsets = (
        (None, {
            'fields': ('email', 'first_name', 'last_name')
        }),
        ('Seguridad y Verificación', {
            # Importante: No mostrar el campo 'password' ya que no se puede editar directamente de forma segura
            'fields': ('verification_code',),
            'classes': ('collapse',) # Opcional: oculta esta sección por defecto
        }),
    )
    
    # Evita que se muestren los campos de contraseña en la edición y creación
    # ya que tu método `save` maneja el hasheo de forma segura.
    # En un proyecto real, se usaría UserAdmin o un formulario específico para cambiar contraseñas.
    readonly_fields = ('verification_code',)

    # Sobreescribe el método para que no se muestre el campo 'password' en el formulario de edición
    # Aunque no se muestra en `fieldsets`, esto es una buena práctica para asegurar.
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        if not is_superuser:
            form.base_fields['password'].widget.attrs['disabled'] = True
        return form

# --- 1. Inline para Historia Clínica ---
# Define cómo se mostrarán las Historias Clínicas dentro del Paciente
class HistoriaClinicaInline(admin.TabularInline):
    # Indica el modelo que se va a mostrar
    model = HistoriaClinica
    # Campos que se muestran en el inline
    fields = ('fecha_visita', 'sintomas_actuales', 'diagnostico_principal', 'otras_comorbilidades')
    # Hace que el campo de texto sea más grande
    extra = 1  # Permite añadir 1 historia clínica vacía por defecto
    readonly_fields = ('fecha_visita',) # La fecha se genera automáticamente

# --- 2. Admin del Modelo Paciente ---
# Clase personalizada para la visualización del Paciente
@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    # Campos que se muestran en la lista de pacientes
    list_display = (
        'numero_identificacion',
        'primer_nombre',
        'primer_apellido',
        'edad', # Usamos la propiedad calculada 'edad'
        'telefono',
        'estado_civil'
    )
    
    # Campos por los que se puede filtrar
    list_filter = ('estado_civil', 'sexo', 'tipo_identificacion')
    
    # Campos por los que se puede buscar (usa __icontains para búsqueda insensible a mayúsculas)
    search_fields = (
        'numero_identificacion',
        'primer_nombre',
        'primer_apellido',
        'telefono'
    )
    
    # Organización de los campos en la vista de detalle
    fieldsets = (
        ('Información Personal Básica', {
            'fields': (
                ('tipo_identificacion', 'numero_identificacion'),
                ('primer_nombre', 'segundo_nombre'),
                ('primer_apellido', 'segundo_apellido'),
            ),
        }),
        ('Detalles Demográficos', {
            'fields': (
                ('fecha_nacimiento', 'sexo', 'estado_civil'),
                ('pais_nacimiento', 'grupo_etnico'),
            ),
        }),
        ('Contacto y Residencia', {
            'fields': (
                'direccion_residencia',
                'telefono',
            ),
        }),
    )
    
    # Añadimos el Inline para que las Historias Clínicas aparezcan
    # en la misma página de edición del Paciente
    inlines = [HistoriaClinicaInline]

# --- 3. Admin del Modelo HistoriaClinica (Registro individual) ---
# Opcional: Para gestionar las Historias Clínicas de forma individual también
@admin.register(HistoriaClinica)
class HistoriaClinicaAdmin(admin.ModelAdmin):

    # Muestra el paciente y la fecha en la lista
    list_display = ('paciente_display', 'fecha_visita', 'diagnostico_principal')
    
    # Permite buscar por campos relacionados del paciente
    search_fields = ('paciente__primer_nombre', 'paciente__primer_apellido', 'diagnostico_principal')
    
    # Filtro por fecha
    list_filter = ('fecha_visita',)
    
    # Método para mostrar el nombre completo del paciente
    def paciente_display(self, obj):
        return f"{obj.paciente.primer_nombre} {obj.paciente.primer_apellido}"
    
    paciente_display.short_description = 'Paciente'


@admin.register(AnalisisFinal)
class AnalisisFinalAdmin(admin.ModelAdmin):
    # Muestra el paciente, el resultado (CCR/CO) y la fecha
    list_display = ('paciente', 'diagnostico_final', 'fecha_analisis')
    
    # Permite buscar por nombre del paciente o su identificación
    search_fields = ('paciente__primer_nombre', 'paciente__primer_apellido', 'paciente__numero_identificacion')
    
    # Filtros laterales para ver rápidamente cuántos CCR o CO hay
    list_filter = ('diagnostico_final', 'fecha_analisis')