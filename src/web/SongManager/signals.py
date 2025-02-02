from django.db.models.signals import post_migrate
from django.core.management import call_command
from django.dispatch import receiver


@receiver(post_migrate)
def load_initial_data(sender, **kwargs):
    try:
        call_command('loaddata', 'initial_data.json')
        print("Initial data correctly loaded.")
    except Exception as e:
        print(f"Error loading initial data: {e}")
