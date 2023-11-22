from django.db import models

class School(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)  # Note: 'localisation' en anglais est 'location'

    def __str__(self):
        return self.name

