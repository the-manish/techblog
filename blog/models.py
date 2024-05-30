from django.db import models

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=200)
    cont = models.TextField()
	
    def __str__(self):
	    return self.title

class Contact(models.Model):
	sno = models.AutoField(primary_key=True)
	name = models.CharField(max_length=255,blank=True,null=True)
	email = models.CharField(max_length=255,blank=True,null=True)
	message = models.TextField(blank=True,null=True)

	def __str__(self):
		return self.name