from django.urls import path
from . import views #impporta todas las funciones

urlpatterns = [
    path('', views.welcome,name='welcome'),
    path('login/', views.login_view,name='login'),
    path('register/',views.register, name='register'),
    path('verify_code/', views.verify_code, name='verify_code'),
    path('forgot_password/',views.forgot_password, name='forgot_password'),
    path('verify_reset_code/',views.verify_reset_code, name='verify_reset_code'),
    path('reset_password/',views.reset_password, name='reset_password'),
    path('logout/', views.logout_view, name="logout"),
    path('home/', views.home, name='home'),
    path("hacer-prediccion/", views.hacer_prediccion, name="hacer_prediccion"),
    path('error_404/', views.error_404, name='error_404'),
    path('crear_paciente/', views.crear_paciente, name='crear_paciente'),
    path('lista_pacientes/', views.lista_pacientes, name='lista_pacientes'),
    path('agregar_historia_clinica/<int:pk>/', views.agregar_historia_clinica, name='agregar_historia_clinica'),
    path('analisis_descrip_clinica/<int:pk>/', views.analisis_descrip_clinica, name='analisis_descrip_clinica'),
    path('historial_clinico/<int:pk>/', views.historial_clinico, name='historial_clinico'),
]