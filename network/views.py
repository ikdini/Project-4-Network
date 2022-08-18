import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from .models import *


def index(request):
  # This is creating a paginator object with 10 posts per page.
  posts = Post.objects.all().order_by('-id')
  paginator = Paginator(posts, 10)

  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  return render(request, "network/index.html", {
    "page_obj": page_obj,
    "posts": posts
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
  # This is creating a new post.
  if request.method == "POST":
    text = request.POST["newPost"].strip()
    poster = request.user

    new_post = Post(content=text, poster=poster)
    new_post.save()
  return HttpResponseRedirect(reverse("index"))

@csrf_exempt
def toggle_likes(request, post_id):
  # This is a function that is called when the user clicks on the like button. It checks if the user has
  # already liked the post, and if so, it removes the like. If not, it adds the like.
  if request.method == "POST":
    post = Post.objects.get(pk=post_id)
    
    if request.user in post.likes.all():
      post.likes.remove(request.user)
    else:
      post.likes.add(request.user)

    likenum = post.likes.count()
    return JsonResponse(likenum, safe=False)

@login_required(login_url="login")
def toggle_follow(request, poster):
  # This is a function that is called when the user clicks on the follow button. It checks if the user
  # has already followed the user, and if so, it removes the follow. If not, it adds the follow.
  if request.method == "POST":
    usr = User.objects.get(pk=poster)
    ussr = request.user
    if usr in ussr.following.all():
      ussr.following.remove(usr)
      usr.follower.remove(ussr)
    else:
      ussr.following.add(usr)
      usr.follower.add(ussr)

    poster = usr.username
  return HttpResponseRedirect(reverse("profile", kwargs={
  "poster": poster
  }))

def profile(request, poster):
  # This is a function that is called when the user clicks on the username. It gets the user's
  # profile and posts and displays them.
  Poster = User.objects.get(username=poster)
  posts = Post.objects.filter(poster__username=poster).order_by('-id')
  paginator = Paginator(posts, 10)

  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  return render(request, "network/profile.html", {
    'page_obj': page_obj,
    "poster": Poster,
    "posts": posts
  })

@login_required(login_url="login")
def following(request):
  # This is a function that is called when the user clicks on the following button. It gets the user's
  # following and posts and displays them.
  following = request.user.following.all()
  posts = Post.objects.filter(poster__in=following).order_by('-id')
  paginator = Paginator(posts, 10)

  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  return render(request, "network/following.html", {
    'page_obj': page_obj,
    "posts": posts
  })

@csrf_exempt
def edit_post(request, post_id):
  # This is a function that is called when the user clicks on the edit button. It gets the post's
  # content and saves it.
  if request.method == "POST":
    post = Post.objects.get(pk=post_id)

    data = json.loads(request.body)
    new_content = data.get("content", "")

    post.content = new_content
    post.edited = True
    post.save()
    return JsonResponse({"message": "Edited successfully."}, status=201)
