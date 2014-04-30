from django.db import models

# Create your models here.


class Event(models.Model):

    class Meta:
        db_table = 'cn_event'

    name = models.CharField(max_length=40)
    description = models.CharField(max_length=200)

    def __unicode__(self):
        return self.description