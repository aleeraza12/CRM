from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args,**kwargs):
        if request.user.is_authenticated:
            return redirect('customer_order')
        else:
            return view_func(request, *args,**kwargs)
    return wrapper_func


def allowed_user(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args,**kwargs)
            else:
                return HttpResponse("You ara not allowed to do that")
        return wrapper_func
    return decorator


def admin_only(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group == 'customer':
                return redirect('user_profile')
            if group == 'admin':
                return view_func(request, *args,**kwargs)
            else:
                return HttpResponse("You ara not allowed to do that")
        return wrapper_func
