from django.db import models

# Create your models here.

class Shop(models.Model):
    reg_id=models.IntegerField(primary_key=True)
    lid=models.CharField(max_length=200)
    name=models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    longitude=models.FloatField(max_length=200)
    latitude=models.FloatField(max_length=200)
    phone=models.CharField(max_length=200)
    address=models.CharField(max_length=200)
    status=models.CharField(max_length=200,default=0)

class Service_center(models.Model):
    reg_id=models.IntegerField(primary_key=True)
    lid=models.CharField(max_length=200)
    name=models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    longitude=models.FloatField(max_length=200,default=76.2971463)
    latitude=models.FloatField(max_length=200,default=9.9930384)
    phone=models.CharField(max_length=200)
    address=models.CharField(max_length=200)
    status=models.CharField(max_length=200,default=0)    

class User(models.Model):
    reg_id=models.IntegerField(primary_key=True)
    lid=models.CharField(max_length=200)
    name=models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    gender=models.CharField(max_length=200)
    dob=models.CharField(max_length=200)
    phone=models.CharField(max_length=200)
    address=models.CharField(max_length=200)
    status=models.CharField(max_length=200,default=0) 
    r_status=models.CharField(max_length=200,default=1) 

class Login(models.Model):
    username=models.CharField(max_length=200)
    password=models.CharField(max_length=200)
    type1=models.CharField(max_length=200)

class Product(models.Model):
    name=models.CharField(max_length=200)
    sh_id=models.CharField(max_length=200)
    image=models.CharField(max_length=200)
    offer=models.IntegerField()
    amount=models.IntegerField()
    quantity=models.IntegerField()
    total=models.IntegerField()
    unique_id=models.CharField(max_length=200)
    brand=models.CharField(max_length=200)
    about_pro=models.CharField(max_length=200)
    rating=models.CharField(max_length=200,default='2')
    
class Feedback(models.Model):
    name=models.CharField(max_length=200)
    feedback=models.CharField(max_length=200)
    lid=models.IntegerField()
    pro_id=models.IntegerField()  
    sentiment=models.CharField(max_length=200)
    date=models.DateField(auto_now_add=True)

class Trouble(models.Model):
    product_id=models.CharField(max_length=200)
    trouble=models.CharField(max_length=200)
    solution=models.CharField(max_length=200)

class Booking(models.Model):
    uid=models.CharField(max_length=200,default='0')
    product_id=models.CharField(max_length=200)
    sid=models.CharField(max_length=200)
    problem=models.CharField(max_length=200)
    date=models.DateField(auto_now_add=True)
    status=models.CharField(max_length=200)


class Order(models.Model):
    uid=models.CharField(max_length=200,default='0')
    product_id=models.CharField(max_length=200)
    sh_id=models.CharField(max_length=200)
    date=models.DateField(auto_now_add=True)
    status=models.CharField(max_length=200)

  




