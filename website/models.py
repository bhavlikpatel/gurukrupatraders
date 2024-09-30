from django.db import models
from django.contrib.auth.models import User


class Quarry(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Material(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
class TruckNo(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Record(models.Model):
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    challan_no = models.CharField(max_length=50)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    weight = models.CharField(max_length=15)
    quarry = models.ForeignKey(Quarry, on_delete=models.CASCADE) 
    royalty_pass = models.CharField(max_length=50)
    truck_no = models.ForeignKey(TruckNo, on_delete=models.CASCADE)
    delivered_at = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.truck_no} {self.delivered_at}"

# class Record(models.Model):
# 	created_at = models.DateTimeField(auto_now_add=True)
# 	first_name = models.CharField(max_length=50)
# 	last_name =  models.CharField(max_length=50)
# 	email =  models.CharField(max_length=100)
# 	phone = models.CharField(max_length=15)
# 	address =  models.CharField(max_length=100)
# 	city =  models.CharField(max_length=50)
# 	state =  models.CharField(max_length=50)
# 	zipcode =  models.CharField(max_length=20)

# 	def __str__(self):
# 		return(f"{self.first_name} {self.last_name}")
