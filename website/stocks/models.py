# # -*- coding: utf-8 -*-
# from __future__ import unicode_literals

# from django.db import models

# # Create your models here.
from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.models import User
from datetime import datetime


class Stock(models.Model):
    user = models.ForeignKey(User)
    symbol = models.CharField(_('Symbol'), max_length=100)
    # symbol 	= models.ForeignKey(SymbolInfo)

class SymbolInfo(models.Model):
	Handle = models.CharField(primary_key = True, max_length=100)
	Name = models.CharField(max_length=100)
	Exchange = models.CharField(max_length=10)
	Country = models.CharField(max_length=50)
	DateStamp = models.DateField(default = datetime(1960,3,12,0,0))

class Historical(models.Model):
	Handle = models.ForeignKey(SymbolInfo, on_delete = models.CASCADE)
	Date = models.DateField()
	Open = models.FloatField()
	High = models.FloatField()
	Low = models.FloatField()
	Close = models.FloatField()
	Volume = models.FloatField()
	Adj_Close = models.FloatField()
	class Meta:
		unique_together = (("Handle", "Date"),)
