from django.db import models


class Layout(models.Model):
    depth = models.FloatField(default=1.5)
    arrangement = models.CharField(max_length=200)
    cable_spacing_m = models.FloatField(default=0)
    outer_diameter_m = models.FloatField(default=0.1)
