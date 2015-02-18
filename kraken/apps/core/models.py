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

    def schema_fields_total_length(self):
        fields = SchemaColumn.objects.filter(schema_version=self).order_by('position')
        total_length = 0
        for field in fields:
            total_length += field.length

        return total_length

    def get_columns(self):
        return SchemaColumn.objects.filter(schema_version=self)

    def save_columns(self, columns={}):
        if columns.get('valid'):
            for c in columns.get('fields'):
                c.schema_version = self
                c.save()
        return columns

    def validate_columns(self, post):
        columns = {'valid': True, 'error_message': None, 'fields': None}
        row_order = post.get('row_order', '').strip()
        field_list = []
        if row_order:
            row_order = row_order.strip().split(' ')
            for i, r in enumerate(row_order):
                cid = post.get('hiddenFieldId_' + r)
                if cid:
                    column = SchemaColumn.objects.get(pk=cid)
                else:
                    column = SchemaColumn()
                column.position = i+1
                column.name = post.get('inputFieldName_' + r)
                column.length = post.get('inputFieldLength_' + r)
                ftype = post.get('selectFieldType_' + r)
                if ftype == SchemaColumn.NUMBER:
                    column.type = SchemaColumn.NUMBER
                elif ftype == SchemaColumn.TEXT:
                    column.type = SchemaColumn.TEXT
                funique = post.get('checkFieldUnique_' + r)
                if funique:
                    column.unique = True
                else:
                    column.unique = False
                column.full_clean()
                field_list.append(column)
            columns['fields'] = field_list
        return columns


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
    TYPE_CHOICES = (
        (TEXT, 'Text'),
        (NUMBER, 'Number')
    )

    position = models.IntegerField()
    schema_version = models.ForeignKey(SchemaVersion)
    name = models.CharField(max_length=200, blank=False)
    type = models.TextField(choices=TYPE_CHOICES, default=TEXT)
    length = models.IntegerField()
    unique = models.BooleanField(default=True)

    class Meta:
        unique_together = (("name", "schema_version"), )