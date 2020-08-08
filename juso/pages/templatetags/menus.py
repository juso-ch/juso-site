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
def button_menu(language_code, top_page):
    pages = (
        top_page.descendants()
        .exclude(is_active=False,)
        .filter(menu="buttons", language_code=language_code)
    )

    return pages


@register.simple_tag
def all_menus(language_code, top_page):
    menus = defaultdict(list)
    pages = (
        top_page.descendants()
        .with_tree_fields()
        .exclude(is_active=False, menu="")
        .filter(language_code=language_code)
    )

    for page in pages:
        menus[page.menu].append(page)

    return menus


@register.filter
def group_by_tree(iterable):

    iterable = sorted(iterable, key=lambda p: p.position)

    for element in iterable:
        yield element, sorted(element.children.all(), key=lambda p: p.position)


@register.filter
def order_by_position(iterable):
    return sorted(iterable, key=lambda p: p.position)
