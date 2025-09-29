from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages

def admin_required(function):
    """Decorador que requiere que el usuario sea administrador"""
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_admin_user():
            return function(request, *args, **kwargs)
        else:
            messages.error(request, 'No tienes permisos para acceder a esta sección.')
            return redirect('dashboard')
    return wrap

def captura_or_admin_required(function):
    """Decorador que permite acceso a usuarios de captura y administradores"""
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_admin_user() or request.user.is_captura_user()):
            return function(request, *args, **kwargs)
        else:
            messages.error(request, 'No tienes permisos para acceder a esta sección.')
            return redirect('login')
    return wrap

def active_user_required(function):
    """Decorador que requiere que el usuario esté activo"""
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_active:
            return function(request, *args, **kwargs)
        else:
            messages.error(request, 'Tu cuenta no está activa. Contacta al administrador.')
            return redirect('login')
    return wrap
