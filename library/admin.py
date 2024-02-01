from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget

from .models import Book, Code, Uploader, Tag, Folder


admin.site.register(Code)
admin.site.register(Tag)
admin.site.register(Uploader)
admin.site.register(Folder)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
