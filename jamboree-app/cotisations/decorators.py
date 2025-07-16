# cotisations/decorators.py
from django.core.exceptions import PermissionDenied

def admin_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.role == 'ADMIN':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap

def participant_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.role == 'PARTICIPANT':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap