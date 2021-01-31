from collections import defaultdict
from io import BytesIO

import requests
from dateutil import parser
from django.core import files
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify
from feincms3.cleanse import cleanse_html
from langdetect import detect
from lxml import etree

from juso.blog.models import Article, RichText, WPImport


def get_image(thumbnail):
    if thumbnail is None:
        return None

    url = thumbnail.find("guid").text
    request = requests.get(url, stream=True)

    if request.status_code != requests.codes.ok:
        return None

    f = BytesIO()
    f.write(request.content)
    return url.split("/")[-1], f


class Command(BaseCommand):
    help = "Executes the specified import"

    def add_arguments(self, parser):
        parser.add_argument("import_slugs", nargs="+", type=str)

    def handle(self, *args, **options):
        for import_slug in options["import_slugs"]:
            try:
                wp_import = WPImport.objects.get(slug=import_slug)
            except WPImport.DoesNotExist:
                raise CommandError('Poll "%s" does not exist' % import_slug)
            tree = etree.parse(wp_import.import_file)
            root = tree.getroot()
            items = root.xpath("//channel/item")

            indexed_posts = defaultdict(lambda: None)

            for post in tree.findall(
                    "channel/item/{http://wordpress.org/export/1.2/}post_id"):
                pid = post.text
                indexed_posts[pid] = post.getparent()

            for item in items:
                post_type = item.find(
                    "{http://wordpress.org/export/1.2/}post_type")
                if post_type.text != "post":
                    continue

                title = item.find("title").text
                content = item.find(
                    "{http://purl.org/rss/1.0/modules/content/}encoded").text
                if len(content) < 400 or item.find("pubDate").text is None:
                    continue
                pub_date = parser.parse(item.find("pubDate").text)
                language = detect(content)
                categories = [
                    i.get("nicename") for i in item.findall("category")
                ]
                namespace = wp_import.default_namespace
                if wp_import.mappings.filter(nicename__in=categories).exists():
                    namespace = wp_import.mappings.filter(
                        nicename__in=categories)[0].target
                thumbnail = None
                for meta in item.findall(
                        "{http://wordpress.org/export/1.2/}postmeta"):
                    if (meta.find("{http://wordpress.org/export/1.2/}meta_key"
                                  ).text == "_thumbnail_id"):
                        thumbnail = indexed_posts[meta.find(
                            "{http://wordpress.org/export/1.2/}meta_value").
                                                  text]
                try:
                    article = Article.objects.create(
                        title=title,
                        slug=slugify(title)[:180],
                        publication_date=pub_date,
                        namespace=namespace,
                        language_code=language,
                        section=wp_import.section,
                    )
                except:
                    print("Failed to create post")
                    continue

                try:
                    image = get_image(thumbnail)
                except Exception as e:
                    print(e)

                if image is not None:
                    try:
                        print(image[0])
                        article.header_image.save(image[0],
                                                  files.File(image[1]))
                    except Exception as e:
                        print(e)

                if "<p>" not in content:
                    content = content.replace("\n", "<br/>")

                content = RichText.objects.create(
                    parent=article,
                    text=cleanse_html("<p>" + content + "</p>"),
                    region="main",
                )
                print(f"Article {title} imported!")
