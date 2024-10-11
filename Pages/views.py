from django.shortcuts import render, redirect
import random
from django.core.mail import send_mail
from django.contrib import messages
from .models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Profile, Post
from django.contrib.auth import logout

OTP = None
EMAIL_USER = None
LNAME = None
FNAME = None

def home_page(request):
    return render(request, 'home_page.html')

def login_form(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home_page')
        else:
            messages.error(request, "Invalid email or password. Please try again.")
            return render(request, 'login_form.html', {'email': email})
    
    return render(request, 'login_form.html')

def generate_otp():
    return str(random.randint(1000, 9999))

def create_account(request):
    global OTP, EMAIL_USER , FNAME , LNAME
    if request.method == 'POST':
        FNAME = request.POST.get('fname')
        LNAME= request.POST.get('lname')
        EMAIL_USER = request.POST.get('email')  

        OTP = generate_otp()  
        send_mail(
            'Your TripGO OTP Code',
            f'Hey {FNAME} Welcome TripGO\nYour OTP code is {OTP}',
            'araut7798@gmail.com', 
            [EMAIL_USER],
            fail_silently=False,
        )
        return redirect('verify_otp')
    return render(request, 'create_account.html')

def verify_otp(request):
    global OTP  , EMAIL_USER
    if request.method == 'POST':
        otp_input = request.POST.get('otp')
        if OTP and OTP == otp_input:
            return redirect('create_password')  
        else:
            messages.error(request, "Incorrect OTP. Please enter the correct OTP.")
    return render(request, 'verify_otp.html' ,{"email" : EMAIL_USER})

def set_password(request):
    if request.method == 'POST':
        password = request.POST.get('create_pass')
        confirm_password = request.POST.get('confirm_pass')

        global EMAIL_USER ,LNAME , FNAME
        if password == confirm_password:
           
           user = User(first_name = FNAME , last_name = LNAME , email = EMAIL_USER , password = password)
           user.save()
           return redirect('success_page')
        else:
            messages.error(request, "Passwords do not match.")
    return redirect('create_password')

def success_page(request):
    return render(request, 'success_page.html')


F_EMAIL = None
F_OTP = None

def forget_pass(request):
    global F_EMAIL, F_OTP
    if request.method == "POST":
        F_EMAIL = request.POST.get('email')
        user = User.objects.filter(email=F_EMAIL).first()
        if user:
            F_OTP = random.randint(1000, 9999)
            send_mail(
                'Your OTP for Password Reset',
                f'Your OTP is {F_OTP}',
                'araut7798@gmail.com',
                [F_EMAIL],
                fail_silently=False,
            )
            return redirect('verify_email')
        else:
            return render(request, 'forget_password.html', {'error': 'Email not found.'})
    return render(request, 'forget_password.html')

def forget_password_otp(request):
    global F_OTP
    if request.method == "POST":
        entered_otp = request.POST.get('f_otp')
        otp = F_OTP
        if otp == entered_otp:
            return redirect('reset_password')
        else:
            return render(request, 'forget_otp.html', {'error': 'Invalid OTP'})
    return render(request, 'forget_otp.html')


def reset_password(request):
    global F_EMAIL
    if request.method == "POST":
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = F_EMAIL

        if password == confirm_password:
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            return render(request, 'login.html', {'message': 'Password reset successful.'})
        else:
            return render(request, 'reset_password.html', {'error': 'Passwords do not match.'})
    return render(request, 'reset_password.html')

def logout_view(request):
    logout(request)
    return redirect('login_page')

@login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user)
    posts = Post.objects.filter(user=request.user)

    if request.method == 'POST':
        if 'profile_update' in request.POST:
            profile.name = request.POST.get('name')
            profile.location = request.POST.get('location')
            profile.bio = request.POST.get('bio')

            if 'image' in request.FILES:
                profile.profile_image = request.FILES['image']
            profile.save()
            return redirect('profile')

        elif 'post_form' in request.POST:
            city = request.POST.get('post_city')
            location = request.POST.get('post_location')
            description = request.POST.get('post_description')

            post_image = request.FILES['post_image']
            Post.objects.create(
                user=request.user, city=city, location=location,
                description=description, post_image=post_image
            )
            return redirect('profile')

    return render(request, 'profile_page.html', {'profile': profile, 'posts': posts})


