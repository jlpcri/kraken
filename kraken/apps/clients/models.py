from django.db import models
from django.conf import settings


class Client(models.Model):
    name = models.CharField(max_length=200, unique=True)


class ClientSchema(models.Model):
    name = models.CharField(max_length=200)
    client = models.ForeignKey(Client)

    class Meta:
        unique_together = (("name", "client"), )


class SchemaVersion(models.Model):
    identifier = models.CharField(max_length=50)
    client_schema = models.ForeignKey(ClientSchema)
    current = models.BooleanField(default=True)
    delimiter = models.CharField(max_length=200)


class VersionBatch(models.Model):
    identifier = models.CharField(max_length=200)
    schema_version = models.ForeignKey(SchemaVersion)
    last_opened = models.CharField(max_length=200)
    contents = models.FileField(upload_to='')


class SchemaColumn(models.Model):
    position = models.IntegerField()
    schema_version = models.ForeignKey(SchemaVersion)
    name = models.CharField(max_length=200)
    field_type = models.TextField(choices='')
    length = models.IntegerField()
    unique = models.BooleanField(default=True)
    payload = models.TextField()