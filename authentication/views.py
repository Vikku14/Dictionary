from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import SignupForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.models import User



# Create your views here.
def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                if 'next' in request.GET:
                    return HttpResponseRedirect(request.GET['next'])
                else:
                    messages.success(request, "You are successfully Logged In.")
                    return HttpResponseRedirect(reverse('core:home'))
            else:
                messages.error(request, "Your account is Deactivated")
                return HttpResponseRedirect(reverse('authentication:signin'))
        else:
            messages.error(request, 'Invalid Username or Password')
            return HttpResponseRedirect(reverse("authentication:signin"))
    else:
        return render(request, 'authentication/signin.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, 'Your account were successfully created and successfully logged In.')
            return HttpResponseRedirect('/home')
        else:
            messages.error(request, 'There was some problems while creating your account. Please review some fields before submiting again.')
        return render(request, 'authentication/signup.html', { 'form': form })
    else:
        return render(request, 'authentication/signup.html', {'form': SignupForm()})


def signout(request):
    logout(request)
    return HttpResponseRedirect(reverse('core:web'))
