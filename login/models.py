from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import math
# Create your models here.
class Author(models.Model):
    id = models.AutoField(primary_key=True)
    spotId = models.CharField(max_length=200) 
    name = models.CharField(max_length=100)
    desc = models.TextField(max_length=3000)
    found = models.BooleanField(default=False)
    image = models.CharField(max_length=300)
    link = models.CharField(max_length=200)

    def __str__(self):
        return str(self.name) + "_" + str(self.id)

class Album(models.Model):
    id = models.AutoField(primary_key=True)
    spotId = models.CharField(max_length=200) 
    name = models.CharField(max_length=100)
    dat = models.IntegerField(default=2022, null=True)
    link = models.CharField(max_length=200)
    image = models.CharField(max_length=300)

    def __str__(self):
        return str(self.name) + "_" + str(self.id)


class Song(models.Model):
    id = models.AutoField(primary_key=True)
    spotId = models.CharField(max_length=200) 
    title = models.CharField(max_length=200) 
    author = models.ManyToManyField(Author, symmetrical=False, blank=True, related_name="written_by") 
    # feats = models.ManyToManyField(Author, symmetrical=True, blank=True, related_name="feat_by") 
    durationS = models.IntegerField(null=True)
    durationM = models.IntegerField(null=True)
    lyrics = models.TextField(max_length=10000)
    spotLink = models.CharField(max_length=200)
    ytLink = models.CharField(max_length=200)
    album = models.ManyToManyField(Album, symmetrical=False, blank=True)

    def __str__(self):
        return str(self.title) + "_" + str(self.id)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favs = models.ManyToManyField(
        Song, 
        related_name = "likes",
        symmetrical = False,
        blank = True
        )

    def __str__(self):
        return self.user.username

from django.db.models.signals import post_save

def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

post_save.connect(create_profile, sender=User)









# class Fav(models.Model):
#     id = models.AutoField(primary_key=True)
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
#     spot_id = models.CharField(max_length=200) 
#     title = models.CharField(max_length=200) 
#     author = models.CharField(max_length=200) 
#     image =  models.CharField(max_length=200) 
#     created = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return str(self.title) + "_" + str(self.id)

#     def diff(self):
#         seconds = (timezone.now() - self.created).total_seconds()
#         minutes = seconds / 60
#         if minutes < 1: return {"value": math.floor(seconds), "tag": "secondes"}
#         hours = minutes / 60
#         if hours < 1: return {"value": math.floor(minutes), "tag": "minutes"}
#         days = hours / 24
#         if days < 1: return {"value": math.floor(hours), "tag": "heures"}
#         years = days / 365.25
#         if years < 1: return {"value": math.floor(days), "tag": "jours"} 
#         return {
#             "value": math.floor(years), "tag": "années"
#         }

#     timeSince = property(diff)

#     class Meta:
#         ordering = ["created"]

    