from django.shortcuts import render,redirect,HttpResponseRedirect
from django.conf import settings
from .forms import SignUpForm, LoginForm, BlogForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Blog
from django.contrib.auth.models import Group
from .models import Contact 
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)


# Create your views here.
def home(request):
    blogs = Blog.objects.all()
    return render(request,'blog/home.html',{'blogs':blogs})

def user_signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request,"CONGRATULATION, You are Registered!")
            user = form.save()
            group = Group.objects.get(name = 'Author')
            user.groups.add(group)
    else:
        form=SignUpForm()
    return render(request,'blog/signup.html',{'form':form})

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request = request, data = request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                pwd = form.cleaned_data['password']
                user = authenticate(username=uname, password=pwd)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = LoginForm()
        return render(request, 'blog/login.html', {'form':form})
    else:
        return HttpResponseRedirect('/dashboard/')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def dashboard(request):
    if request.user.is_authenticated:
        blogs = Blog.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        return render(request, 'blog/dashboard.html',{'blogs':blogs,'full_name':full_name,'groups':gps})

def add_blog(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = BlogForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                cont = form.cleaned_data['cont']
                blg = Blog(title=title, cont = cont)
                blg.save()
                form = BlogForm()
        else:
            form = BlogForm()
        return render(request, 'blog/addblog.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')

def update_blog(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Blog.objects.get(pk=id)
            form = BlogForm(request.POST,instance = pi)
            if form.is_valid():
                form.save()
        else:
            pi = Blog.objects.get(pk=id)
            form = BlogForm(instance=pi)
        return render(request, 'blog/updateblog.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')

def delete_blog(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Blog.objects.get(pk=id)
            pi.delete()
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')

def about(request):
    return render(request, 'blog/about.html')

def contact(request):
    if request.method == "POST":
        name1 = request.POST.get('name')
        email1 = request.POST.get('email')
        message1 = request.POST.get('message')

        logger.debug(f"Received POST data: name={name1}, email={email1}, message={message1}")

        if len(name1) > 4:
            contact = Contact(name=name1, email=email1, message=message1)
            contact.save()
            logger.debug("Contact saved successfully")
            messages.success(request, 'Successfully Form Submitted')
            return redirect('contact')
        else:
            logger.debug("Validation error: name too short")
            messages.error(request, 'First Name Should Be More Than 4 Characters')
            return redirect('contact')

    return render(request, 'blog/contact.html')