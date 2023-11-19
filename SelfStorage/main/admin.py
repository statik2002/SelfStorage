from django.contrib import admin

from main.models import Customer, CallBackOrder, CallBackOrderStatus
from main.models import Storage, Box, Status, Rent, Image, UtmMark, Order, City, RemindDay
from main.utils import export_to_csv


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


@admin.register(CallBackOrder)
class CallBackOrderAdmin(admin.ModelAdmin):
    pass


@admin.register(CallBackOrderStatus)
class CallBackOrderStatusAdmin(admin.ModelAdmin):
    pass


class ImageInline(admin.TabularInline):
    model = Image
    extra = 0


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    search_fields = [
        'title',
        'phone',
        'email',
        'city_name',
        'address',
    ]
    list_display = [
        'title',
        'phone',
        'email',
        'city',
        'address',
    ]
    raw_id_fields = [
        'city_name',
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
    list_filter = [
        'status'
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
    list_display = ('utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'link_counter')

    fields = ('utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'link_counter')

    readonly_fields = ('utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'link_counter')

    actions = [export_to_csv]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    search_fields = [
        'user',
        'box',
        'status',
    ]
    list_display = [
        'user',
        'box',
        'start_date',
        'end_date',
        'status',
        'delivery',
        'loaders',
    ]
    raw_id_fields = [
        'user',
        'box',
        'status',
    ]


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    search_fields = [
        'name',
    ]
    list_display = [
        'name',
    ]


@admin.register(RemindDay)
class RemindDayAdmin(admin.ModelAdmin):
    list_display = ('day', 'status')
