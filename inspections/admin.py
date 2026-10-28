from django.contrib import admin
from .models import Company,Membership,Inspection,Activity
admin.site.register(Company)
admin.site.register(Membership)
@admin.register(Inspection)
class InspectionAdmin(admin.ModelAdmin):
 list_display=('job_number','insured_name','town','status','job_fee','company')
 search_fields=('job_number','insured_name','property_address','policy_number')
 list_filter=('status','company','paid')
 def get_queryset(self,request):
  qs=super().get_queryset(request)
  return qs if request.user.is_superuser else qs.filter(company__memberships__user=request.user).distinct()
 def has_module_permission(self,request):return request.user.is_superuser
admin.site.register(Activity)
