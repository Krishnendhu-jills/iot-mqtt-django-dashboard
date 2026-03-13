from django.db import models

class SensorData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)  # when the reading arrives
    value = models.FloatField()  # temperature value
    topic = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.timestamp}: {self.value}"
