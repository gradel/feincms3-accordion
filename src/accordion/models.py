from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from content_editor.models import create_plugin_base, Region

from feincms3.plugins import image, richtext


class Accordion(models.Model):
    name = models.CharField(
        _('Name'),
        blank=False,
        max_length=200,
        validators=[MinLengthValidator(3)]
    )
    toggle_close = models.BooleanField(
        _('Toggle close'),
        default=False,
        help_text=_('Wether opening an item closes other open ones')
    )
    regions = [
        Region(key="items", title=_("Accordion items")),
    ]

    class Meta:
        verbose_name = _('Accordion')
        verbose_name_plural = _('Accordions')
        constraints = [
            models.UniqueConstraint(str.lower('name'), name='unique_lower_name_accordion')
        ]

    def __str__(self):
        return self.name


class AccordionBase(models.Model):
    """The page plugin, abstract, just contains link to the real accordion"""
    accordion = models.ForeignKey(
        Accordion,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='base_accordion_accordion',
        verbose_name=_('Accordion')
    )

    class Meta:
        abstract = True
        verbose_name = _('Accordion')
        verbose_name_plural = _('Accordions')

    def __str__(self):
        return self.accordion.name

    def get_items(self):
        return [
            item_link.accordion_item
            for item_link
            in self.accordion.accordion_accordionitemlink_set.order_by('ordering')
        ]


AccordionPluginBase = create_plugin_base(Accordion)


class AccordionItem(models.Model):
    heading = models.CharField(
        _('Heading'),
        blank=False,
        max_length=300,
        validators=[MinLengthValidator(2)]
    )
    regions = [
        Region(key="accordion_item_content", title=_("Accordion item content")),
    ]

    class Meta:
        verbose_name = _('Accordion item')
        verbose_name_plural = _('Accordion items')

    def __str__(self):
        return self.heading

    def get_regions(self):
        from .renderer import renderer
        regions = renderer.regions_from_item(self)
        return regions


class AccordionItemLink(AccordionPluginBase, models.Model):
    """The accordion item plugin, abstract, contains link to the real accordion item"""
    accordion_item = models.ForeignKey(
        AccordionItem,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='base_accordion_accordion_item',
        verbose_name=_('Accordion item')
    )

    class Meta:
        verbose_name = _('AccordionItem')
        verbose_name_plural = _('AccordionItems')

    def __str__(self):
        return self.accordion_item.heading


AccordionItemPluginBase = create_plugin_base(AccordionItem)


class RichText(richtext.RichText, AccordionItemPluginBase):
    pass


class Image(image.Image, AccordionItemPluginBase):
    pass
