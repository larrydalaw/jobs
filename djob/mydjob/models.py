from django.db import models

class DJobItem(models.Model):


  id =  models.IntegerField()
  job_name =  models.CharField(max_length= 50 )
  job_id =  models.CharField(max_length=50 )
  company =  models.CharField(max_length= 100)
  detail =  models.CharField(max_length=700 )
  industry =  models.CharField(max_length=45 )
  salaryfrom =  models.IntegerField()
  salaryto =  models.IntegerField()
  area =  models.CharField(max_length= 30)
  vacant =  models.IntegerField()
  date_posted =  models.DateTimeField()
