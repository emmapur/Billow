from django.http import HttpResponse
from django.shortcuts import redirect 


def users_allowed(allowed_roles=[]):
    def decorator(view_function):
        def wrapper_function(request, *args, **kwargs):

            #group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                print(group)
            if group in allowed_roles:
                return view_function(request, *args, **kwargs)
            else: 
                return HttpResponse("You are not authorised to view this page")
        return wrapper_function
    return decorator