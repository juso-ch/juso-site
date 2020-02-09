from django.contrib import admin

from feincms3.admin import TreeAdmin
from juso.sections.models import Section, Category
# Register your models here.


@admin.register(Section)
class SectionAdmin(TreeAdmin):
    list_display = [
        "indented_title",
        "move_column",
        "name",
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
