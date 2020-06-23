from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.

def web(request):
    try:
        if request.user.is_authenticated:
            return redirect("core:home")
        else:
            return render(request, 'core/web.html')
    except:
        return render(request, 'core/web.html')

@login_required()
def home(request):
    return render(request, 'core/home.html')
