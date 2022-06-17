from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import *


def index(request):
  posts = Post.objects.all()
  return render(request, "network/index.html", {
    "posts": posts.order_by('-id'),
  })


def login_view(request):
  if request.method == "POST":

    # Attempt to sign user in
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)

    # Check if authentication successful
    if user is not None:
      login(request, user)
      return HttpResponseRedirect(reverse("index"))
    else:
      return render(request, "network/login.html", {
        "message": "Invalid username and/or password."
      })
  else:
    return render(request, "network/login.html")


def logout_view(request):
  logout(request)
  return HttpResponseRedirect(reverse("index"))


def register(request):
  if request.method == "POST":
    username = request.POST["username"]
    email = request.POST["email"]

    # Ensure password matches confirmation
    password = request.POST["password"]
    confirmation = request.POST["confirmation"]
    if password != confirmation:
      return render(request, "network/register.html", {
        "message": "Passwords must match."
      })

    # Attempt to create new user
    try:
      user = User.objects.create_user(username, email, password)
      user.save()
    except IntegrityError:
      return render(request, "network/register.html", {
        "message": "Username already taken."
      })
    login(request, user)
    return HttpResponseRedirect(reverse("index"))
  else:
    return render(request, "network/register.html")

@login_required(login_url="login")
def create_post(request):
  if request.method == "POST":
    text = request.POST["newPost"]
    poster = request.user

    new_post = Post(content=text, poster=poster)
    new_post.save()
    return HttpResponseRedirect(reverse("index"))

def toggle_likes(request, post_id):
  if request.method == "POST":
    post = Post.objects.get(pk=post_id)
    
    if request.user in post.likes.all():
      post.likes.remove(request.user)
    else:
      post.likes.add(request.user)
  
  return HttpResponseRedirect(reverse("index"))

def profile(request, poster):
  posts = Post.objects.filter(poster__username=poster)
  return render(request, "network/profile.html", {
    "posts": posts.order_by('-id'),
    "poster": poster
  })