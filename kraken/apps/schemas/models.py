from django.db import models
import time
from kraken.apps.core.models import ClientSchema


class SchemaVersion(models.Model):
    # delimiter options
    FIXED = 'Fixed'
    PIPE = 'Pipe'
    COMMA = 'Comma'
    DELIMITER_TYPE_CHOICES = (
        (FIXED, 'Fixed'),
        (PIPE, 'Pipe'),
        (COMMA, 'Comma')
    )

    identifier = models.CharField(max_length=50)
    client_schema = models.ForeignKey(ClientSchema)
    current = models.BooleanField(default=True)
    delimiter = models.TextField(choices=DELIMITER_TYPE_CHOICES, default=FIXED)

    class Meta:
        unique_together = (("identifier", "client_schema"), )


def version_batch_location(instance, filename):
    return "{0}_{1}".format(str(time.time()).replace('.', ''), filename)


class VersionBatch(models.Model):
    identifier = models.CharField(max_length=200)
    schema_version = models.ForeignKey(SchemaVersion)
    last_opened = models.DateTimeField('last opened', auto_now=True)
    contents = models.FileField(upload_to=version_batch_location)

    @property
    def batch_file_path(self):
        return ''


class SchemaColumn(models.Model):
    # field type options
    USER_DEFINED_LIST = 'User defined list'
    FIRST_NAME = 'First name'
    LAST_NAME = 'Last name'
    ADDRESS = 'Address'
    ZIP_CODE = 'Zip code'
    FIELD_TYPE_CHOICES = (
        (USER_DEFINED_LIST, 'User defined list'),
        (FIRST_NAME, 'First name'),
        (LAST_NAME, 'Last name'),
        (ADDRESS, 'Address'),
        (ZIP_CODE, 'Zip code')
    )

    position = models.IntegerField()
    schema_version = models.ForeignKey(SchemaVersion)
    name = models.CharField(max_length=200)
    field_type = models.TextField(choices=FIELD_TYPE_CHOICES, default=USER_DEFINED_LIST)
    length = models.IntegerField()
    unique = models.BooleanField(default=True)
    payload = models.TextField()
