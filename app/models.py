from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    phone = models.CharField(max_length=20, unique=True)


class ClientMaster(models.Model):
	company_name = models.CharField(max_length=250)
	industry_type = models.CharField(max_length=250, null=True)
	country = models.CharField(max_length=250)
	address1 = models.CharField(max_length=250, null=True)
	address2 = models.CharField(max_length=250, null=True)
	state = models.CharField(max_length=250)
	pin = models.CharField(max_length=50)
	email = models.EmailField(max_length = 254)


class DrvingLicence(models.Model):
	licence_id = models.CharField(max_length=25)
	country = models.CharField(max_length=50)
	valid_up_to = models.DateField(null=True, blank=True)



# class UploadFiles(forms.Form):
# 	title = forms.CharField(max_length=50)
#     file = forms.FileField() document_files

class Interview(models.Model):
	company = models.ForeignKey(ClientMaster, on_delete=models.CASCADE, null=True, blank=True)
	# candidate  = models.ForeignKey(Candidate, on_delete=models.CASCADE, null=True, blank=True)
	scheduled_on = models.DateTimeField(null=True, blank=True)
	duration_in_min =  models.IntegerField(null=True, blank=True)


class Candidate(models.Model):
	status = (('schedule', 'SCHEDULE'),
				 ('not_schedule', ' NOT SCHEDULE'),
				 ('completed', 'COMPLETED'),
				 ('seleted', 'SELECTED')
				 )

	passport =  (('collected', 'COLLECTED'),
				 ('not_collected', ' NOT COLLECTED')
				 )

	salary_type =  (('per_month', 'MONTHLY'),
				 ('per_annum', 'YEARLY')
				 )
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	primary_mob_no = models.CharField(max_length=15)
	secondary_mob_no = models.CharField(max_length=15, null=True, blank=True)
	age = models.IntegerField()
	dob = models.DateField()
	passport_no = models.CharField(max_length=100, null=True, blank=True)
	passport_expery_date = models.DateField(null=True, blank=True)
	driving_license = models.ManyToManyField(DrvingLicence, null=True, blank=True)
	job_category = models.CharField(max_length=100, null=True, blank=True)
	total_experence = models.FloatField(default=0.0, null=True, blank=True)
	abroad_experence = models.FloatField(default=0.0, null=True, blank=True)
	document_files = models.FileField(blank=True, upload_to='documents/')
	interview  = models.ForeignKey(Interview, on_delete=models.CASCADE, null=True, blank=True)
	interview_status = models.CharField(max_length=40, default = 'not_schedule', choices = status, null=True, blank=True)
	visa_approval_status = models.BooleanField(default=False)
	salary_details = models.TextField(null=True, blank=True)
	passport_status = models.CharField(max_length=40, choices = passport, null=True, blank=True)
	departure_date = models.DateField(null=True, blank=True)
	added_date = models.DateField(auto_now=True,null=True,blank=True)



