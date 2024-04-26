from django.db import models

# Create your models here.

class logintable(models.Model):
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    type=models.CharField(max_length=50)

class policetable(models.Model):
    LOGIN=models.ForeignKey(logintable,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    address=models.CharField(max_length=50)
    idproof=models.FileField()
    phone=models.BigIntegerField()
    email=models.CharField(max_length=50)
    rank=models.CharField(max_length=50)



class feedbacktable(models.Model):
    security = models.ForeignKey(policetable, on_delete=models.CASCADE)
    comments=models.CharField(max_length=100)
    date=models.DateField()

class emergencytable(models.Model):
    police=models.ForeignKey(policetable,on_delete=models.CASCADE)
    message=models.CharField(max_length=100)
    date=models.DateField()
    time=models.TimeField()
    response=models.CharField(max_length=100)


class cameratable(models.Model):
    camera_no=models.IntegerField()
    latitude=models.FloatField()
    longitude=models.FloatField()

class notificationtable(models.Model):
    camera=models.ForeignKey(cameratable,on_delete=models.CASCADE)
    notification=models.CharField(max_length=100)
    response=models.CharField(max_length=100)
    date=models.DateField()
    time=models.TimeField()
