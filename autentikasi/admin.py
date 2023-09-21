from django.contrib import admin
from .models import CustomGroup, CustomUser, Student, Lecturer

admin.site.register(CustomGroup)
admin.site.register(CustomUser)
admin.site.register(Student)
admin.site.register(Lecturer)
