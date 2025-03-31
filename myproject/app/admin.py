from django.contrib import admin
from .models import People, AdditionalData

class AdditionalDataInline(admin.StackedInline):
    model = AdditionalData
    extra = 1

@admin.register(People)
class PeopleAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number')
    search_fields = ('name', 'email', 'phone_number')
    inlines = [AdditionalDataInline]

@admin.register(AdditionalData)
class AdditionalDataAdmin(admin.ModelAdmin):
    list_display = ('people', 'type_house', 'address')
    list_filter = ('type_house',)
    search_fields = ('people__name', 'address')