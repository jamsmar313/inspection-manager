from django.db import models
from django.contrib.auth.models import User
class Company(models.Model):
 name=models.CharField(max_length=200,unique=True)
 def __str__(self):return self.name
class Membership(models.Model):
 ROLES=[('owner','Owner'),('admin','Administrator'),('inspector','Inspector'),('bookkeeper','Bookkeeper')]
 company=models.ForeignKey(Company,on_delete=models.CASCADE,related_name='memberships')
 user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='company_memberships')
 role=models.CharField(max_length=20,choices=ROLES,default='inspector')
 class Meta:constraints=[models.UniqueConstraint(fields=['company','user'],name='unique_company_member')]
class Inspection(models.Model):
 company=models.ForeignKey(Company,on_delete=models.CASCADE,related_name='inspections')
 job_number=models.CharField(max_length=120)
 insured_name=models.CharField(max_length=255,blank=True)
 property_address=models.CharField(max_length=300,blank=True)
 area=models.CharField(max_length=100,blank=True)
 town=models.CharField(max_length=150,blank=True)
 phone=models.CharField(max_length=100,blank=True)
 policy_number=models.CharField(max_length=120,blank=True)
 insurance_carrier=models.CharField(max_length=200,blank=True)
 inspection_company=models.CharField(max_length=200,blank=True)
 agent_name=models.CharField(max_length=200,blank=True)
 agent_phone=models.CharField(max_length=100,blank=True)
 date_assigned=models.DateField(null=True,blank=True)
 job_fee=models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
 status=models.CharField(max_length=60,default='New')
 scheduled_at=models.DateTimeField(null=True,blank=True)
 inspection_complete_date=models.DateField(null=True,blank=True)
 report_submitted_date=models.DateField(null=True,blank=True)
 paid=models.BooleanField(default=False)
 payment_date=models.DateField(null=True,blank=True)
 next_action_date=models.DateField(null=True,blank=True)
 contact_notes=models.TextField(blank=True)
 general_notes=models.TextField(blank=True)
 exterior_notes=models.TextField(blank=True)
 roof_notes=models.TextField(blank=True)
 electrical_notes=models.TextField(blank=True)
 plumbing_notes=models.TextField(blank=True)
 hvac_notes=models.TextField(blank=True)
 occupancy_notes=models.TextField(blank=True)
 hazards_notes=models.TextField(blank=True)
 photos_measurements=models.TextField(blank=True)
 field_notes=models.TextField(blank=True)
 calendar_event_id=models.CharField(max_length=255,blank=True)
 assigned_inspector=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='assigned_inspections')
 created_at=models.DateTimeField(auto_now_add=True)
 updated_at=models.DateTimeField(auto_now=True)
 class Meta:
  constraints=[models.UniqueConstraint(fields=['company','job_number'],name='unique_job_per_company')]
  ordering=['-updated_at']
 def __str__(self):return f'{self.job_number} — {self.insured_name}'
class Activity(models.Model):
 inspection=models.ForeignKey(Inspection,on_delete=models.CASCADE,related_name='activities')
 user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
 event=models.CharField(max_length=100)
 detail=models.TextField(blank=True)
 created_at=models.DateTimeField(auto_now_add=True)
