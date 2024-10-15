from django.db.models import Q
from django.contrib import admin

from content_editor.admin import (
    ContentEditor,
    ContentEditorInline,
)
from feincms3.plugins import image, richtext

from .models import (
    Accordion,
    AccordionItem,
    AccordionItemLink,
    Image,
    RichText,
)

accordion_button = """<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e8eaed"><path d="M880-720v480q0 33-23.5 56.5T800-160H160q-33 0-56.5-23.5T80-240v-480q0-33 23.5-56.5T160-800h640q33 0 56.5 23.5T880-720Zm-720 80h640v-80H160v80Zm0 160v240h640v-240H160Zm0 240v-480 480Z"/></svg>"""


class AccordionItemLinkInline(ContentEditorInline):
    button = accordion_button
    fieldsets = [
        (None, {
            'fields': (
                'accordion_item',
                'region', 'ordering',
            ),
        }),
    ]
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):

        field = super().formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.name == 'accordion_item':

            if request._obj_ is not None:
                field.queryset = field.queryset.filter(
                    Q(base_accordion_accordion_item__parent=request._obj_)
                    | Q(base_accordion_accordion_item__parent__isnull=True)
                )
            else:
                field.queryset = field.queryset.filter(
                    base_accordion_accordion_item__parent__isnull=True
                )

        return field

    def get_formset(self, request, obj=None, **kwargs):
       # just save obj reference for future processing in `formfield_for_foreignkey`
       request._obj_ = obj
       formset = super().get_formset(request, obj, **kwargs)
       return formset


@admin.display(description='plugged in')
def accordion_parent(obj):
    return ', '.join(
        str(base_accordion.parent)
        for base_accordion
        in obj.base_accordion_accordion.all()
    ) or '------'


@admin.register(Accordion)
class AccordionAdmin(ContentEditor, admin.ModelAdmin):
    list_filter = ('base_accordion_accordion__parent',)
    list_display = ('name', accordion_parent,)
    inlines = [
        AccordionItemLinkInline.create(
            model=AccordionItemLink,
            button = accordion_button
        ),
    ]


@admin.display(description='plugged in')
def accordion_item_parent(obj):
    return ', '.join(
        str(base_accordion_item.parent)
        for base_accordion_item
        in obj.base_accordion_accordion_item.all()
    ) or '------'


@admin.register(AccordionItem)
class AccordionItemAdmin(ContentEditor, admin.ModelAdmin):
    list_filter = ('base_accordion_accordion_item__parent',)
    list_display = ('heading', accordion_item_parent,)
    inlines = [
        richtext.RichTextInline.create(model=RichText),
        image.ImageInline.create(model=Image),
    ]


class AccordionInlineAdmin(ContentEditorInline):
    button = accordion_button
    fieldsets = [
        (None, {
            'fields': (
                'accordion',
                'region', 'ordering',
            ),
        }),
    ]
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):

        field = super().formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.name == 'accordion' and hasattr(request, '_obj_'):
            if request._obj_ is not None:
                field.queryset = field.queryset.filter(
                    Q(base_accordion_accordion__parent=request._obj_)
                    | Q(base_accordion_accordion__parent__isnull=True)
                )
            else:
                field.queryset = field.queryset.filter(
                    base_accordion_accordion__parent__isnull=True
                )
        return field
