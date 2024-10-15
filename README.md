# feincms3-accordion
An accordion plugin for feincms3.

**This is a toy app which serves as a proof of concept for chaining foreign keys
in a feincms3 plugin.**

**Better do not use this app unless you know what you are doing ;)**

It allows for using images and richtext mixed up inside accordion items.

## Rationale

Some CMS use tree-backed plugins which allows for nesting plugins
which in many situations comes in handy:

- gallery plugin with images
- map plugin with markers
- ...

feincms3/django-content-editor does not support this natively since plugins are
just sortable foreign keys to a base (page, article...) with admin inlines on steroids.

There are  workarounds for this shortcoming:

https://406.ch/writing/django-content-editor-now-supports-nested-sections/

https://github.com/feincms/django-content-editor/issues/29

One of them is to let the plugin hold a foreign key to a model which in turn serves
as base for child plugins. Im my experience needing more than two levels of plugin-nesting
is rarely needed, but two levels are. So I build this **experimental** accordion app
where the child plugins again hold foreign keys (to accordion items). The accordion items
then are the base for "normal" content plugins, here richtext and image,
but could be whatever you want.

With the django admin enabling adding/editing of FK models via popups you may stay on
an admin page while adding/editing accordions, accordion items and these items contents.

The select lists for accordions and accordion-items in the admin are filtered so you
can not use one of them in two places. Such reuse will rarely be wanted and would impose
the risk of inadvertently changing the ordering in another place.

Does this app make sense, is it save to use? I'm not sure, perhaps.

## Installation (if you really want)

Install the app from github with your favorite tool
```bash
python -m pip install 'feincms3-accordion @ git+https://github.com/gerlad/feincms3-accordion.git'
```
or for a quick test just copy the `accordion` folder in your project.

Add 'accordion' to `INSTALLED_APPS` in your settings file

**The following instructions assume a `standard` feincms3 module layout**

In the `page` apps `models.py` file:
```python
...
from accordion.models import AccordionBase
...
class Accordion(AccordionBase, PagePlugin):
    pass
```
Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```
In the `page` apps `admin.py` file:
```python
from accordion.admin import AccordionInlineAdmin

@admin.register(models.Page)
class PageAdmin(ContentEditor, TreeAdmin):
    ...
    inlines = [
        ...
        AccordionInlineAdmin.create(
            model=models.Accordion,
        ),
        ...
    ]

    def get_form(self, request, obj=None, **kwargs):
        # save page reference for possible filtering foreign-key plugins
        # in inline forms
        request._obj_ = obj
        return super().get_form(request, obj, **kwargs)
```
In the `page` apps `renderer.py` file:
```python
...
from .models import Accordion
...
renderer = RegionRenderer()  # already there
...
# add this
renderer.register(
    Accordion,
    template_renderer('accordion/accordion.html'),
    # or template_renderer('accordion/accordion_nojs.html'),
)
```
The included accordion in `accordion/accordion.html` relies on the `detail` element and
its `name` attribute, which enables the *exclusive* accordion behavior in main browsers.

https://developer.mozilla.org/en-US/blog/html-details-exclusive-accordions/

A polyfill for older browsers is available in `static/accordion/exclusive-accordion-polyfill.js`
```html
<script src="{% static 'accordion/exclusive-accordion-polyfill.js' %}"></script>
```
Another included accordion in `accordion/accordion_nojs.html` works with
the included styles in `static/accordion/accordion.css`
```html
<link rel="stylesheet" href="{% static 'accordion/accordion_nojs.css' %}">
```
and is a pure CSS accordion that also works without javascript, but surely
has suboptimal accessibility.

You will most probably use your own HTML/Styles though. For that to do, overwrite
accordion.html with your own template and use your own CSS.

