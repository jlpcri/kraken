import time
from django.db import models


class Client(models.Model):
    """
    Model for client.

    Currently serves as essentially a folder for schemas
    """
    name = models.CharField(max_length=200, unique=True)

    def schemas(self):
        return ClientSchema.objects.filter(client=self).order_by('name')

    def __unicode__(self):
        return self.name


class ClientSchema(models.Model):
    """
    Model for schemas.

    Currently serves as essentially a folder for schema versions
    """
    name = models.CharField(max_length=200)
    client = models.ForeignKey(Client)

    class Meta:
        unique_together = (("name", "client"), )

    def versions(self):
        return SchemaVersion.objects.filter(client_schema=self).order_by('identifier')

    def __unicode__(self):
        return self.client.name + " " + self.name


class SchemaVersion(models.Model):
    """
    Model for schema versions

    Contains version identifier and delimiter. Individual field constraints for a schema version are
    SchemaColumn objects with a foreign key back to a SchemaVersion.
    """
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
        if columns.get('valid') and columns.get('fields'):
            cols = SchemaColumn.objects.filter(schema_version=self)
            cols_pks = cols.values_list('pk', flat=True)
            columns_pks = [x.pk for x in columns.get('fields')]
            for c in cols_pks:
                if c not in columns_pks:
                    SchemaColumn.objects.get(pk=c).delete()
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
                    cid = post.get('hiddenFieldId_' + r)
                    if cid:
                        column = SchemaColumn.objects.get(pk=cid)
                    else:
                        column = SchemaColumn()
                    column.position = i+1
                    column.name = post.get('inputFieldName_' + r)
                    column.length = post.get('inputFieldLength_' + r)
                    column.schema_version = self
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
                    field_list.append(column)
                    column.full_clean()
                except Exception as e:
                    if columns['valid']:
                        columns['valid'] = False
                        columns['error_message'] = 'Custom Fields contain errors'
            columns['fields'] = field_list
            return columns
        return {'valid': None, 'error_message': None, 'fields': None}


def version_file_location(instance, filename):
    return "{0}_{1}".format(str(time.time()).replace('.', ''), filename)


class VersionFile(models.Model):
    name = models.CharField(max_length=200, blank=False)
    schema_version = models.ForeignKey(SchemaVersion)
    last_opened = models.DateTimeField('last opened', auto_now=True)
    contents = models.FileField(upload_to=version_file_location)

    class Meta:
        unique_together = (("name", "schema_version"), )

    @property
    def file_contents(self):
        f = self.contents
        f.open(mode='rb')
        lines = f.readlines()
        data = ''
        for line in lines:
            data += line
        f.close()

        return data


class FileColumn(models.Model):
    NUMBER = 'Number'
    TEXT = 'Text'
    CUSTOM_LIST = 'Custom List'
    FIRST_NAME = 'First Name'
    LAST_NAME = 'Last Name'
    ADDRESS = 'Address'
    ZIP_CODE = 'ZIP Code'
    GENERATOR_CHOICES = (
        (TEXT, 'Text'),
        (NUMBER, 'Number'),
        (CUSTOM_LIST, 'Custom List'),
        (FIRST_NAME, 'First Name'),
        (LAST_NAME, 'Last Name'),
        (ADDRESS, 'Address'),
        (ZIP_CODE, 'ZIP Code')
    )
    NUMBER_GENERATOR_CHOICES = (
        (NUMBER, 'Number'),
        (CUSTOM_LIST, 'Custom List'),
        (ZIP_CODE, 'ZIP Code')
    )

    version_file = models.ForeignKey('VersionFile')
    schema_column = models.ForeignKey('SchemaColumn')
    generator = models.TextField(choices=GENERATOR_CHOICES, default=TEXT)
    payload = models.TextField()  # JSON objects defining options for chosen generator

    class Meta:
        unique_together = (("version_file", "schema_column"), )


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