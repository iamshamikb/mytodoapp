from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.forms import  UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import Todoform
from .models import ToDo
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'todo/home.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'todo/signup_page.html', {'form':UserCreationForm()})
    else:
        p1 = request.POST['password1']
        p2 = request.POST['password2']
        uname = request.POST['username']
        if p1 == p2:
            try:
                u = User.objects.create_user(uname, password=p1)
                u.save()
                login(request, u)
                return redirect('loggedinpage')
            except IntegrityError:
                return render(request, 'todo/signup_page.html', {'form':UserCreationForm(), 'error':'Username Taken!!'})
        else:
            return render(request, 'todo/signup_page.html', {'form':UserCreationForm(), 'error':'Passwords should match!!'})
            
def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/login_page.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/login_page.html', {'form':AuthenticationForm(),'error':'Wrong Credentials'})
        else:
            login(request, user)
            return redirect('loggedinpage')

@login_required
def loggedinpage(request):
    todos = ToDo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'todo/loggedinpage.html', {'todos':todos})

@login_required
def completedtodos(request):
    todos = ToDo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'todo/completedtodos.html', {'todos':todos})

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/create_todo.html', {'form':Todoform()})
    else:
        form = Todoform(request.POST)
        newform = form.save(commit=False)
        newform.user = request.user
        newform.save()
        return redirect('loggedinpage')

@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(ToDo, pk = todo_pk, user=request.user)
    if request.method =='GET':
        form = Todoform(instance=todo)
        return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form})
    else:
        form = Todoform(request.POST, instance=todo)
        form.save()

@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(ToDo, pk = todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('loggedinpage')

@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(ToDo, pk = todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('loggedinpage')