from django.contrib import admin

from main.models import Customer
from main.models import Storage, Box, Status, Rent, Image, UtmMark


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'date_joined')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    search_fields = [
        'storage',
        'image',
    ]
    list_display = [
        'storage',
        'image',
    ]
    raw_id_fields = [
        'storage',
    ]


class ImageInline(admin.TabularInline):
    model = Image
    extra = 0


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    search_fields = [
        'title',
        'phone',
        'email',
        'city',
        'address',
    ]
    list_display = [
        'title',
        'phone',
        'email',
        'city',
        'address',
    ]
    inlines = [
        ImageInline
    ]


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    search_fields = [
        'title',
        'storage',
        'price',
    ]
    list_display = [
        'title',
        'storage',
        'price',
        'floor',
        'length',
        'weigth',
        'heigth',
    ]
    raw_id_fields = [
        'storage',
    ]


@admin.register(Rent)
class RentAdmin(admin.ModelAdmin):
    search_fields = [
        'renter',
        'box',
        'status',
    ]
    list_display = [
        'renter',
        'box',
        'status',
        'start_date',
        'end_date',
    ]
    raw_id_fields = [
        'renter',
        'box',
        'status',
    ]


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    search_fields = [
        'title',
    ]
    list_display = [
        'title',
    ]


@admin.register(UtmMark)
class UtmMarkAdmin(admin.ModelAdmin):
    search_fields = [
        'url',
    ]
    list_display = [
        'url',
        'count',
    ]