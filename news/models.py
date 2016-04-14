from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Reporter(models.Model):
	full_name = models.CharField(max_length=70)
	
	def __str__(self): #__unicode__ on Python 2
		return self.full_name

class Article(models.Model):
	pub_date = models.DataField()
	headline = models.CharField(max_length=200)
	content = models.TextField()
	reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)

	def __str__(self): #__unicode__ on Python 2
		return self.headline


