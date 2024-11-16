from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Users , Blogs
import bcrypt

def index(request):
    return render (request, "home.html")

def allblogs(request):
    user = Users.objects.get(id = request.session['loggedInUser'])
    blogs = Blogs.objects.all()
    isThereCat = False
    context = {
        'user': user,
        'blogs': blogs,
        'isThereCat': isThereCat
    }
    return render (request, "allblogs.html", context)

def allcat(request, cat):
    user = Users.objects.get(id = request.session['loggedInUser'])
    blogs =  Blogs.objects.filter(cat = cat)
    cat = cat
    isThereCat = True
    context = {
        'user': user,
        'blogs': blogs,
        'isThereCat': isThereCat,
        'cat': cat
    }
    return render (request, "allblogs.html", context)

def register(request):
    if request.method=='GET':
        return render(request,"register.html")
    if request.method=="POST":
        errors=Users.objects.reg_validator(request.POST)
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/blogs')
        else:
            fname=request.POST['fn']
            lname=request.POST['ln']
            email = request.POST['email']
            pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            newUsers= Users.objects.create(fname=fname,lname=lname,email=email,password=pw_hash)
            newUsers.save()
            request.session['loggedInUser']=newUsers.id
            return redirect('/blogs')

def login(request):
    if request.method == "GET":
        return render (request, "login.html")
    if request.method == "POST":
        errors= Users.objects.login_validator(request.POST)
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect ('/login')
        else:
            user = Users.objects.get(email = request.POST['email'])
            request.session['loggedInUser'] = user.id
            return redirect("/blogs")

def logout(request):
    del request.session['loggedInUser']
    return redirect('/')

def create_blog(request):
    if request.method == "GET":
        return render (request, "addblog.html")
    if request.method == "POST":
        errors=Blogs.objects.validator(request.POST)
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/blogs/create')
        else:
            user = Users.objects.get(id = request.session['loggedInUser'])
            title = request.POST['title']
            content = request.POST['content']
            pic = request.POST['pic']
            cat = request.POST['cats']
            newBlog = Blogs.objects.create(title = title, content = content, pic = pic, uploaded_by = user, cat = cat)
            newBlog.save()
            return redirect ("/blogs")

def blog_dis(request, id):
    blog = Blogs.objects.get(id = id)
    user = Users.objects.get(id=request.session['loggedInUser'])
    context = {
        'blog': blog,
        'user': user,
    }
    return render(request, "show.html", context)

def del_blog(request, id):
    blog = Blogs.objects.get(id = id)
    upload_user = blog.uploaded_by.id
    logged_user = Users.objects.get(id = request.session['loggedInUser']).id
    if upload_user == logged_user:
        blog.delete()
    return redirect ('/blogs')

def add_likes(request,blog_id):
    if not 'loggedInUser' in request.session:
        return redirect('/')
    like=Blogs.objects.get(id=blog_id)
    user=Users.objects.get(id=request.session['loggedInUser'])
    user.user_liked.add(like)
    user.save()
    return redirect('/blogs')
    