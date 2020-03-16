"""
Definition of models.
"""
from django.db import models

# Create your models here.


#class users(models.Model):
    #id = models.CharField(max_length=30).primary_key=True
    #member_id = models.CharField(max_length=60)
    #username = models.CharField(max_length=60)
    #password = models.CharField(max_length=60)
    #exp_date = models.CharField(max_length=60)
    #admin_enabled = models.CharField(max_length=60)
    #password = models.CharField(max_length=60)
    #password = models.CharField(max_length=60)
    #password = models.CharField(max_length=60)
    #password = models.CharField(max_length=60)
    #password = models.CharField(max_length=60)
    #password = models.CharField(max_length=60)
    #password = models.CharField(max_length=60)
    #password = models.CharField(max_length=60)
    #password = models.CharField(max_length=60)
    #password = models.CharField(max_length=60)
    #password = models.CharField(max_length=60)
    #password = models.CharField(max_length=60)
    #password = models.CharField(max_length=60)
    #password = models.CharField(max_length=60)
    #password = models.CharField(max_length=60)
    #password = models.CharField(max_length=60)
    #password = models.CharField(max_length=60)
    #password = models.CharField(max_length=60)
    #password = models.CharField(max_length=60)
    #password = models.CharField(max_length=60)
    #password = models.CharField(max_length=60)
    #password = models.CharField(max_length=60)
    #password = models.CharField(max_length=60)
    #password = models.CharField(max_length=60)
    #password = models.CharField(max_length=60)


class SqlModel(models.Model):
    q_id = models.IntegerField()



class University(models.Model):
    name = models.CharField(max_length=50)
 
    class Meta:
        verbose_name = "University"
        verbose_name_plural = "Universities"
 
    def __unicode__(self):
        return self.name
 
class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    university = models.ForeignKey(University, on_delete=models.DO_NOTHING)
 
    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
 
    def __unicode__(self): 
        return '%s %s' % (self.first_name, self.last_name)