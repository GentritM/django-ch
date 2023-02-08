from datetime import datetime
from django.db import models


class SwapiMetaData(models.Model):
    """SwapiMetaData model."""

    filename = models.CharField(max_length=100)
    date = models.CharField(max_length=120)
    csv_location = models.CharField(max_length=166)

    def __str__(self):
        return self.filename
