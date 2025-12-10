from modeltranslation.translator import register, TranslationOptions
from .models import ExpertiseCard, Service, ProtectionStandard, LegalDocument

@register(ExpertiseCard)
class ExpertiseCardTranslationOptions(TranslationOptions):
    fields = ('title', 'short_description', 'full_content')

@register(Service)
class ServiceTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

@register(ProtectionStandard)
class ProtectionStandardTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(LegalDocument)
class LegalDocumentTranslationOptions(TranslationOptions):
    fields = ('title', 'content')
