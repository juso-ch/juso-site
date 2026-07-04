"""Render a spread of real, active URLs through the full request stack.

This is the primary regression check for the Django/feincms3 upgrade: it
exercises page/blog/event rendering (feincms3 regions, plugins, templates,
per-site template loading) against whatever data is in the connected database.
Point it at a restored production dump to confirm a new stack still renders the
real content.

Usage:
    python manage.py smoke_urls                 # sample across all sites
    python manage.py smoke_urls --per-site 5    # more pages per site
    python manage.py smoke_urls --fail-on 500   # only fail on server errors

Exit code is non-zero if any checked URL returns a status >= the threshold
(default 500), so it is CI-friendly.
"""
from django.core.management.base import BaseCommand
from django.test import Client, override_settings

# A local-memory cache keeps the smoke run self-contained: it does not need the
# production memcached to be reachable, and caching does not affect whether a
# page renders correctly (only performance / cache-specific bugs).
_LOCMEM_CACHES = {
    "default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}
}


class Command(BaseCommand):
    help = "Fetch a sample of real active URLs and report their status codes."

    def add_arguments(self, parser):
        parser.add_argument("--per-site", type=int, default=3,
                            help="Max pages to check per site (default 3).")
        parser.add_argument("--fail-on", type=int, default=500,
                            help="Fail if any status >= this value (default 500).")
        parser.add_argument("--articles", type=int, default=10,
                            help="Number of blog articles to check (default 10).")
        parser.add_argument("--events", type=int, default=10,
                            help="Number of events to check (default 10).")

    @override_settings(CACHES=_LOCMEM_CACHES)
    def handle(self, *args, **opts):
        # Imported here so the command module loads even mid-migration.
        from juso.pages.models import Page

        client = Client()
        checks = []  # (host, url, label)

        # Pages: the site root plus a spread of deeper pages, grouped by site.
        # NB: Page.objects.active() filters by current_site(), which is None
        # outside a request, so we filter on is_active directly here. The real
        # site is resolved by feincms3_sites middleware from the Host header.
        site_seen = {}
        pages = (Page.objects.with_tree_fields()
                 .filter(is_active=True)
                 .select_related("site")
                 .order_by("site_id", "position", "path"))
        for page in pages:
            site = page.site
            host = getattr(site, "host", "") or "testserver"
            # host may be a regex-ish pattern like "jusosg.ch/stadtsg"; the part
            # before the first slash is a usable Host header.
            host = host.split("/")[0]
            count = site_seen.get(site.pk, 0)
            if count >= opts["per_site"]:
                continue
            site_seen[site.pk] = count + 1
            checks.append((host, page.path, f"page[{site.pk}] {page.path}"))

        checks += self._collect("juso.blog.models", "Article",
                                opts["articles"], "article")
        checks += self._collect("juso.events.models", "Event",
                                opts["events"], "event")

        failures, errors, ok = [], [], 0
        for host, url, label in checks:
            try:
                resp = client.get(url, HTTP_HOST=host, follow=True)
                status = resp.status_code
            except Exception as exc:  # noqa: BLE001 - report, don't crash the run
                errors.append((label, host, url, repr(exc)))
                self.stderr.write(self.style.ERROR(f"ERR  {host}{url}  {exc!r}"))
                continue
            line = f"{status} {host}{url}  ({label})"
            if status >= opts["fail_on"]:
                failures.append((label, host, url, status))
                self.stderr.write(self.style.ERROR(line))
            elif status >= 400:
                self.stdout.write(self.style.WARNING(line))
                ok += 1
            else:
                self.stdout.write(line)
                ok += 1

        self.stdout.write("")
        self.stdout.write(
            f"checked={len(checks)} ok/redirect/4xx={ok} "
            f"failures(>={opts['fail_on']})={len(failures)} errors={len(errors)}")
        if failures or errors:
            self.stderr.write(self.style.ERROR("SMOKE TEST FAILED"))
            raise SystemExit(1)
        self.stdout.write(self.style.SUCCESS("SMOKE TEST PASSED"))

    def _collect(self, module_path, model_name, limit, label):
        """Best-effort collection of get_absolute_url() for a content model."""
        from importlib import import_module
        out = []
        try:
            model = getattr(import_module(module_path), model_name)
            # Avoid .active() (site-scoped); filter on is_active when present.
            field_names = {f.name for f in model._meta.get_fields()}
            qs = (model.objects.filter(is_active=True)
                  if "is_active" in field_names else model.objects.all())
            for obj in qs[:limit]:
                try:
                    url = obj.get_absolute_url()
                except Exception:  # noqa: BLE001
                    continue
                host = "testserver"
                site = getattr(obj, "site", None)
                if site is not None and getattr(site, "host", ""):
                    host = site.host.split("/")[0]
                out.append((host, url, f"{label} {obj.pk}"))
        except Exception as exc:  # noqa: BLE001
            self.stderr.write(f"(skipped {label}s: {exc!r})")
        return out
