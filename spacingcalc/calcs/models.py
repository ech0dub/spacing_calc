from django.db import models


class Layout(models.Model):
    layout_name = models.CharField(max_length=200, default='Enter description of layout')
    pub_date = models.DateTimeField('date published')
    depth_to_top_m = models.FloatField(default=1.5)
    arrangement = models.CharField(max_length=200, default='touching trefoil')
    cable_spacing_m = models.FloatField(default=0)
    outer_diameter_m = models.FloatField(default=0.1)

    def __str__(self):
        return self.layout_name
