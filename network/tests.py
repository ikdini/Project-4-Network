from django.db.models import Max
from django.test import TestCase, Client

from .models import *

# Create your tests here.
class PostTestCase(TestCase):
  def setUp(self):

    # Create users
    user1 = User.objects.create_user(username="test1", password="test1", email="test1@example.com")
    user2 = User.objects.create_user(username="test2", password="test2", email="test2@example.com")

    # Create posts
    Post.objects.create(content="test2", poster=user1)
    Post.objects.create(content="test3", poster=user2)
    Post.objects.create(content="", poster=user1)
    Post.objects.create(content="", poster=user2)
    Post.objects.create(content="test10")


  def test_post_creation(self):
    """Test post creation"""
    user1 = User.objects.get(username="test1")
    post1 = Post.objects.get(content="test2", poster=user1)
    self.assertEqual(post1.content, "test2")
    self.assertEqual(post1.poster, user1)

  def test_post_count1(self):
    """Test user post count"""
    a = User.objects.get(username="test1")
    b = User.objects.get(username="test2")
    self.assertEqual(a.my_post.count(), 2)
    self.assertEqual(Post.objects.filter(poster=b).count(), 2)
    self.assertEqual(Post.objects.filter(poster=None).count(), 1)
    self.assertEqual(Post.objects.count(), 5)

  def test_valid_post(self):
    """Test Valid Post"""
    user1 = User.objects.get(username="test1")
    user2 = User.objects.get(username="test2")
    post1 = Post.objects.get(content="test2", poster=user1)
    post2 = Post.objects.get(content="", poster=user2)
    post3 = Post.objects.get(content="test10")
    self.assertTrue(post1.is_valid_post())
    self.assertFalse(post2.is_valid_post())
    self.assertFalse(post3.is_valid_post())

  def test_post_likes(self):
    """Test Post Likes Count"""
    user1 = User.objects.get(username="test1")
    user2 = User.objects.get(username="test2")
    post1 = Post.objects.get(content="test2", poster=user1)
    self.assertEqual(post1.likes.count(), 0)
    post1.likes.add(user1)
    self.assertEqual(post1.likes.count(), 1)
    post1.likes.remove(user1)
    self.assertEqual(post1.likes.count(), 0)
    post1.likes.add(user2)
    self.assertEqual(post1.likes.count(), 1)
    post1.likes.remove(user2)
    self.assertEqual(post1.likes.count(), 0)
    post1.likes.add(user1)
    self.assertEqual(post1.likes.count(), 1)
    post1.likes.add(user2)
    self.assertEqual(post1.likes.count(), 2)
    self.assertEqual(user1.liked.count(), 1)

  def test_follow(self):
    """Test Follow Count"""
    user1 = User.objects.get(username="test1")
    user2 = User.objects.get(username="test2")
    post1 = Post.objects.get(content="test2", poster=user1)
    
    self.assertEqual(user1.follower.count(), 0)
    user1.follower.add(user1)
    self.assertEqual(user1.follower.count(), 1)
    user1.follower.remove(user1)
    self.assertEqual(user1.follower.count(), 0)
    user1.follower.add(user2)
    self.assertEqual(user1.follower.count(), 1)
    user1.follower.remove(user2)
    self.assertEqual(user1.follower.count(), 0)
    user1.follower.add(user1)
    self.assertEqual(user1.follower.count(), 1)
    user1.follower.add(user2)
    self.assertEqual(user1.follower.count(), 2)
    self.assertEqual(post1.poster.follower.count(), 2)
    
  def test_index(self):
    """Test Index Page"""
    c = Client()
    response = c.get("/")
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.context["page_obj"].number, 1)
    self.assertEqual(response.context["posts"].count(), 5)
    self.assertTemplateUsed(response, "network/index.html")
    self.assertContains(response, "test1")
    self.assertContains(response, "test2")
    self.assertContains(response, "test10")
    self.assertContains(response, "test3")

  def test_valid_profile_page(self):
    """Test Valid Profile Page"""
    user1 = User.objects.get(username="test1")

    c = Client()
    response = c.get(f"/profile/{user1.username}")
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.context["page_obj"].number, 1)
    self.assertEqual(response.context["posts"].count(), 2)

  def test_following_page(self):
    """Test Following Page"""
    user1 = User.objects.get(username="test1")
    user2 = User.objects.get(username="test2")
    user1.following.add(user2)

    c = Client()
    c.login(username='test1', password='test1')
    response = c.get("/following")
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.context["posts"].count(), 2)
    self.assertContains(response, "logout")