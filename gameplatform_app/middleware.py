from django.shortcuts import redirect
from .models import Usuario

class AutenticacaoMiddleware:
    """
    Middleware para verificar se o usuário está autenticado
    usando a sessão.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        usuario_id = request.session.get('usuario_id')

        if usuario_id:
            try:
                request.usuario = Usuario.objects.get(pk=usuario_id)
            except Usuario.DoesNotExist:
                request.usuario = None
                del request.session['usuario_id']
        else:
            request.usuario = None

        response = self.get_response(request)
        return response
