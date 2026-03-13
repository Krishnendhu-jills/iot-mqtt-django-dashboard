from django.contrib import admin
from .models import SensorData

#first code
# admin.site.register(SensorData)



@admin.register(SensorData)
class SensorDataAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "temperature", "ph", "turbidity")
    list_filter = ("timestamp",)
    search_fields = ("temperature", "ph", "turbidity")
    ordering = ("-timestamp",)
    
# Change admin page titles
admin.site.site_header = "IoT Water Quality Monitoring Admin"
admin.site.site_title = "Water Quality Dashboard"
admin.site.index_title = "Sensor Data Administration"

