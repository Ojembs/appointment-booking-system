from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from patients.models import Patient
from specialists.models import Specialist
from .models import User


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'patient':
            Patient.objects.create(user=instance)
        elif instance.role == 'specialist':
            Specialist.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.role == 'patient' and hasattr(instance, 'patient_profile'):
        instance.patient_profile.save()
    elif instance.role == 'specialist' and hasattr(instance, 'specialist_profile'):
        instance.specialist_profile.save()