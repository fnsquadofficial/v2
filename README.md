# FN Squad · GitHub Pages

This release targets the root of `https://fnsquadofficial.github.io/`.

## Deploy after review

1. Extract the ZIP into a review branch of the existing `fnsquadofficial.github.io` repository. Copy the hidden `.github/` directory too. This replaces the existing `.github/workflows/pages.yml`.
2. Review the changes. In GitHub, check **Settings → Pages → Build and deployment** and use **GitHub Actions** as the source.
3. Merge into `main` when ready to publish. The Pages workflow rebuilds the public site and uploads `dist/`. Watch the **Actions** tab for the deployed URL.

The archive also contains a prebuilt `dist/`, including the old `.html` aliases, `404.html`, canonical URLs and a public sitemap.

## Edit and preview locally

The site is static. Edit page templates in `build.py`, links and stories in `content/reference.json`, and styles, scripts and assets in `dist/`.

```sh
python3 build.py --target github-pages
python3 -m http.server --directory dist 8000
```

Open `http://localhost:8000/` in your browser. The public build includes the GitHub Pages hosting notice in English and Bahasa Melayu. The CSS and platform logos load locally.
