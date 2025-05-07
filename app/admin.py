from django.contrib import admin
from .models import User,Url

class AdminUser(admin.ModelAdmin):
    list_display = ['email','username']
    list_filter = ['email','username']

class UrlAdmin(admin.ModelAdmin):
    list_display = ['original_url','short_url',]
    
admin.site.register(User,AdminUser)
admin.site.register(Url,UrlAdmin)
