from django.contrib import admin

from .models import FireCategory, SubCategory, RiskLevel, FireResponse, UserSubmission

admin.site.register(FireCategory)
admin.site.register(SubCategory)
admin.site.register(RiskLevel)
admin.site.register(FireResponse)
admin.site.register(UserSubmission)