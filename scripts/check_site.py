"""Fail deployment on missing local files, anchors, duplicate IDs or stale V2 links."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys

ROOT = Path(__file__).resolve().parents[1] / 'dist'
ORIGIN = 'fnsquadofficial.github.io'
BASE = '/v2/'


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.tags = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def check(root):
    root = root.resolve()
    pages = {p: Page(p.read_text(encoding='utf-8')) for p in root.rglob('*.html')}
    errors = []
    references = 0
    if not pages:
        errors.append('No generated HTML pages found')
    for path, page in pages.items():
        label = path.relative_to(root)
        ids = [attrs['id'] for _, attrs in page.tags if 'id' in attrs]
        for value, count in Counter(ids).items():
            if count > 1:
                errors.append(f'{label}: duplicate id {value}')
        for tag, attrs in page.tags:
            if tag == 'img' and 'alt' not in attrs:
                errors.append(f'{label}: image missing alt attribute')
            for key in ('href', 'src'):
                if key not in attrs:
                    continue
                url = urlsplit(attrs[key])
                if url.netloc and url.netloc != ORIGIN:
                    continue
                if url.scheme and url.scheme not in ('http', 'https'):
                    continue
                route = unquote(url.path)
                if route.startswith('/'):
                    if not route.startswith(BASE):
                        errors.append(f'{label}: URL outside V2: {attrs[key]}')
                        continue
                    target = root / route[len(BASE):]
                else:
                    target = path.parent / route if route else path
                target = target.resolve()
                if not target.is_relative_to(root):
                    errors.append(f'{label}: URL escapes public directory: {attrs[key]}')
                    continue
                if target.is_dir():
                    target /= 'index.html'
                references += 1
                if not target.is_file():
                    errors.append(f'{label}: missing file: {attrs[key]}')
                elif url.fragment and target in pages:
                    target_ids = {a.get('id') for _, a in pages[target].tags}
                    if unquote(url.fragment) not in target_ids:
                        errors.append(f'{label}: missing anchor: {attrs[key]}')
    return errors, len(pages), references


if __name__ == '__main__':
    errors, pages, references = check(ROOT)
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        sys.exit(1)
    print(f'Validated {pages} HTML files and {references} local references.')
