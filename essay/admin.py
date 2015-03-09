from django.contrib import admin
from essay.models import Essay
from essay.forms import EssayAdmin

# Register your models here.
admin.site.register(Essay,EssayAdmin)
