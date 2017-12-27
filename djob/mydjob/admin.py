from django.contrib import admin

# Register your models here.

from djobs.models import DJobItem

class DJobAdmin(admin.ModelAdmin):
    list_display = ['id', 'job_name', 'job_id', 'company', 'detail', 'industry', 'salaryfrom', 'salaryto', 'area', 'vacant', 'date_posted']


admin.site.register(DJobItem,DJobAdmin)