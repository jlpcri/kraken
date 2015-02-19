import time
from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def schemas(self):
        return ClientSchema.objects.filter(client=self)

    def __unicode__(self):
        return self.name


class ClientSchema(models.Model):
    name = models.CharField(max_length=200)
    client = models.ForeignKey(Client)

    class Meta:
        unique_together = (("name", "client"), )

    def versions(self):
        return SchemaVersion.objects.filter(client_schema=self)

    def __unicode__(self):
        return self.client.name + " " + self.name


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

    def __unicode__(self):
        return unicode(self.client_schema) + u", " + self.identifier

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

    def get_columns(self, position_order=False):
        """
        Gets a ModelSet of columns from VersionColumn associated with this ClientVersion
        Receives:   position_order (True or False) default (False)
        Returns:    ModelSet
        """
        if position_order:
            return SchemaColumn.objects.filter(schema_version=self).order_by('position')
        return SchemaColumn.objects.filter(schema_version=self)

    def save_columns(self, columns={}):
        """
        Saves ModelSet of columns to database
        Receives:   columns (dict) default (empty dict)
        Returns:    dict
        """
        if columns.get('valid'):
            for c in columns.get('fields'):
                c.save()
        return columns

    def validate_columns(self, post):
        """
        Populates list of VersionColumn models from fields in form inside Schema Editor template
                and validates columns using model.full_clean()
        Receives:   request.POST
        Returns:    dict
        """
        columns = {'valid': True, 'error_message': None, 'fields': None}
        row_order = post.get('row_order', '').strip()
        field_list = []
        if row_order:
            row_order = row_order.strip().split(' ')
            for i, r in enumerate(row_order):
                try:
                    print 'aaa'
                    cid = post.get('hiddenFieldId_' + r)
                    print type(cid)
                    if cid:
                        print 'check a'
                        column = SchemaColumn.objects.get(pk=cid)
                    else:
                        print 'check b'
                        column = SchemaColumn()
                    print 'bbb'
                    column.position = i+1
                    print 'ccc'
                    column.name = post.get('inputFieldName_' + r)
                    print 'ddd'
                    column.length = post.get('inputFieldLength_' + r)
                    print 'eee'
                    column.schema_version = self
                    print 'fff'
                    ftype = post.get('selectFieldType_' + r)
                    print 'ggg'
                    if ftype == SchemaColumn.NUMBER:
                        column.type = SchemaColumn.NUMBER
                    elif ftype == SchemaColumn.TEXT:
                        column.type = SchemaColumn.TEXT
                    print 'hhh'
                    funique = post.get('checkFieldUnique_' + r)
                    print 'iii'
                    if funique:
                        column.unique = True
                    else:
                        column.unique = False
                    print 'jjj'
                    print column
                    field_list.append(column)
                    column.full_clean()
                except Exception as e:
                    if columns['valid']:
                        columns['valid'] = False
                        columns['error_message'] = 'Custom Fields contain errors'
            columns['fields'] = field_list
            print field_list
            return columns
        return {'valid': None, 'error_message': None, 'fields': None}


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

    def __unicode__(self):
        return unicode(self.schema_version) + u" - {0}: {1}".format(self.position, self.name)

    class Meta:
        unique_together = (("name", "schema_version"), )