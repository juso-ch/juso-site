# Upgrade: Python 3.8 / Django 3.2 → Python 3.13 / Django 5.2 LTS

Staged, no-data-loss upgrade. Each phase is independently deployable; the test
suite gates every step.

## Target
Python 3.13 · Django 5.2 LTS · Postgres 17 · psycopg 3 (landing zone: 5.2 LTS,
supported to April 2028).

## Safety net (Phase 0 — done)
- `juso/tests_smoke.py` — self-contained tests (no prod data needed): boots the
  stack, walks every admin changelist + add-form, checks migration/model sync.
  Run: `python manage.py test juso.tests_smoke`
- `juso/management/commands/smoke_urls.py` — renders a spread of **real** active
  page/blog/event URLs through the full feincms3 stack against a restored dump.
  Run: `python manage.py smoke_urls --per-site 3` (exit non-zero on any 5xx).
  Baseline on Django 3.2: **131/131 URLs → HTTP 200.**
- `.github/workflows/test.yml` — CI runs checks + migrations + tests on Postgres.

### Local validation environment
```
# Postgres 12 (prod parity) with a restored dump:
docker run -d --name juso-pg12 -e POSTGRES_USER=juso -e POSTGRES_PASSWORD=juso \
  -e POSTGRES_DB=juso -p 127.0.0.1:5433:5432 postgres:12-alpine
docker exec -i juso-pg12 pg_restore -U juso -d juso --no-owner --no-privileges < juso-prod.dump

# env for manage.py against that DB:
export SQL_ENGINE=django.db.backends.postgresql POSTGRES_DB=juso POSTGRES_USER=juso \
  POSTGRES_PASSWORD=juso SQL_HOST=127.0.0.1 SQL_PORT=5433 DEBUG=0 \
  SECRET_KEY=k ALLOWED_HOSTS="*"
```

## Findings while building the safety net
- **Migration drift (pre-existing):** models had uncommitted changes (verbose_name
  tweaks + one index). Captured as migrations `blog/0060`, `events/0060`,
  `forms/0051`, `pages/0091`, `testimonials/0009`. All are state-only except the
  pages index.
- **`pages_page_is_acti_4365f3_idx` exists in prod but had no migration** — the
  index was created outside migration history. `pages/0091` creates it
  idempotently (`CREATE INDEX IF NOT EXISTS`) so it is safe on prod and fresh DBs.
- **Latent admin bug (fixed):** `get_form` in blog/events/forms/link_collections/
  pages admins did `sections[0]` / `Site.objects.filter(...)[0]`, which 500s when
  the editor has no sections. Guarded — behavior unchanged when sections exist.

## Phase 1 — cleanup on Django 3.2 (done)
- Removed unused `django-fobi` + `django-taggit-templatetags`; recompiled
  requirements dropped 13 orphaned transitives (django-nine, django-nonefield,
  vishap, easy-thumbnails, reportlab, svglib, unidecode, …). Django stays 3.2.15.
- **`bleach` re-added as an explicit dep** — it is imported directly in
  people/events models but was only present as a fobi transitive.
- `ugettext`→`gettext` (people/admin.py); removed the `postgres…jsonb.JSONField`
  import from `webpush/migrations/0001` (would crash migrate on Django 4.0);
  `pytz`→`zoneinfo.ZoneInfo` (events/models.py). Verified no migration drift.
- **`USE_L10N` kept for now** — on 3.2 the global default is False, so removing it
  here would flip localized formatting off. Removed in Phase 2 (no-op on Django 4).
- Docker base → `python:3.10-bookworm`, `netcat`→`netcat-traditional` (both
  Dockerfiles). NB: needs a `docker build` smoke on CI/host before deploy.
- Validated on the prod dump: 131/131 URLs → 200, admin suite green, no drift.

## Phase 2 — Django 3.2 → 4.2 LTS (done)
Key result: **the feincms3 stack (feincms3 0.38.1, content-editor 6.0,
tree-queries 0.7, imagefield 0.14, js-asset 1.2.2, ckeditor 6.2) runs unchanged
on Django 4.2** — 131/131 real URLs render. So it stays pinned; only Django and
the independent packages moved. Full ecosystem upgrade is Phase 3.

