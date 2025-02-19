from django.db import models

# Create your models here.

class newregistration(models.Model):
    Fullname = models.CharField(max_length=30)
    Email = models.CharField(max_length=50)
    Mobile = models.IntegerField()
    Age = models.IntegerField()
    Gender = models.CharField(max_length=20)
    Address = models.CharField(max_length=300)
    Propic = models.ImageField(upload_to='images/')
    Password = models.CharField(max_length=20)
    def __str__(self):
        return self.Fullname

class sparereg(models.Model):
    sparename=models.CharField(max_length=30)
    spareprice = models.IntegerField()
    sparepic = models.ImageField(upload_to='images/')
    sparecompany = models.CharField(max_length=200)
    sparedesc = models.CharField(max_length=200)
    sparecategory = models.CharField(max_length=20)
    sparemodel=models.CharField(max_length=30)
    def __str__(self):
        return self.sparename

class addtocart(models.Model):
    userid = models.IntegerField()
    item = models.ForeignKey(sparereg, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class wishlist(models.Model):
    userid=models.IntegerField()
    item=models.ForeignKey(sparereg,on_delete=models.CASCADE)

class address(models.Model):
    userdetails = models.ForeignKey(newregistration, on_delete=models.CASCADE)
    addressline1=models.CharField(max_length=200)
    addressline2=models.CharField(max_length=200)
    pincode=models.IntegerField()
    city=models.CharField(max_length=20)
    state=models.CharField(max_length=30)
    contact_name=models.CharField(max_length=30)
    contact_number=models.IntegerField()

class Order(models.Model):
    userdetails=models.ForeignKey(newregistration,on_delete=models.CASCADE)
    address=models.ForeignKey(address,on_delete=models.CASCADE)
    ordered_date=models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    order_pic=models.ImageField()
    pro_name=models.CharField(max_length=20)
    quantity=models.IntegerField()
    price=models.IntegerField()
    order_status=models.BooleanField(default=True)
class billing_db(models.Model):
    Email=models.EmailField(max_length=100,null=True,blank=True)
    Name=models.CharField(max_length=100,null=True,blank=True)
    Address=models.CharField(max_length=100,null=True,blank=True)
    Phone=models.CharField(max_length=100,null=True,blank=True)
    Description=models.CharField(max_length=100,null=True,blank=True)
    Total_Price=models.IntegerField(null=True,blank=True)
class contact_db(models.Model):
    Name=models.CharField(max_length=100,null=True,blank=True)
    Email=models.EmailField(max_length=100,null=True,blank=True)
    Subject=models.CharField(max_length=100,null=True,blank=True)
    Message=models.CharField(max_length=100,null=True,blank=True)
    

#here order models have no connection with cart model






