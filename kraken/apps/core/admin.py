from django.contrib import admin
from models import Client, ClientSchema, SchemaVersion, VersionFile, FileColumn, SchemaColumn

for m in [Client, ClientSchema, SchemaVersion, VersionFile, FileColumn, SchemaColumn]:
    admin.site.register(m)
