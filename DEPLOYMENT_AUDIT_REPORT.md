# INKAGROWTH Django Deployment Audit

Audit date: 2026-06-07

## Homepage Source of Truth

- URL pattern: `path('', front_views.index, name='index')`
- View: `front.views.index`
- Template rendered by `/`: `front/templates/index.html`
- Template lookup mode: `APP_DIRS=True` with no project-level `TEMPLATES['DIRS']`

## URL Pattern Findings

- `/` is served only by `front_views.index`.
- No active `home/` route exists.
- No active `index/` route exists.
- No `TemplateView` route serves a homepage template.
- The only non-route `home` reference is the `StaticSitemap` item name that maps to `/`.

## Template Findings

Active frontend templates:

- `front/templates/index.html`
- `front/templates/contact.html`
- `front/templates/authority_page.html`
- `front/templates/blog_index.html`
- `front/templates/blog_post.html`
- `front/templates/robots.txt`

Duplicate homepage templates:

- None in the active working tree.
- No `home.html` file exists.
- No landing-page template file exists.

Old homepage/template code found in Git history:

- Earlier commits contained older SEO/service/blog/dashboard templates, including `seo_page.html`, `service_page.html`, `post_list.html`, `post_detail.html`, `team.html`, and dashboard post templates.
- Those templates were removed from the active tree before this audit and are not deployed by current URL patterns.

## Deployment Findings

- `Procfile` was an empty directory, while `ProcfileY` and `Procfile.save` were tracked obsolete Procfile copies.
- Render deployment config was not present as `render.yaml`.
- Static files are generated under ignored `staticfiles/`; no homepage HTML is stored there.
- Django template caching is not explicitly enabled; template rendering uses the standard app template loader.

## Fix Applied

- Replaced the invalid `Procfile` directory with a real `Procfile`.
- Removed obsolete `ProcfileY` and `Procfile.save`.
- Added `render.yaml` with explicit build and start commands.
- Kept exactly one homepage implementation: `front.views.index` rendering `front/templates/index.html`.
- Removed duplicate `STATIC_ROOT` assignment in settings.
