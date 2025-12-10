from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import ExpertiseCard, Service, ProtectionStandard, LegalDocument

@admin.register(ExpertiseCard)
class ExpertiseCardAdmin(TranslationAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'short_description')

@admin.register(Service)
class ServiceAdmin(TranslationAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'description')

@admin.register(ProtectionStandard)
class ProtectionStandardAdmin(TranslationAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')


@admin.register(LegalDocument)
class LegalDocumentAdmin(TranslationAdmin):
    list_display = ('title', 'slug', 'is_active')
    list_editable = ('is_active',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'description')

