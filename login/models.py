from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import math
# Create your models here.

class Fav(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    spot_id = models.CharField(max_length=200) 
    title = models.CharField(max_length=200) 
    author = models.CharField(max_length=200) 
    image =  models.CharField(max_length=200) 
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title) + "_" + str(self.id)

    def diff(self):
        seconds = (timezone.now() - self.created).total_seconds()
        minutes = seconds / 60
        if minutes < 1: return {"value": math.floor(seconds), "tag": "secondes"}
        hours = minutes / 60
        if hours < 1: return {"value": math.floor(minutes), "tag": "minutes"}
        days = hours / 24
        if days < 1: return {"value": math.floor(hours), "tag": "heures"}
        years = days / 365.25
        if years < 1: return {"value": math.floor(days), "tag": "jours"} 
        return {
            "value": math.floor(years), "tag": "années"
        }

    timeSince = property(diff)

    class Meta:
        ordering = ["created"]

    