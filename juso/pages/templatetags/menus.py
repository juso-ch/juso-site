from collections import defaultdict

from django import template

from juso.pages.models import Page

register = template.Library()


@register.simple_tag
def top_page(page):
    if page.ancestors().count() > 0:
        return page.ancestors()[0]
    return page


@register.simple_tag
def all_menus(language_code, top_page):
    menus = defaultdict(list)
    pages = top_page.descendants().with_tree_fields().exclude(
        is_active=False,
        menu=""
    ).filter(
        language_code=language_code
    ).extra(
        where=["tree_depth>=1 and tree_depth<=2"]
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
