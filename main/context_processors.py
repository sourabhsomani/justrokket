from .forms import SignupForm
from .forms import LoginForm


def login_form(request):
    return {
        'login_form': LoginForm(),
        'signup_form': SignupForm(),
    }

def username(request):
    if request.user.is_authenticated:
        a = str(request.user.username)
        return {'username': a.split('@')[0]}
    else:
        return {}
