from django.contrib import admin
from home.models import UserDetail

# Register your models here.
class UserDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'uname', 'email', 'fname', 'lname', 'gender', 'phone', 'password')
   
admin.site.register(UserDetail, UserDetailAdmin)    
