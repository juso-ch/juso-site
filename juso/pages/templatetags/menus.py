from collections import defaultdict
from django import template
from juso.pages.models import Page


register = template.Library()


@register.simple_tag
def all_menus():
    menus = defaultdict(list)
    pages = Page.objects.with_tree_fields().exclude(
        is_active=False,
        menu=""
    ).extra(
        where=["tree_depth<=1"]
    )

    for page in pages:
        menus[page.menu].append(page)
    return menus


@register.filter
def group_by_tree(iterable):
    parent = None
    children = []

    depth = -1

    for element in iterable:
        if parent is None or element.tree_depth == depth:
            if parent:
                yield parent, children
                parent = None
                children = []
            parent = element
            depth = element.tree_depth
        else:
            children.append(element)
    if parent:
        yield parent, children
