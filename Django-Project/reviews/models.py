from django.db import models


class Reviews(models.Model):
    productid = models.CharField(max_length=250)
    userid = models.CharField(max_length=250)
    profilename = models.CharField(max_length=250)
    score = models.FloatField()
    indice = models.IntegerField()
    summary = models.TextField()
    text = models.TextField(blank=True, null=True)
    timed = models.DateField(blank=True, null=True)
    helpfulness = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reviews'
