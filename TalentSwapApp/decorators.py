from django.http import HttpResponseForbidden

def employee_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if not hasattr(request.user, 'employee'):
            return HttpResponseForbidden("You are not authorized to view this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func

def company_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if not hasattr(request.user, 'company'):
            return HttpResponseForbidden("You are not authorized to view this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func