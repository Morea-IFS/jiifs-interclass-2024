from django.shortcuts import redirect
from .models import Terms_Use

class CheckTermosMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if not Terms_Use.objects.filter(usuario=request.user).exists():
                if request.path != "/termos-de-uso/":
                    return redirect('termos_uso')
        
        return self.get_response(request)
