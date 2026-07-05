from collections import defaultdict

from django import template

from juso.pages.models import Page

register = template.Library()


@register.simple_tag
def top_page(page):
    # Topmost ancestor (root) in a single query, or the page itself if it is
    # already top-level.
    return page.ancestors().first() or page


@register.simple_tag
def button_menu(language_code, top_page):
    pages = (top_page.descendants().exclude(is_active=False, ).filter(
        menu="buttons", language_code=language_code))

    return pages


@register.simple_tag
def all_menus(language_code, top_page):
    menus = defaultdict(list)

    # prefetch children so group_by_tree's per-item children.all() in the nav
    # templates doesn't issue a query per top-level menu entry (N+1).
    pages = (top_page.descendants().with_tree_fields().exclude(
        is_active=False, menu="").filter(
            language_code=language_code).prefetch_related("children"))

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