- Django → 4.2.30. Bumps: django-su 1.0 (0.9 used a Django-1.6-era import),
  reversion 5.1, debug-toolbar 4.4, simple-captcha 0.6.3, sekizai 4.1,
  celery 5.3.6, celery-results 2.5.1, redis 5.3, gunicorn 23 (CVE-2024-1135),
  uvicorn 0.50 + **uvicorn-worker** (uvicorn.workers removed), html-sanitizer 2.6,
  pywebpush 2.3, Pillow 10.4, taggit 5.0.1, flat-json-widget 0.4.
- `docker-compose.prod.yml`: worker class → `uvicorn_worker.UvicornH11Worker`.
- Settings: removed `USE_L10N` (no-op on 4.x); added env-driven
  `CSRF_TRUSTED_ORIGINS` (Django 4.0 Origin checks).
- **html-sanitizer 2.x fix:** `HTML_SANITIZERS["default"]["attributes"]["table"]`
  was `("summary")` — a bare string (1.x silently split it into chars). Now
  `("summary",)`. 2.x validates it must be a collection.
- **taggit 5.0.1 migrations 0004–0006** applied to the prod copy (0006 renames an
  index; 0004/0005 metadata). No duplicate tags/items → constraints held.
- **7 metadata-only app migrations** generated (translations/parent FK
  `related_name` state churn from Django 4.x); each produces 0 chars of SQL.
- **Historical-migration fix (blog):** `0010/0018/0034` referenced
  `to="events.NameSpace"`, a model deleted in `events/0050`. Django 4.2 renders
  migration state eagerly, so `blog/0050` (which removes that field *after* the
  model was deleted) failed on fresh DB builds. Repointed to the always-present
  `blog.NameSpace` (data-irrelevant: the field is add-then-removed). events/pages
  references resolve on their own and were left untouched.
- Validated on prod dump: 131/131 URLs 200, admin suite green, no drift, row
  counts identical to baseline (only transient captcha challenge rows differ).

### Still TODO before deploying Phase 2
- `docker build -f Dockerfile.prod .` smoke on CI/host (base image + compilemessages
  + gunicorn/uvicorn_worker boot) — not runnable in this analysis env.
- Bump prod Postgres 12 → a supported major is deferred to Phase 5, but note PG12
  is EOL; schedule it.

## Phase 3 — feincms3 lockstep upgrade (done, branch upgrade/phase-3-feincms3)
feincms3 0.38→5.6, content-editor 6→9, sites 0.11→0.21.3, tree-queries 0.7→0.24,
js-asset 1→4, imagefield 0.14→0.22, admin-ordering→0.20. Validated on the dump:
131/131 URLs render, admin suite green, no drift, row counts identical.

- **Rich text:** `CleansedRichTextField` moved to `feincms3.cleanse` (was
  `feincms3.plugins.richtext`); split imports in people/glossary/pages models.
- **Renderer:** `TemplatePluginRenderer` → `RegionRenderer` (4 renderer.py); the
  `register_string_renderer` shim still works. `Regions.from_item(x, renderer=r,
  …)` → `r.regions_from_item(x, …)` across 21 view call sites.
- **Page types (data migration `pages/0093`):** Page `AppsMixin`+`TemplateMixin`
  → `PageTypeMixin`; `APPLICATIONS`+`TEMPLATES` → one `TYPES` list of
  `TemplateType`/`ApplicationType`. `template_key`+`application` → `page_type`
  (backfilled: application key if set, else template key); `app_instance_namespace`
  → `app_namespace` (renamed, data preserved). `page.template.template_name` →
  `page.type.template_name`. Backfill verified against real data.
