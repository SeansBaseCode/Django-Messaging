from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from app.forms import *
from app.models import *

def sign_in(request):
    context = {}
    if request.method == "POST":
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('name')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                context['signup_success'] = True
                return redirect('message_board')  
            else:
                context["error"] = "Invalid credentials"
    else:
        form = SignInForm()

    context["form"] = form
    return render(request, "login.html", context)

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            
            if User.objects.filter(name=name).exists():
                form.add_error('name', 'A user with this name already exists.')
            elif User.objects.filter(email=email).exists():
                form.add_error('email', 'A user with this email already exists.')
            else:
                form.save()
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
            message.save() 
            form.save()
            return redirect('message_board')
    else:
        form = MessageForm()

    messages = Message.objects.all()

    return render(request, 'message_board.html', {'form': form, 'messages': messages})



def admin_access(request):
    pass
def delete_all_messages(request):
    if request.method == 'POST':
        Message.objects.all().delete()
        return HttpResponse("All messages have been deleted successfully.")
    return HttpResponse("Invalid request method.", status=400)

def delete_message_by_id(request, message_id):
    if request.method == 'POST':
        message = get_object_or_404(Message, id=message_id)
        message.delete()
        return HttpResponse(f"The message has been deleted successfully.")
    return HttpResponse("Invalid request method.", status=400)