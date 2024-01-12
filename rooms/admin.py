from django.contrib import admin
from rooms import models

admin.site.register(models.Topic)
admin.site.register(models.Rooms)
admin.site.register(models.Message)
admin.site.register(models.RoomRating)