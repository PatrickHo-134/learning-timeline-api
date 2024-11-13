from pyexpat import model
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils import timezone
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVector

class Label(models.Model):
    name = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=7)  # for storing hex color codes
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'label'

    def __str__(self):
        return self.name


class Collection(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=50)
    is_archived = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'collection'
        ordering = ['-created_at']
        verbose_name = 'Collection'

    def archive_collection(self):
        # Archived the collection and all related learning notes
        self.is_archived = True
        self.save()

        # Archive all learning notes that belong to this collection
        self.collection_notes.update(archived=True)

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
    collection = models.ForeignKey(
        Collection, null=True, blank=True, on_delete=models.SET_NULL, related_name='collection_notes')

    # Add SearchVectorField for full-text search
    search_vector = SearchVectorField(null=True)

    class Meta:
        db_table = 'learning_note'
        ordering = ['-created_at']  # Order notes by most recent first
        verbose_name = 'Learning Note'
        verbose_name_plural = 'Learning Notes'
        indexes = [
            models.Index(fields=['user', 'created_at']),
            GinIndex(fields=['search_vector']),
        ]

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        self.search_vector = SearchVector('title', 'content')
        super(LearningNote, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
