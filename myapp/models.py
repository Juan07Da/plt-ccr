import random
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from datetime import date
from django.db.models import JSONField

class AppUser(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Guardada encriptada
    verification_code = models.CharField(max_length=6, blank=True, null=True)

    def save(self, *args, **kwargs):
        """Hashea la contraseña antes de guardar el usuario."""
        if not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        """Verifica si la contraseña ingresada es correcta."""
        return check_password(raw_password, self.password)

    def generate_verification_code(self):
        """Genera un código de 6 dígitos y lo guarda en el modelo"""
        self.verification_code = str(random.randint(100000, 999999))
        self.save()

class Paciente(models.Model):
    # Opciones para campos de selección
    TIPO_ID_CHOICES = (
        ('CC', 'Cédula de Ciudadanía'),
        ('TI', 'Tarjeta de Identidad'),
        ('CE', 'Cédula de Extranjería'),
        ('PA', 'Pasaporte'),
    )

    ESTADO_CIVIL_CHOICES = (
        ('SOLTERO', 'Soltero/a'),
        ('CASADO', 'Casado/a'),
        ('DIVORCIADO', 'Divorciado/a'),
        ('VIUDO', 'Viudo/a'),
        ('UNION_LIBRE', 'Unión Libre'),
    )

    SEXO_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    )

    # --- Columnas Requeridas ---
    tipo_identificacion = models.CharField(
        max_length=3,
        choices=TIPO_ID_CHOICES,
        default='CC',
        verbose_name="Tipo de Identificación"
    )
    numero_identificacion = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Número de Identificación"
    )
    primer_nombre = models.CharField(max_length=100, verbose_name="Primer Nombre")
    segundo_nombre = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Segundo Nombre"
    )
    primer_apellido = models.CharField(max_length=100, verbose_name="Primer Apellido")
    segundo_apellido = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Segundo Apellido"
    )
    estado_civil = models.CharField(
        max_length=15,
        choices=ESTADO_CIVIL_CHOICES,
        verbose_name="Estado Civil"
    )
    fecha_nacimiento = models.DateField(verbose_name="Fecha de Nacimiento")
    pais_nacimiento = models.CharField(
        max_length=100,
        default='Colombia',
        verbose_name="País de Nacimiento"
    )
    # NOTA: La edad se calculará automáticamente en el modelo o en la vista.
    sexo = models.CharField(
        max_length=1,
        choices=SEXO_CHOICES,
        verbose_name="Sexo"
    )
    direccion_residencia = models.CharField(
        max_length=255,
        verbose_name="Dirección de Residencia"
    )
    telefono = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name="Teléfono"
    )
    grupo_etnico = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Grupo Étnico"
    )

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        ordering = ['primer_apellido', 'primer_nombre']

    def __str__(self):
        return f"{self.primer_nombre} {self.primer_apellido} ({self.numero_identificacion})"

    # Método para calcular la edad (ejemplo: se usa en plantillas o vistas)
    def calcular_edad(self):
        today = date.today()
        # Se calcula la diferencia restando 1 si la fecha de cumpleaños no ha pasado
        return today.year - self.fecha_nacimiento.year - ((today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))

    edad = property(calcular_edad)

class HistoriaClinica(models.Model):
    # Enlace al paciente
    paciente = models.ForeignKey(
        'Paciente', 
        on_delete=models.CASCADE,
        related_name='historias',
        verbose_name="Paciente"
    )
    
    fecha_visita = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha y Hora de la Visita"
    )
    
    sintomas_actuales = models.TextField(
        verbose_name="Síntomas del Paciente"
    )

    tratamientos_actuales = models.TextField(
        verbose_name="Tratamientos/Examenes realizados"
    )
    
    diagnostico_principal = models.TextField(
        verbose_name="Diagnóstico del Profesional"
    )
    
    otras_comorbilidades = models.TextField(
        blank=True,
        null=True,
        verbose_name="Otras Comorbilidades y Antecedentes"
    )

    # Se eliminaron: predicciones y diagnostico_final
    
    class Meta:
        verbose_name = "Historia Clínica"
        verbose_name_plural = "Historias Clínicas "
        ordering = ['-fecha_visita'] 

    def __str__(self):
        return f"HC #{self.pk} - {self.paciente.primer_apellido} ({self.fecha_visita.strftime('%Y-%m-%d')})"
    
class AnalisisFinal(models.Model):
    DIAGNOSTICO_FINAL_CHOICES = (
        ('CCR', 'Cáncer Colorrectal'),
        ('CO', 'Paciente Control'),
    )

    # Conexión con el modelo Paciente
    paciente = models.ForeignKey(
        'Paciente',
        on_delete=models.CASCADE,
        related_name='analisis_finales',
        verbose_name="Paciente"
    )

    # Columna para guardar el JSON del modelo NLP
    predicciones_nlp = models.JSONField(
        verbose_name="Predicciones NLP (JSON)"
    )

    # Columna para el diagnóstico final
    diagnostico_final = models.CharField(
        max_length=3,
        choices=DIAGNOSTICO_FINAL_CHOICES,
        verbose_name="Diagnóstico Final"
    )

    # (Opcional) Fecha de registro para mantener orden
    fecha_analisis = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Fecha del Análisis"
    )

    class Meta:
        verbose_name = "Análisis Final"
        verbose_name_plural = "Análisis Finales"
        ordering = ['-fecha_analisis']

    def __str__(self):
        return f"Análisis: {self.get_diagnostico_final_display()} - {self.paciente.primer_apellido}"
    
class RecursoMedico(models.Model):
    TIPO_CHOICES = (
        ('LIBRO', 'Libro / Guía'),
        ('ARTICULO', 'Artículo Científico'),
        ('VIDEO', 'Video / Conferencia'),
    )

    titulo = models.CharField(max_length=200, verbose_name="Título del Recurso")
    autor = models.CharField(max_length=150, verbose_name="Autor / Institución")
    descripcion = models.TextField(verbose_name="Breve Descripción")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='ARTICULO')
    
    # Aquí guardamos el link externo (PDF, web, youtube)
    url_recurso = models.URLField(verbose_name="Enlace al recurso")
    
    # Opcional: Una imagen de portada (si no quieres complicarte con imágenes, podemos usar iconos genéricos en el HTML)
    imagen_url = models.URLField(blank=True, null=True, verbose_name="URL de Imagen de Portada (Opcional)")

    fecha_publicacion = models.DateField(blank=True, null=True, verbose_name="Fecha de Publicación")

    def __str__(self):
        return self.titulo
    
class Noticia(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Titular de la Noticia")
    resumen = models.TextField(verbose_name="Resumen Breve")
    
    # Guardamos el link de la noticia original
    url_noticia = models.URLField(verbose_name="Enlace a la Noticia Completa")
    
    # Guardamos el link de una imagen para la portada
    url_imagen = models.URLField(verbose_name="URL de la Imagen de Portada")
    
    fuente = models.CharField(max_length=100, verbose_name="Nombre de la Fuente (Ej. El Tiempo)")
    fecha_publicacion = models.DateField(auto_now_add=True, verbose_name="Fecha de Publicación")

    class Meta:
        verbose_name = "Noticia"
        verbose_name_plural = "Noticias"
        ordering = ['-fecha_publicacion'] # Las más recientes primero

    def __str__(self):
        return self.titulo