from django.shortcuts import redirect

def custom_login_required_hr(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login-hr/')  # Redirect to your login URL
        return view_func(request, *args, **kwargs)
    return wrapper

def custom_login_required_candidate(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login-Candidate/')  # Redirect to your login URL
        return view_func(request, *args, **kwargs)
    return wrapper

