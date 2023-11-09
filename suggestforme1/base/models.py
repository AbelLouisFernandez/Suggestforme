from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.CharField(max_length=100)
    avatar = models.ImageField(null=True,blank=True,default="avatar.png")
    #USERNAME_FIELD = 'email'

    # Add any additional fields or methods as needed

    def __str__(self):
        return self.username

class anime(models.Model):
  name=models.CharField(max_length=100)
  description=models.CharField(max_length=10000,null=True,blank=True)
  status=models.CharField(max_length=100,null=True,blank=True)
  season=models.IntegerField(null=True,blank=True)
  episodeperseason=models.IntegerField(null=True,blank=True)
  genres=models.CharField(max_length=100,null=True,blank=True)
  banner=models.ImageField(null=True,blank=True)
  format=models.CharField(max_length=100,null=True,blank=True)
  startyear=models.DateField(null=True,blank=True)
  endyear=models.DateField(null=True,blank=True)
  trailerlink=models.CharField(max_length=10000,null=True,blank=True)
  studio=models.CharField(max_length=1000,null=True,blank=True)
  def __str__(self):
    return self.name


class userwatchedstatus(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    anime = models.ForeignKey(anime, on_delete=models.CASCADE)
    viewed = models.BooleanField(default=False)

    def __str__(self):
     return f"{self.user.username} viewed {self.anime.name}"


