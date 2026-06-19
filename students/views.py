from django.shortcuts import render, redirect
from .models import students
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/login/')

def home(request):
    if request.method == "POST":

        name = request.POST.get("name")
        age = request.POST.get("age")
        course = request.POST.get("course")

        students.objects.create(
            name=name,
            age=age,
            course=course
        )

        return redirect('/')
    
    search = request.GET.get("search")
    
    if search:
        all_students = students.objects.filter(
            name__icontains = search
        )
    else:
        all_students = students.objects.all()

    

    return render(request, "home.html",{
        "students": all_students
    })

def delete_student(request, id):
    
    student = students.objects.get(id=id)

    student.delete()

    return redirect('/')

def edit_student(request, id):
     
     student = students.objects.get(id=id)

     if request.method == "POST":
         
         student.name = request.POST.get("name")
         student.age = request.POST.get("age")
         student.course = request.POST.get("course")

         student.save()

         return redirect('/')

     return render(request, "edit.html",{
         "student":student
     })


def register_page(request):
    if request.method =='POST':

        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            
            return render(request, 'register.html',{
                "error" : "Username already Exists!"
            })

        User.objects.create_user(
            username=username,
            password=password
        )

        return redirect('/')
    
    return render (request, "register.html")

def login_page(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            return redirect('/')
        
    return render(request, 'login.html')

def logout_page(request):
    
    logout(request)

    return redirect('/login/')