from django.db import models
from django.contrib.auth.models import AbstractUser

from datetime import timedelta

# from boards.models import Board


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    billing_cycle = models.CharField(max_length=10, choices=[('monthly', 'Monthly'), ('yearly', 'Yearly')], default='monthly')
    max_users = models.PositiveIntegerField(null=True, blank=True)  # Limit on the number of users if applicable
    max_teams = models.PositiveIntegerField(null=True, blank=True)  # Limit on the number of teams if applicable
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.price} {self.billing_cycle})"


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    industry = models.ForeignKey('Industry', on_delete=models.SET_NULL, null=True, related_name='users')
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True, related_name='users')
    
    def __str__(self):
        return self.username
    
    def get_avatar(self):
        if self.avatar:
            return self.avatar.url
        return 'default_avatar.jpg'


class UserSubscription(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='subscription')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, related_name='subscriptions')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"

    def renew(self):
        # Logic to renew the subscription
        if self.plan.billing_cycle == 'monthly':
            self.end_date += timedelta(days=30)
        elif self.plan.billing_cycle == 'yearly':
            self.end_date += timedelta(days=365)
        self.save()

    def cancel(self):
        self.active = False
        self.save()


class StarredBoard(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='starred_boards')
    board = models.ForeignKey('boards.Board', on_delete=models.CASCADE, related_name='starred_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.board.title}"


class Industry(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    