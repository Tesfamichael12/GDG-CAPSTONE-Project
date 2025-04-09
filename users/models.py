from django.db import models
from django.contrib.auth.models import User

from django.core.validators import RegexValidator

""" Model for User Profile """

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    following = models.ManyToManyField(User, related_name="following", blank=True)
    friends = models.ManyToManyField(User, related_name='my_friends', blank=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(default="", null=True, max_length=500, blank=True)
    date_of_birth = models.CharField(blank=True,max_length=150)
    updated = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True, null=True)


    def profile_posts(self):
        return self.user.post_set.all()

    def get_friends(self):
        return self.friends.all()

    def get_friends_no(self):
        return self.friends.all().count()

    def __str__(self):
        return f'{self.user.username} Profile'



STATUS_CHOICES = (
    ('send','send'),
    ('accepted','accepted')
)

class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friend_sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friend_receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"