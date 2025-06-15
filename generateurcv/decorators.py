# generateurcv/decorators.py
from django.shortcuts import redirect
from functools import wraps

def utilisateur_site_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'utilisateur_id' not in request.session:
            return redirect('login')  # Redirection si pas connecté
        return view_func(request, *args, **kwargs)
    return wrapper
