from django.contrib import admin

from .models import Week, Thread, ReferenceFile
admin.site.register(Week)
admin.site.register(Thread)
admin.site.register(ReferenceFile)
