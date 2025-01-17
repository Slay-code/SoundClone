from django.db import models
from django.contrib.auth.models import User


class Track(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="images/")
    song = models.FileField(upload_to="songs/")
    author = models.CharField(max_length=200)
    album = models.ForeignKey(to="MusicAlbum", on_delete=models.CASCADE, blank=True, null=True)
    user = models.ManyToManyField(to=User, blank=True, related_name="tracks")
    
    class Meta:
        db_table = "Track"
        
    def __str__(self):
        return self.name


class MusicAlbum(models.Model):
    name = models.CharField(max_length=355)
    image_album = models.ImageField(upload_to="images/album/")
    
    class Meta:
        db_table = "Music_Album"
        
    def __str__(self):
        return self.name