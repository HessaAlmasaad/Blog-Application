from distutils.log import error
from pyexpat import model
from django.db import models
import bcrypt
import re

class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['emailExist'] = "Invalid email address!"
        elif len(postData['password']) < 8:
            errors['password'] = "password should be at least 8 characters"
        elif postData['password'] != postData['cPassword']:
            errors['cPassword'] = "password is not equal to the confirm password"
        elif len(postData['fn']) < 2:
            errors['fn'] = "name should be at least 2 characrters long"
        elif len(postData['ln']) < 2:
            errors['ln'] = "name should be at least 2 characrters long"
        return errors

    def login_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invali
        user = Users.objects.filter(email=postData['email'])
        if len(user) == 0:
            errors['email_e'] = "Email or Password is not correct"

        elif (user[0].email != postData['email']):
            errors['email_n'] = "Email or Password is not correct"

        elif not bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
            errors['password'] = "Email or Password is not correct"
        return errors
    
class BlogManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['content']) < 5:
            errors['content'] = "You have to write somting in the content field to share it!"  
        elif len(postData['title'])==0:
            errors['title']=" title is required"
        return errors

class Users(models.Model):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Blogs(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    pic = models.TextField()
    cat = models.CharField(max_length=255, default="all")
    uploaded_by = models.ForeignKey(Users, related_name="user_upload", on_delete=models.CASCADE)
    user_liked = models.ManyToManyField(Users, related_name="liked_blogs")
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    objects = BlogManager()


