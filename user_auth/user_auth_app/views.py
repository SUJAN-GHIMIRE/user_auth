from django.shortcuts import render
#imports for registration 
from user_auth_app.forms import UserForm,UserProfileInfoForm

#imports for login
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect ,HttpResponse
from django.urls import reverse


# Create your views here.

def index(request):
    return render(request,'index.html')

def user_auth_index(request):
    return render(request,'user_auth_app/user_auth_index.html')


@login_required
def special(request):
    return HttpResponse("you are logged in ,Nice!") 

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))



# user registration
def registration(request):
    registered = False
   

    if request.method == "POST":          #this is activated when we click submit by giving info 
        user_form = UserForm(data = request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()              #saves user directly to db
            user.set_password(user.password)        #hassing the pasword
            user.save()                           #saving password in db

            profile = profile_form.save(commit = False)
            profile.user = user                      #gives one to one relation
            
            if "profile_pic" in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    
    else:                             #this runs and creates instances when page is loaded 
        user_form =UserForm()
        profile_form =UserProfileInfoForm()

    


    # this return works 1st to display form without any values of its key when else executes
    # in second time after form is filled and users gives value ani clicks submit its value are filled after 
    # validation and its loads the index paf=ge with thank ypu for registering
    return render(request,'user_auth_app/registration.html',
                                    {'user_form':user_form,
                                     'profile_form':profile_form,
                                     'registered':registered})


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        #django build in authentication
        user = authenticate(username =username ,password = password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('user_auth_app:user_auth_index'))
                # if view name is passed the a colon is used
               
            
            else:
                return HttpResponse("Account Not Active")
        
        else:
            print("some one tried to login and failed")
            print(f"username :{username} and password : {password}")
            return HttpResponse("invalid login supplied!")
    else:
        return render(request, 'user_auth_app/user_login.html',{})

    # return render(request,'user_auth_app/user_login.html')
