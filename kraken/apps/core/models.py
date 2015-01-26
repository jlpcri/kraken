from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=200, unique=True)


class ClientSchema(models.Model):
    name = models.CharField(max_length=200)
    client = models.ForeignKey(Client)

    class Meta:
        unique_together = (("name", "client"), )
