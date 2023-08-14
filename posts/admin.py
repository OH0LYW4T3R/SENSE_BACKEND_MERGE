from django.contrib import admin

from .models import Post, Report

# Register your models here.
@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    pass

@admin.register(Report)
class ReportModelAdmin(admin.ModelAdmin):
    pass