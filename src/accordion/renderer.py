from django.utils.safestring import mark_safe

from feincms3.renderer import RegionRenderer, template_renderer

from .models import Image, RichText


renderer = RegionRenderer()
renderer.register(
    RichText,
    template_renderer('plugins/richtext.html', lambda plugin, context: context.update({
        'plugin': plugin,
        'html': mark_safe(plugin.text)
    }))
)
renderer.register(
    Image,
    template_renderer('image.html'),
)
