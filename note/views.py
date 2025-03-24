import base64
import secrets
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
import random
from note.utils import deleteotpreqs, sendEmailToClient, sendMailWithAttachment
from . models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from datetime import datetime, time, timedelta
from django.utils import timezone
from django.db.models import Q
import time
def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')

        user = User.objects.filter(username = username)

        if user.exists():
            messages.info(request, 'Username Already Exists')
            return redirect('/register/')

        user = User.objects.create(
            first_name = firstname,
            last_name = lastname,
            username = username,
            email = email
        )
        user.set_password(password)
        user.save()
        messages.info(request, 'Account Created Succesfully')

        return redirect('/login/')

    return render(request, 'register.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username = username).exists():
            messages.info(request,  "User Doesn't Exists")
            return redirect('/login/')
        user = authenticate(username = username, password = password)

        if user is None:
            messages.info(request, 'Invalid Credentials')
            return redirect('/login/')
        else:
            login(request, user)
            deleteotpreqs(user)
            return redirect('/home/')

    return render(request, 'login.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login/')
def upload(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if User.objects.filter(username=request.user.username).exists():
            post = User.objects.get(username=request.user.username)
        else:
            messages.info(request, "UserCredentials does not exist for this user.")
        images = request.FILES.getlist('photos')
        if not images:
            messages.info(request, "No Pictures Uploaded")
            return redirect('/gallery/')
        else:
            messages.info(request, 'Images Uploaded Succesfully')
            for img in images:
                multiple.objects.create(post=post, images=img, title = title)
            return redirect('/gallery/')
    
    return render(request, 'addphotoentry.html')

@login_required(login_url='/login/')
def home(request):
    return render(request, 'home.html', {'user' : request.user.username})

@login_required(login_url='/login/')
def logout_page(request):
    logout(request)
    return redirect('/login/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login/')
def showdairy(request):
    if request.method == 'GET':
        user = request.user
        dairies = UserCredentials.objects.filter(user = user)
        context = {'dairy': dairies}

        if request.GET.get('search'):
            search = request.GET.get('search')
            if search.isdigit():
                dairies = dairies.filter(
                    Q(created_at__year=search) |
                    Q(created_at__month=search) |
                    Q(created_at__day=search)
                )
            else:
                dairies = dairies.filter(
                    Q(descriptive__icontains=search) |
                    Q(title__icontains=search)
                )
            context = {'dairy' : dairies}


    return render(request, 'dairylist.html', context)


@login_required(login_url='/login/')
def descriptivedairy(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            #return render(request, 'addentry.html')
            return redirect('/adddairy/')
        if action == 'show':
            return redirect('/showdairy/')
    return render(request, 'descrptivediary.html')


@login_required(login_url='/login/')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adddairy(request):
    current_date = datetime.now().date().strftime('%B %d, %Y')
    if request.method == 'POST':
        title = request.POST.get('title')
        des = request.POST.get('description')
        user = request.user
        usercredentials = UserCredentials.objects.create(
            title = title,
            descriptive = des,
            user = user
        )
        usercredentials.save()
        messages.success(request, 'Your Magic Got Saved')


        #return render(request,'addentry.html', {'redirect' : True})
        return redirect('/showdairy/?new_entry=True')
    

    return render(request, 'addentry.html', {'current_date' : current_date})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login/')
def deletedairy(request, id):
    if request.GET.get('action') == 'delete':
        UserCredentials.objects.filter(id = id).delete()
        messages.info(request, 'Your Entry Got Deleted')
        return redirect('/showdairy/')
    return render(request, 'dairylist.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login/')
def editdairy(request, id):
    if request.GET.get('action') == 'edit':
        queryset = UserCredentials.objects.get(id = id)
        context = {'dairy': queryset}
        return render(request, 'updatedairy.html', context)
    
    return render(request, 'dairylist.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login/')
def updateddairy(request, id):
    if request.method == 'POST':
        queryset = UserCredentials.objects.get(id = id)
        title = request.POST.get('title')
        description = request.POST.get('description')
        queryset.title = title
        queryset.descriptive = description
        queryset.save()
        messages.info(request, 'Your Corrections Got Made Up Succesfully')
        return redirect('/showdairy/')
    return render(request, 'updatedairy.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login/')
def viewingpage(request, id):
    queryset = UserCredentials.objects.get(id = id)
    context = {'dairy': queryset}
    return render(request, 'view.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login/')
def photodiary(request):
    if request.method == 'POST':
        if request.POST.get('action') == 'add':
            return redirect('/upload/')
        if request.POST.get('action') == 'show':
            return redirect('/gallery/')
    return render(request, 'photodiary.html')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login/')
def showphotos(request):
    grouped_images = {}
    photos = multiple.objects.filter(post=request.user)

    for photo in photos:
        title = photo.title if photo.title else "Untitled"
        date = photo.date.strftime('%Y-%m-%d')
        
        if title not in grouped_images:
            grouped_images[title] = {}
        
        if date not in grouped_images[title]:
            grouped_images[title][date] = []
        
        grouped_images[title][date].append(photo)

    context = {'grouped_images': grouped_images}
    return render(request, 'gallery.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login/')
def updatephotos(request, title):
    if request.method == 'POST':
        if User.objects.filter(username=request.user.username).exists():
            post = User.objects.get(username=request.user.username)
        else:
            messages.info(request, "UserCredentials does not exist for this user.")
        images = request.FILES.getlist('photos')
        for img in images:
            multiple.objects.create(post=post, images=img, title=title)
        messages.info(request, 'Images Updated Succesfully')
        return redirect('/gallery/')
    
    return render(request, 'galleryedit.html', {'title' : title})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login/')
def deletephotos(request, id):
    if request.method == 'POST':
        multiple.objects.filter(id = id).delete()
        messages.info(request, 'Image Deleted Succesfully')
        return redirect('/gallery/')
    return render(request, 'gallery.html')

    


from django.views.decorators.cache import cache_control



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def checkMail(request):
    if 'otp' not in request.session:
        messages.error(request, "Please request an OTP first.")
        return redirect('/login/')
    
    
    if request.method == 'POST':
        check = request.POST.get('otp')
        otp = request.session.get('otp')
        expTime = request.session.get('exptime')
        otp_hashed = base64.b64decode(otp)

        if time.time() <= expTime and bcrypt.checkpw(str(check).encode('utf-8'), otp_hashed):
            del request.session['otp']
            del request.session['exptime']
            request.session['otp_verified'] = True
            otprecord = OTPRequest.objects.get(id=request.session.get('otpRecord'))
            if otprecord:
                otprecord.verified = True
                otprecord.save()
            return redirect('/passcheck/')
        else:
            if time.time() > expTime:
                messages.error(request, 'OTP time got expired')
            else:
                messages.error(request, 'Invalid OTP')
    

    return render(request, 'otpPage.html')


import bcrypt
from django.db import transaction

def otpViewPage(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            user = User.objects.filter(username=username).first()

            if not user:
                messages.error(request, 'Username Not Found')
                return redirect('/otpreq/')



            lastOtpReq = OTPRequest.objects.filter(user=user).order_by('-timestamp').first()
            if lastOtpReq:
                time_since_last_otp = timezone.now() - lastOtpReq.timestamp
                if time_since_last_otp.total_seconds() < 300 and lastOtpReq.verified != True:
                    messages.info(request, "OTP already sent. Please wait 5 minutes before requesting again. We'll redirect you shortly")
                    return render(request, 'otpRequestingPage.html', {
                        'wait_before_redirect': True,
                        'redirect_url': '/verify-otp/'  
                    })

           
            time_threshold = timezone.now() - timedelta(days=1)
            otpreqCount = OTPRequest.objects.filter(user=user, timestamp__gte=time_threshold).count()

            if otpreqCount >= 3:
                messages.error(request, "You've Exceeded Your Otp Limit (3 Times)")
                return redirect('/login/')

           
            otp = ''.join(str(secrets.randbelow(10)) for _ in range(6))
            email = user.email
            
            
            request.session['exptime'] = time.time() + 300
            
            
            try:
                
                sendEmailToClient(otp, email)  
                
                
                with transaction.atomic():  
                    otpreq = OTPRequest.objects.create(user=user)
                    request.session['otpRecord'] = otpreq.id

                
                otp_hashed = bcrypt.hashpw(str(otp).encode('utf-8'), bcrypt.gensalt())
                hashed_otp = base64.b64encode(otp_hashed).decode('utf-8')

                
                request.session['otp'] = hashed_otp
                request.session.set_expiry(300)
                request.session['user_data'] = user.id

                return redirect('/verify-otp/')

            except Exception as e:
                
                print(f"An error occurred: {e}")
                messages.error(request, 'An error occurred while processing your email check your internet connection. Please try again.')
                return redirect('/otpreq/')
                

    except Exception as e:
        
        print(f"An unexpected error occurred: {e}")
        messages.error(request, 'An unexpected error occurred. Please try again.')
        return redirect('/otpreq/')  

   
    return render(request, 'otpRequestingPage.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def passCheck(request):
    if not request.session.get('otp_verified', False):
        messages.error(request, 'OTP must be verified before getting in to this..')
        return redirect('/login/')
    elif request.method == 'POST':
        password = request.POST.get('password')
        user = User.objects.get(id=request.session.get('user_data'))
        user.set_password(password)
        user.save()
        messages.info(request, 'Password Changed Succesfull')
        del request.session['otp_verified']
        return redirect('/login/')
    return render(request, 'paasCheck.html')

