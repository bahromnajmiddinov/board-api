from django.db import models

from accounts.models import CustomUser


class Team(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='team_logos/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(CustomUser, related_name='teams', on_delete=models)
    members = models.ManyToManyField(CustomUser, related_name='team_memberships', through='TeamMembership')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.name} by {self.owner.username}'


class TeamMembership(models.Model):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('MEMBER', 'Member'),
        ('MANAGER', 'Manager'),
        ('LEAD', 'Lead'),
        ('VIP', 'VIP'),
        ('VIEWER', 'Viewer'),
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='MEMBER')
    joined_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username} - {self.team.name} - {self.role}'
    