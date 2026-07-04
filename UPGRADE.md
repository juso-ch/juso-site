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

## Later (not in this branch)
Phase 3: feincms3 lockstep (5.6 / content-editor 9 / sites 0.21 / meta fork exit +
RegionRenderer refactor + page-types data migration). Phase 4: Django 5.2 / Py 3.13
/ psycopg 3. Phase 5: Postgres 12 → 17. See the full plan discussion.
