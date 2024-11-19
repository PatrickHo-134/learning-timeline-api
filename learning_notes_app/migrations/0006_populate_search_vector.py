# management/commands/populate_search_vector.py

from django.core.management.base import BaseCommand
from django.contrib.postgres.search import SearchVector
from learning_notes_app.models import LearningNote

from django.db import migrations

def populate_search_vector(apps, schema_editor):
    LearningNote = apps.get_model('learning_notes_app', 'LearningNote')
    LearningNote.objects.update(
        search_vector=SearchVector('title', 'content')
    )

class Migration(migrations.Migration):

    dependencies = [
        ('learning_notes_app', '0005_learningnote_search_vector_and_more'),  # Replace with the actual previous migration name
    ]

    operations = [
        migrations.RunPython(populate_search_vector),
    ]
