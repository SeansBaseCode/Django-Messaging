from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from app.forms import *
from app.models import *
from django.contrib.auth.models import User

def sign_in(request):
    context = {}
    if request.method == "POST": 
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            logout(request)
            login(request, user)
            context['signup_success'] = True
            if user.is_superuser:
                return redirect('access')
            else:
                return redirect('messages')  
        else:
            context["error"] = "Invalid credentials"
    else:
        form = SignInForm()

    return render(request, "login.html", context)

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            if User.objects.filter(username=name).exists():
                form.add_error('name', 'A user with this name already exists.')
            elif User.objects.filter(email=email).exists():
                form.add_error('email', 'A user with this email already exists.')
            else:
                User.objects.create_user(username=name,
                                         password=password,
                                         email=email)
                return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def message_board(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            print(message.user)
            message.save() 
            return redirect('messages')
    else:
        form = MessageForm()

    messages = Message.objects.all()

    return render(request, 'message_board.html', {'form': form, 'messages': messages})

@login_required
def delete(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if message.user != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to delete this message.")
    message.delete()
    if request.user.is_superuser:
        return redirect('access')
    else:
        return redirect('messages')

@user_passes_test(lambda u: u.is_superuser, login_url='messages')
def admin_access(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            print(message.user)
            message.save() 
            return redirect('access')
    else:
        form = MessageForm()
    messages = Message.objects.all()
    return render(request, 'admin.html', {'form': form, 'messages': messages})
def delete_all_messages(request):
    if request.method == 'POST':
        Message.objects.all().delete()
        return redirect('access')
    return redirect('access')

