from django.db import models
from django.conf import settings


class Specialist(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="specialist_profile"
    )

    specialty = models.CharField(max_length=255)
    bio = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.specialty}"

class Availability(models.Model):
    specialist = models.ForeignKey(
        Specialist,
        on_delete=models.CASCADE,
        related_name="availabilities"
    )

    weekday = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ("specialist", "weekday", "start_time")

    def __str__(self):
        return f"{self.specialist.user.username} - {self.weekday}"
