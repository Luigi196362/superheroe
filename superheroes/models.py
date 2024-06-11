from django.db import models
from django.conf import settings

# Create your models here.
class Superheroe(models.Model):
    name = models.TextField()
    image = models.URLField()
    characteristics = models.TextField()


    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)

class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    superheroe = models.ForeignKey('superheroes.Superheroe', related_name='votes', on_delete=models.CASCADE)
    