- **feincms3-sites 0.21:** requires `("site","path")` in `unique_together`
  (replaced the named UniqueConstraint). `site` is now a dynamically-added
  `SiteForeignKey`, so it can't appear in `Meta.indexes`; the two site-indexes
  were dropped (unique_together covers path+site lookups). Added
  `ordering=["position"]` (feincms3.W001).
- **tree-queries 0.24** must be in `INSTALLED_APPS`. Its `TreeAdmin.changelist_view`
  clashes with django-reversion's positional `super()` call — bridged with
  `ReversionTreeAdminCompat` mixin (juso/utils.py) placed after VersionAdmin.
- Admin: `application`/`template_key`/`app_instance_namespace` fields → `page_type`
  /`app_namespace`.
- **Deferred** (work on target stack, keep for a focused follow-up): exit the
  feincms3-meta fork (still imports/renders on 5.6), taggit 5→6, django-su→hijack,
  CKEditor 4 → django-prose-editor.

## Phase 4 — Django 4.2 → 5.2 LTS, Python 3.13, psycopg 3 (done)
Landing zone: Django 5.2 LTS (supported to April 2028) on Python 3.13, psycopg 3.
Validated on the prod dump: **131/131 URLs → 200**, admin suite green, no
migration drift.

- Django → 5.2, `psycopg2-binary` → `psycopg[binary]` 3.2 (the `postgresql`
  backend auto-selects psycopg 3 — no settings change). Bumps: Pillow 11,
  debug-toolbar 7, ckeditor 6.7, reversion 6.3, celery 5.5, taggit 5.1+,
  beautifulsoup4 4.15, cryptography 49. Compiled against `.venv-p4` (Py 3.13).
- **`get_storage_class()` removed in Django 5.1** (sections/models.py) → use the
  `default_storage` instance directly.
- **debug-toolbar 7 imports a model at URL-import time.** `juso/urls.py`
  unconditionally did `include(debug_toolbar.urls)`, but `debug_toolbar` is only
  in `INSTALLED_APPS` when `DEBUG` is on — so under `DEBUG=0` (prod, CI) every
  request 500'd with `HistoryEntry ... isn't in an application in INSTALLED_APPS`.
  Moved the import + `__debug__/` route inside the `if settings.DEBUG:` block.
- Docker base → `python:3.13-bookworm`; CI `python-version` → 3.13.

### Postgres 14+ requirement — Phase 5 folded in
**Django 5.2 hard-requires PostgreSQL 14+** (`NotSupportedError` on connect
otherwise), so the Postgres upgrade can no longer be deferred: Phase 4 is *not*
deployable against the existing PG12. All Postgres pins moved to
`postgres:17-alpine` (CI `test.yml`, `docker-compose.yml` — dev volume renamed
`postgres13_data` → `postgres17_data`, and `docker-compose.prod.yml`).

**Prod DB migration runbook (one-time, required before/with the Phase 4 deploy).**
A 17 container will not start on a PG12 `PGDATA`; dump from 12 and restore into a
fresh 17 volume:
```
# 1. With prod still on PG12, dump the live DB (custom format):
docker compose -f docker-compose.prod.yml exec db \
  pg_dump -U "$POSTGRES_USER" -Fc "$POSTGRES_DB" > juso-pg12.dump

# 2. Stop the stack; remove/rename the old PG12 volume so 17 initialises fresh:
docker compose -f docker-compose.prod.yml down
docker volume rm <project>_postgres_data   # back it up first if unsure

# 3. Bring up only the new PG17 db, then restore:
docker compose -f docker-compose.prod.yml up -d db
docker compose -f docker-compose.prod.yml exec -T db \
  pg_restore -U "$POSTGRES_USER" -d "$POSTGRES_DB" --no-owner --no-privileges < juso-pg12.dump

# 4. Start the rest and migrate (applies the Phase 3 feincms3 + language_code
#    migrations the raw prod dump predates):
docker compose -f docker-compose.prod.yml up -d
docker compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
```
Local validation followed exactly this shape: prod dump restored into a fresh
`postgres:17-alpine`, `migrate` applied 25 pending migrations, `smoke_urls
--per-site 3` → 131/131.
