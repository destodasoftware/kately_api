from django.db import models


class Utility(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    create = models.DateField(auto_now_add=True)
    update = models.DateField(auto_now=True)
    is_valid = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)

    class Meta:
        abstract = True
