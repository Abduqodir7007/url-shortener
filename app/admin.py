from django.contrib import admin
from .models import User,Url,ClickEvent 
# Register your models here.
admin.site.register(User)
admin.site.register(Url)
admin.site.register(ClickEvent)