from django.db import models

from uuid import uuid4

from accounts.models import CustomUser
from teams.models import Team


class Project(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='projects')
    boards = models.ManyToManyField('Board', related_name='projects')

class Board(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=100)
    is_public = models.BooleanField(default=False)
    participants = models.ManyToManyField(CustomUser, related_name='boards')
    
    # Timestamps
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at', 'updated_at']),
            models.Index(fields=['title', 'is_public']),
            models.Index(fields=['created_by']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
        ]
    
    def __str__(self):
        return f'{self.title} by {self.created_by.username}'
    

class BoardSettings(models.Model):
    board = models.OneToOneField(Board, related_name='settings', on_delete=models.CASCADE)
    
    # Board settings
    grid_size = models.PositiveIntegerField(default=10)
    zoom_level = models.PositiveIntegerField(default=1)
    background_color = models.CharField(max_length=7, default='#FFFFFF') 


class BoardElement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    board = models.ForeignKey(Board, related_name='elements', on_delete=models.CASCADE)
    element_type = models.CharField(max_length=50)  # e.g., 'rectangle', 'circle', 'text'
    content = models.TextField(null=True, blank=True)  # Content like text or image URL
    team = models.ForeignKey(Team, related_name='boards', on_delete=models.CASCADE, null=True, blank=True)
    
    # Position fields
    x_position = models.FloatField()  # X coordinate
    y_position = models.FloatField()  # Y coordinate
    
    # Size and other attributes
    width = models.FloatField()
    height = models.FloatField()
    rotation = models.FloatField(default=0.0)  # Rotation in degrees

    # Timestamps
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='board_elements')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.element_type} on {self.board.name} at ({self.x_position}, {self.y_position})'


class Comment(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='comments')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    color = models.CharField(max_length=7, default='#000000')
    muted = models.ManyToManyField(CustomUser, related_name='muted_comments')
    resolve = models.BooleanField(default=False)
    pin = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.owner.username}: {self.content[:50]}...'
    
