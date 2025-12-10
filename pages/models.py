from django.db import models
from django.utils.translation import gettext_lazy as _

class ExpertiseCard(models.Model):
    title = models.CharField(_("Title"), max_length=200)
    image = models.ImageField(_("Image"), upload_to='expertise/')
    short_description = models.TextField(_("Short Description"))
    full_content = models.TextField(_("Full Content"), help_text=_("HTML content allowed"))
    order = models.PositiveIntegerField(_("Order"), default=0)
    is_active = models.BooleanField(_("Active"), default=True)

    class Meta:
        verbose_name = _("Expertise Card")
        verbose_name_plural = _("Expertise Cards")
        ordering = ['order']

    def __str__(self):
        return self.title


class Service(models.Model):
    title = models.CharField(_("Title"), max_length=200)
    description = models.TextField(_("Description"))
    order = models.PositiveIntegerField(_("Order"), default=0)
    is_active = models.BooleanField(_("Active"), default=True)

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")
        ordering = ['order']

    def __str__(self):
        return self.title


class ProtectionStandard(models.Model):
    title = models.CharField(_("Title"), max_length=200)
    description = models.TextField(_("Description"))
    order = models.PositiveIntegerField(_("Order"), default=0)
    is_active = models.BooleanField(_("Active"), default=True)

    class Meta:
        verbose_name = _("Protection Standard")
        verbose_name_plural = _("Protection Standards")
        ordering = ['order']

    def __str__(self):
        return self.title


class LegalDocument(models.Model):
    title = models.CharField(_("Title"), max_length=200)
    slug = models.SlugField(_("Slug"), unique=True)
    content = models.TextField(_("Content"), help_text=_("HTML content allowed"))
    is_active = models.BooleanField(_("Active"), default=True)

    class Meta:
        verbose_name = _("Legal Document")
        verbose_name_plural = _("Legal Documents")

    def __str__(self):
        return self.title

