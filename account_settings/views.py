from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import  UserForm, ProfileForm, ProfilePhotoForm
from django.db import transaction
from django.contrib import messages
from .models import ProfilePhoto
# Create your views here.


@login_required()
def settings(request):
    return redirect('account_settings:profile')

@login_required()
@transaction.atomic
def profile(request):
    if request.method == 'POST':

        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Your profile was successfully updated!')
            return redirect('account_settings:profile')
        else:
            messages.error(request, 'Please correct the error below.')
            return render(request, 'account_settings/profile.html', { 'user_form': user_form ,'profile_form': profile_form })


    else:
        user_form = UserForm(instance = request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        context = {'user_form': user_form,
                    'profile_form': profile_form,
                    }
        return render(request, 'account_settings/profile.html',context)

@login_required()
@transaction.atomic
def picture(request):
    if request.method == 'POST':
        try:
            form = ProfilePhotoForm(request.POST, request.FILES, instance=request.user.profilephoto )
            if form.is_valid():
                form.save()
                messages.success(request,'Your profile Picture successfully updated!')
                return redirect('account_settings:picture')
            else:
                messages.error(request, 'Please correct the error below.')
                return render(request, 'account_settings/picture.html', { 'form': form })
        except Exception as e:
            messages.error(request, 'Enexpected Error.'+str(e))
            return render(request, 'account_settings/picture.html', { 'form':ProfilePhotoForm() })


    else:
        form = ProfilePhotoForm()
        p = ProfilePhoto.objects.get(user__id=request.user.id)
    return render(request, 'account_settings/picture.html',{'form':form, 'p':p})
