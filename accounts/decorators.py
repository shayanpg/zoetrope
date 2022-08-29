import functools
from django.shortcuts import redirect
from django.contrib import messages

def require_api_calls_remaining(view_func, redirect_url="calls_depleted"):
    """
        this decorator restricts users from accessing the view function
        who have run out of their allotment of API calls.
    """
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.api_calls_remaining > 0:
            return view_func(request, *args, **kwargs)
        return redirect(redirect_url)  
    return wrapper