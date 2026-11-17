# FN Squad V2 — Official Website

> **Sole official FN Squad website.** All four leaders agreed to use V2 as the current authoritative website, confirmed on 17 November 2026.
>
> **Official website:** https://fnsquadofficial.github.io/v2/
>
> The previous `fnsquadofficial/fnsquadofficial.github.io` website is superseded. The original-era `faizzzlol/freakyniggas` website is a historical archive. Future website development belongs in this repository.

This repository builds the project site at [fnsquadofficial.github.io/v2/](https://fnsquadofficial.github.io/v2/).

## Deploy from GitHub

1. Add the release files to the root of `fnsquadofficial/v2` and commit them to `main`. The workflow belongs at `.github/workflows/pages.yml`.
2. In the repository, open **Settings → Pages**. Under **Build and deployment**, set **Source** to **GitHub Actions**. Leave **Custom domain** blank for the default project URL.
3. Open **Actions → Deploy to GitHub Pages → Run workflow**. Select `main` and run it.
4. Open the deployment URL from the successful run.

The workflow runs when you start it in **Actions**. Run it again after committing a new release. It builds the public pages and uploads `dist/`.

## Build and preview locally

Edit page templates in `build.py`, links and stories in `content/reference.json`, and styles, scripts and assets in `dist/`.

```sh
python3 build.py --target github-pages
python3 -c "from shutil import copytree; copytree('dist', '.preview/v2', dirs_exist_ok=True)"
python3 -m http.server --directory .preview 8000
```

Open [localhost:8000/v2/](http://localhost:8000/v2/). The `v2/` path matches the hosted site. Keep the temporary `.preview/` folder out of commits.
