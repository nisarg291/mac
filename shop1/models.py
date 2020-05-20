from django.db import models
# it is one type of vo class
# Create your models here.
class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=1000)
    desc1= models.CharField(max_length=2000,default="")
    pub_date = models.DateField()
    image = models.ImageField(upload_to='shop/images', default="")

    # it is use to what is display in admin pannel (database) so in each entry it display the product name of each product
    def __str__(self):
        return self.product_name

class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100, default="")
    phone = models.CharField(max_length=100, default="")
    desc = models.CharField(max_length=1000, default="")

    # it is use to what is display in admin pannel (database) so in each entry it display the name of each user
    def __str__(self):
        return self.name

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=6000)
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=120)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120)
    zip_code = models.CharField(max_length=120)
    phone = models.CharField(max_length=120, default="")

class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)
    #using this we do not need to add timestmp it automatic take current time

    # it is use to what is display in admin pannel (database) so in each entry it display the description of each order
    def __str__(self):
        return self.update_desc[0:7] + "..."