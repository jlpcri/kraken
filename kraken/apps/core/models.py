import time
from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def schemas(self):
        return ClientSchema.objects.filter(client=self)


class ClientSchema(models.Model):
    name = models.CharField(max_length=200)
    client = models.ForeignKey(Client)

    class Meta:
        unique_together = (("name", "client"), )

    def versions(self):
        return SchemaVersion.objects.filter(client_schema=self)


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
    client_schema = models.ForeignKey(ClientSchema, related_name='schema')
    current = models.BooleanField(default=True)
    delimiter = models.TextField(choices=DELIMITER_TYPE_CHOICES, default=FIXED)

    class Meta:
        unique_together = (("identifier", "client_schema"), )

    def files(self):
        return VersionFile.objects.filter(schema_version=self)

    def getFields(self):
        return SchemaColumn.objects.filter(schema_version=self)

    def saveFields(self, fields=[]):
        for i, f in enumerate(fields):
            column = SchemaColumn(schema_version=self)
            column.position = i+1
            column.name = f.get('name')
            column.length = f.get('length')
            if f.get('type') == 'Number':
                column.type = SchemaColumn.NUMBER
            elif f.get('type') == 'Text':
                column.type = SchemaColumn.TEXT
            if f.get('unique'):
                column.unique = True
            else:
                column.unique = False
            column.save()
        return self.getFields()

    def validateFields(self, fields=[]):
        for i, f in enumerate(fields):
            pass


class VersionFile(models.Model):
    name = models.CharField(max_length=200)
    schema_version = models.ForeignKey(SchemaVersion)

    class Meta:
        unique_together = (("name", "schema_version"), )


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

class BatchField(models.Model):
    NUMBER = 'Number'
    RANDOM_TEXT = 'Random text'
    USER_DEFINED_LIST = 'User defined list'
    FIRST_NAME = 'First name'
    LAST_NAME = 'Last name'
    ADDRESS = 'Address'
    ZIP_CODE = 'Zip code'
    GENERATOR_CHOICES = (
        (RANDOM_TEXT, 'Random text'),
        (NUMBER, 'Number'),
        (USER_DEFINED_LIST, 'User defined list'),
        (FIRST_NAME, 'First name'),
        (LAST_NAME, 'Last name'),
        (ADDRESS, 'Address'),
        (ZIP_CODE, 'Zip code')
    )

    parent = models.ForeignKey('VersionBatch')
    column = models.ForeignKey('SchemaColumn')
    generator = models.TextField(choices=GENERATOR_CHOICES, default=RANDOM_TEXT)
    payload = models.TextField()  # JSON objects defining options for chosen generator


class SchemaColumn(models.Model):
    # field type options
    TEXT = 'Text'
    NUMBER = 'Number'
    FIELD_TYPE_CHOICES = (
        (TEXT, 'Text'),
        (NUMBER, 'Number')
    )

    position = models.IntegerField()
    schema_version = models.ForeignKey(SchemaVersion)
    name = models.CharField(max_length=200, blank=False)
    type = models.TextField(choices=FIELD_TYPE_CHOICES, default=TEXT)
    length = models.IntegerField()
    unique = models.BooleanField(default=True)

    class Meta:
        unique_together = (("name", "schema_version"), )