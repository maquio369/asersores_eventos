from django.http import HttpResponsePermanentRedirect

class ForceHTTPMiddleware:
    """
    Middleware para forzar HTTP en lugar de HTTPS
    Útil cuando no tienes certificado SSL configurado
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Si la petición viene por HTTPS, redirigir a HTTP
        if request.is_secure():
            url = request.build_absolute_uri().replace('https://', 'http://')
            return HttpResponsePermanentRedirect(url)
        
        response = self.get_response(request)
        return response