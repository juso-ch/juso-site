from django.template.loaders import filesystem
from feincms3_sites.middleware import current_site


class SiteTemplateLoader(filesystem.Loader):
    def __init__(self, engine, dirs=None, template_names=None):
        super().__init__(engine)
        self.dirs = dirs
        self.template_names = template_names

    def get_template_sources(self, template_name):
        if self.template_names and template_name not in self.template_names:
            return super().get_template_sources(template_name)
        return super().get_template_sources(
            f"{current_site().host}/{template_name}")
