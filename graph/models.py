from django.db import models


# Create your models here.


class Forecast(models.Model):
    timestamp = models.DateTimeField()
    yhat = models.IntegerField()
    y = models.IntegerField()
    yhat_upper = models.IntegerField()
    yhat_lower = models.IntegerField()
    anomaly = models.FloatField()
    location = models.CharField(max_length=7)
    pred_date = models.DateTimeField()
    indicator = models.IntegerField()
    updated = models.DateTimeField(auto_now=True)