from django.db import models
from accounts.models import User


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='_following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='_followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"

    def clean(self):
        if self.follower == self.following:
            raise ValidationError("Users can not follow themselves.")