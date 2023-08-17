from django.db import models

# Create your models here.
class Log(models.Model):
    imagepath=models.CharField(max_length=200)
    predict=models.ForeignKey("lungtype", on_delete=models.CASCADE)
    pubdate=models.CharField(max_length=200)
    def __str__(self):
        return 
    def __unicode__(self):
        return 
    
class lungtype(models.Model):
    condition=models.CharField(max_length=200)
    def __str__(self):
        return 

    def __unicode__(self):
        return 

