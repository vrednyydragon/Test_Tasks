from django.db import models

class Alias(models.Model):
    alias = models.TextField(blank=True, null=True)
    target = models.TextField(max_length=24)
    start = models.DateTimeField()
    end = models.DateTimeField(default='9999-12-31 00:00:00.000001+00:00')

    def __str__(self):
        return f"{self.alias}- {self.target} - {self.start} - {self.end}"
