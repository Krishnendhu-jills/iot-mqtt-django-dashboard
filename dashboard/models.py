from django.db import models

class SensorData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    temperature = models.FloatField(null=True, blank=True)
    ph = models.FloatField(null=True, blank=True)
    turbidity = models.FloatField(null=True, blank=True)

    def __str__(self):
         return f"T:{self.temperature} pH:{self.ph} Turb:{self.turbidity}"
