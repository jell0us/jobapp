from django.db import models
from django.contrib.auth.models import User

#Create your models here
class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(blank=False, null=False)
    birthdate = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, blank=True, null=True)
    contactno = models.CharField(max_length=13, blank=False, null=False)
    role = models.CharField(max_length=20, blank=False, null=False)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Job(models.Model):
   title = models.CharField(max_length=200, blank=False, null=False)
   description = models.TextField()
   requirements = models.TextField()
   posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
   posted_date = models.DateTimeField(auto_now_add=True)
   
   def __str__(self):
       return self.title
   
class Application(models.Model):
   job = models.ForeignKey(Job, on_delete=models.CASCADE, blank=False, null=False)
   applicant = models.ForeignKey(User, on_delete=models.CASCADE, null=True) 
   resume = models.FileField(upload_to='resumes/')
   applied_at = models.DateTimeField(auto_now_add=True)
   
   def __str__(self):
       applicant_name = self.applicant.username if self.applicant else 'Unknown Applicant'
       job_title = self.job.title if self.job else 'Unknown Job'
       return f"{applicant_name} applied for {job_title}"
