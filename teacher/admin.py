from teacher.models import NGO, NGO_Admin, CHW, Content
from django.contrib import admin

# Register your models here.
admin.site.register(NGO)
admin.site.register(NGO_Admin)
admin.site.register(CHW)
admin.site.register(Content)


# @admin.register(Committee)
# class CommitteeAdmin(admin.ModelAdmin):
#     readonly_fields = ("committee_id",)
