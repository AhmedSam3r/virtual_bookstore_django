from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Category, Book


@admin.register(Category)
class UserCustomAdmin(admin.ModelAdmin):
    model = Category
    list_display = ('id', 'name', )
    search_fields = ('name', )
    ordering = ('id', )


class BookResourceAdmin(resources.ModelResource):
    class Meta:
        model = Book
        common_fields = ('title', 'isbn', 'author',
                         'publication_date', 'category__name',
                         'page_count', 'price', )
        fields = common_fields
        export_order = common_fields
        import_order = common_fields
        import_id_fields = ('isbn', )
        use_transactions = True
        skip_unchanged = True
        report_skipped = True


@admin.register(Book)
class BookAdmin(ImportExportModelAdmin):
    resource_class = BookResourceAdmin
    list_display = ('title', 'isbn', 'author',
                    'publication_date', 'category',
                    'page_count', 'price',
                    )
    ordering = ("id", )
    # TODO add category name
    search_fields = ('title', 'author',)
    raw_id_fields = ("category", )
    list_filter = ("publication_date", )
