
from django.urls import path

from . import views

urlpatterns = [
  path("", views.index, name="index"),
  path("login", views.login_view, name="login"),
  path("logout", views.logout_view, name="logout"),
  path("register", views.register, name="register"),
  path("following", views.following, name="following"),
  path("create_post", views.create_post, name="create_post"),
  path("likes/<int:post_id>/", views.toggle_likes, name="toggle_likes"),
  path("follow/<int:poster>/", views.toggle_follow, name="toggle_follow"),
  path("profile/<str:poster>/", views.profile, name="profile"),

  # API Routes
  path("edit_post/<int:post_id>", views.edit_post, name="edit_post"),
]
