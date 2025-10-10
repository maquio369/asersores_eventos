from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Dashboard y autenticación
    path('', views.dashboard, name='dashboard'),
    path('exportar-excel/', views.exportar_eventos_excel, name='exportar_eventos_excel'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Gestión de eventos
    path('eventos/crear/', views.crear_evento, name='crear_evento'),
    path('eventos/', views.mis_eventos, name='mis_eventos'),
    path('eventos/<int:evento_id>/', views.detalle_evento, name='detalle_evento'),
    path('eventos/<int:evento_id>/editar/', views.editar_evento, name='editar_evento'),
    path('eventos/<int:evento_id>/cancelar/', views.cancelar_evento, name='cancelar_evento'),
    path('eventos/<int:evento_id>/pdf/', views.descargar_pdf, name='descargar_pdf'),
    path('calendario/', views.calendar_view, name='calendar_view'),
    
    # Municipios
    path('municipios/', views.lista_municipios, name='lista_municipios'),

    # Perfil de usuario
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    
    # Administración (solo admin)
    path('gestion/usuarios/', views.gestionar_usuarios, name='gestionar_usuarios'),
    path('gestion/usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('gestion/usuarios/<int:user_id>/editar/', views.editar_usuario, name='editar_usuario'),
    path('gestion/usuarios/<int:user_id>/toggle/', views.toggle_user_status, name='toggle_user_status'),
    
    # API endpoints
    path('api/user-permissions/', views.check_user_permissions, name='check_user_permissions'),
    
]
