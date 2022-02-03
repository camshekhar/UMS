from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required 
from django.contrib import messages
from django.contrib.auth.models import User
from home.models import UserDetail

# Registering Users Here.
def signup(request):
    
    if request.user.is_authenticated:
        return redirect('home')
    
    else:
        if request.method == 'POST':
            username = request.POST['uname']
            fname = request.POST['fname']
            lname = request.POST['lname']
            email = request.POST['email']
            gender = request.POST['gender']
            phone = request.POST['phone']
            pass1 = request.POST['pass1']
            pass2 = request.POST['pass2']
            
            # Validations for registration
            if User.objects.filter(username=username):
                messages.error(request, 'Username already exists, username should be unique!')
                return redirect('signup')
                        
            if User.objects.filter(email=email):
                messages.error(request, 'Email Already Registered!')   
                return redirect('signup') 
                
            if len(username) > 10:
                messages.error(request, 'Username should be less than 10 characters')
                return redirect('signup') 
                    
                    
            if pass1 != pass2:
                messages.error(request, "Confirm Password didn't matched!")
                return redirect('signup') 
                
            
            if not username.isalnum():
                messages.error(request, 'Username must be Alpha-Numeric!')
                return redirect('signup') 
            
            myuser = User.objects.create_user(username, email, pass1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()
            username2 = User.objects.get(username=username)
            user_detail = UserDetail(uname=username2, email=email, fname=fname, lname=lname, gender=gender, phone=phone, password=pass1)
            myuser.save()
            user_detail.save()
            messages.success(request, 'Successfully Registered!, Login using your Credentials.')
            return redirect('signin')
    return render(request, 'register.html')

# User Login Here.
def signin(request):
    
    if request.user.is_authenticated:
        return redirect('home')
    
    else:
        if request.method == 'POST':
            username = request.POST['username']
            pass1 = request.POST['pass']
            user = authenticate(request, username=username, password=pass1)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login Successful')
                return redirect('home')
                    
            else:
                messages.error(request, 'Invalid Credentials!') 
    return render(request, 'login.html')

# User Details Management Here.
@login_required(login_url='signin')
def home(request):
    users_detail = UserDetail.objects.all()
    return render(request, 'index.html', {'users_detail': users_detail})
    
# User Logout Here.
@login_required(login_url='signin')
def signout(request):
    logout(request)
    messages.success(request, 'Successfully Logged Out!')
    request.session.flush() # Will Clear the Current active Session.
    return redirect('signin')

# Deleting Other User.
@login_required(login_url='signin')
def delete_other(request, email):
    
    user = User.objects.get(email=email)
    user.delete()
    messages.success(request, 'Deleted Successfully!')
    return redirect('home')

# Deleting Logged In User.
@login_required(login_url='signin')
def delete_own(request, username):
    user = User.objects.get(username=username)
    logout(request)
    request.session.flush() # Will Clear the Current active Session.
    user.delete()
    messages.success(request, 'Logged Out and Deleted Successfully!')
    return redirect('signin')
    
# User Details Editing Here.
@login_required(login_url='signin')
def edit(request, email):
    user_details = UserDetail.objects.get(email=email)
    return render(request, 'edit.html', {'ud':user_details})

# User details Updating Here.
@login_required(login_url='signin')
def update(request, email):
    user_details = UserDetail.objects.get(email=email)
    myuser = User.objects.get(email=email)
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        gender = request.POST['gender']
        phone = request.POST['phone']
        
        myuser.email = email
        myuser.first_name = fname
        myuser.last_name = lname
        
        myuser.save()
        
        user_details.fname = fname
        user_details.lname = lname
        user_details.email = email
        user_details.phone = phone
        user_details.gender = gender
        
        user_details.save()
        messages.success(request, 'Successfully Updated!')
        return redirect('home')
    return HttpResponse('404 - Requested Page Not Found!')

# Changing User password Here.
def password_change(request):
    
    if request.method == 'POST':
        new_pass = request.POST['new_pass']
        conf_pass = request.POST['conf_pass']
        conf_email = request.POST['conf_email']
        
        if new_pass != conf_pass:
            messages.error(request, "Confirm Password didn't matched!")
            return redirect('password_change')
        
        user = User.objects.get(email=conf_email)
        user_detail = UserDetail.objects.get(email=conf_email)
        user.set_password(new_pass)
        user.save()
        user_detail.password = new_pass
        user_detail.save()
        messages.success(request, 'Password Changed Successfully.')
        return redirect('signin')
    return render(request, 'pass_change.html') 
    
    
    
    