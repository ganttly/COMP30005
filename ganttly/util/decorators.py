from django.conf import settings
from django.http import HttpResponseRedirect
from ganttly.models import Project

def secure_required(view_func):
    """Decorator makes sure URL is accessed over https."""
    def _wrapped_view_func(request, *args, **kwargs):
        if not request.is_secure():
            if getattr(settings, 'HTTPS_SUPPORT', True):
                request_url = request.build_absolute_uri(request.get_full_path())
                secure_url = request_url.replace('http://', 'https://')
                return HttpResponseRedirect(secure_url)
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func

def login_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.is_authenticated():
            pass
        else:
            return HttpResponseRedirect('/ganttly/')
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func

def project_admin_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        project = Project.objects.get(id=kwargs['project_id'])
        if request.user != project.admin:
            return HttpResponseRedirect('/ganttly/projects/')
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func

def project_member_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        project = Project.objects.get(id=kwargs['project_id'])
        team = project.team

        if request.user == project.admin or request.user in team.all():
            pass
        else:
            return HttpResponseRedirect('..')
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func