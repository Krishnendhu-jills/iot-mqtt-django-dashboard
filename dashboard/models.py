
from django.db import models

class SensorData(models.Model):
    topic = models.CharField(max_length=100)
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.topic} - {self.value}"