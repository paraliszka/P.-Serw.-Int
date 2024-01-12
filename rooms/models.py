from django.db import models
from django.db.models import Sum

from user.models import User


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Rooms(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    link = models.CharField(max_length=1000)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    #wyświetlanie pokoi od najnowszego
    class Meta:
        ordering = ['-updated', '-created']

    def get_rating(self):
        return RoomRating.objects.filter(room=self).aggregate(Sum('rating'))['rating__sum'] or 0

    def __str__(self):
        return self.name


class Message(models.Model):
    # forenkey jeśli zostanie usunięty pokój to wiadomości też
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)

    content = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

class RoomRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def get_rating(self):
        return self.rating