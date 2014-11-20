from django.db import models
from django.contrib.auth.models import User

# Tables
class UserExtra(models.Model):
	userid = models.CharField(User, max_length=25, blank=True, null=True)
	verified = models.BooleanField(null=False, default=False)
	approval_date = models.DateField(blank=True, null=True)

	# Return a nice, human-readable representation of the model from the __unicode__() method.
	def __unicode__(self):
		return self.userid

class Link(models.Model):
	name = models.CharField(max_length=50, blank=False, null=False)    
	link = models.URLField(blank=False, null=False)
	dateCreated = models.DateField(editable=False)
	dateUpdated = models.DateField()
	tags =  models.TextField(blank=True, null=True)

	# Return a nice, human-readable representation of the model from the __unicode__() method.
	def __unicode__(self):
		return self.name

class List(models.Model):
	name = models.CharField(max_length=50, blank=False, null=False)     
	dateCreated = models.DateField(editable=False)
	dateUpdated = models.DateField()
	links = models.ManyToManyField(Link)

	# Return a nice, human-readable representation of the model from the __unicode__() method.
	def __unicode__(self):
		return self.name