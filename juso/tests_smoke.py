"""Self-contained smoke tests that run without production data.

These are the CI safety net for the Django/feincms3 upgrade. They do not touch
real content; they boot the stack, walk every registered admin, and exercise a
minimal request. The data-backed rendering check lives in the
``smoke_urls`` management command (run against a restored dump).
"""
from django.contrib.admin.sites import site as admin_site
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

_LOCMEM_CACHES = {
    "default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}
}


@override_settings(CACHES=_LOCMEM_CACHES)
class AdminSmokeTest(TestCase):
    """Load the admin index, changelist and add-form for every model.

    Django/feincms3 upgrades most often break in the admin (form widgets,
    list_display callables, inlines). Hitting every registered admin surfaces
    those regressions without needing any content in the database.
    """

    @classmethod
    def setUpTestData(cls):
        # feincms3_sites middleware resolves a Site from the Host header on
        # every request; without a default site even the admin returns 500.
        from feincms3_sites.models import Site
        Site.objects.create(
            host="testserver", is_default=True, is_active=True,
            default_language="de")
        cls.user = get_user_model().objects.create_superuser(
            username="smoke", email="smoke@example.com", password="smoke-pass")

    def setUp(self):
        self.client.force_login(self.user)

    def test_admin_index(self):
        self.assertEqual(self.client.get(reverse("admin:index")).status_code, 200)

    def test_admin_changelists_and_add_forms(self):
        failures = []
        for model, model_admin in admin_site._registry.items():
            info = (model._meta.app_label, model._meta.model_name)
            try:
                url = reverse("admin:%s_%s_changelist" % info)
            except Exception as exc:  # noqa: BLE001
                failures.append(f"reverse changelist {info}: {exc!r}")
                continue
            resp = self.client.get(url)
            if resp.status_code != 200:
                failures.append(f"changelist {info} -> {resp.status_code}")
            # Add-form: only where the admin permits adding.
            if model_admin.has_add_permission(self._request()):
                try:
                    add_url = reverse("admin:%s_%s_add" % info)
                    resp = self.client.get(add_url)
                    # 403 is acceptable (some models block add via other hooks).
                    if resp.status_code not in (200, 403):
                        failures.append(f"add {info} -> {resp.status_code}")
                except Exception as exc:  # noqa: BLE001
                    failures.append(f"add {info}: {exc!r}")
        self.assertEqual(failures, [], "\n".join(failures))

    def _request(self):
        from django.test import RequestFactory
        req = RequestFactory().get("/admin/")
        req.user = self.user
        return req


@override_settings(CACHES=_LOCMEM_CACHES)
class MigrationsStateTest(TestCase):
    """Fail loudly if models and migrations have drifted apart."""

    def test_no_missing_migrations(self):
        from django.core.management import call_command
        # Raises SystemExit(1) if makemigrations would create anything.
        call_command("makemigrations", "--check", "--dry-run", verbosity=0)
