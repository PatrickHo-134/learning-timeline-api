from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils import timezone

# class User(AbstractUser):
#     id = models.AutoField(primary_key=True)
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=128)
#     created_at = models.DateTimeField(auto_now_add=True)
#     last_login_at = models.DateTimeField(blank=True, null=True)

#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"

class Label(models.Model):
    name = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=7) # for storing hex color codes
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class LearningNote(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)
    labels = models.ManyToManyField(Label, related_name='learning_notes')

    class Meta:
        ordering = ['-created_at']  # Order notes by most recent first
        verbose_name = 'Learning Note'
        verbose_name_plural = 'Learning Notes'
        indexes = [
            models.Index(fields=['user', 'created_at']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super(LearningNote, self).save(*args, **kwargs)