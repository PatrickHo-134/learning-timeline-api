from django.contrib import admin

# Register your models here.
from .models import LearningNote, Label

admin.site.register(LearningNote)
admin.site.register(Label)