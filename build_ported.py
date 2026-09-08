#!/usr/bin/env python3
"""Port the client's 22 FAQ pages + 35 realisation pages 1:1 at their own URLs.

Content (questions/answers, project text, images) is the client's own text —
lifted verbatim from faq_extract.json / projects_extract.json. This script
does not rewrite, summarise or add copy. It reuses the existing helpers in
transform.py (shell/patch_forms/patch_head/CTA_FORM) and build_pages_2.py
(faq_jsonld) rather than duplicating that logic.

One documented content-cleaning exception: the scraped "lis" for 19/22 FAQ
entries end with 4 lines that are not FAQ-answer content at all — they are
the field labels of the embedded WordPress contact form on the live FAQ page
("Je hebt interesse in: ...", "ik wil een douche op maat",
"ik wil een volledige badkamerrenovatie (...)", "Hoe heb je ons leren
kennen?..."), which the extractor swept up as if they were <li> answer
content. Rendering that as a bullet list under the answer would show every
visitor a nonsensical, unstyled duplicate of the real CTA form that already
sits at the bottom of the page. is_junk_li() drops exactly that fixed
4-string pattern; every other list item is kept and rendered verbatim.

Run from repo root: python3 build_ported.py
Idempotent: re-running regenerates the same files and re-applies patches to
a freshly re-read inloopdouche.html template each time.
"""
import html as H
import json
import pathlib
import re
import subprocess
import sys

import transform as T
from build_pages_2 import faq_jsonld

ROOT = pathlib.Path(__file__).resolve().parent
DATA_ROOT = pathlib.Path(
    "/private/tmp/claude-501/-Users-jefvangool-Documents-GitHub-mcp-audit-platform/"
    "66b1f551-7c16-420d-a557-3d348fc2afa5/scratchpad/ck"
)
FAQ_JSON = DATA_ROOT / "faq" / "faq_extract.json"
PROJECTS_JSON = DATA_ROOT / "projects_extract.json"
CK_LIVE_PDF = "https://ckservice.be/wp-content/uploads/2020/05/algemene-aannemingsvoorwaarden-CK-Service.pdf"

ORIGIN = T.ORIGIN


# ---------------------------------------------------------------------------
# text helpers
# ---------------------------------------------------------------------------
def esc(s):
    """Escape for HTML body text (keep quotes literal, they're fine in text)."""
    return H.escape(s or "", quote=False)


def attr_esc(s):
    """Escape for use inside an HTML attribute value."""
    return H.escape(s or "", quote=True)


def meta_desc(text, limit=155):
    text = " ".join((text or "").split())
    if len(text) <= limit:
        return text
    cut = text[:limit]
    if " " in cut:
        cut = cut.rsplit(" ", 1)[0]
    return cut


_JUNK_LI_PREFIXES = (
    "je hebt interesse in:",
    "ik wil een volledige badkamerrenovatie",
    "hoe heb je ons leren kennen",
)
_JUNK_LI_EXACT = {"ik wil een douche op maat"}


def is_junk_li(item):
    """Scraped contact-form field labels bled into `lis` — see module docstring."""
    if not isinstance(item, str):
        return False
    t = item.strip().lower()
    if t in _JUNK_LI_EXACT:
        return True
    return any(t.startswith(p) for p in _JUNK_LI_PREFIXES)


def clean_lis(raw):
    out = []
    for item in raw or []:
        if isinstance(item, list):
            out.extend(x for x in item if isinstance(x, str) and not is_junk_li(x))
        elif isinstance(item, str) and not is_junk_li(item):
            out.append(item)
    return out


def render_ul(items):
    if not items:
        return ""
    return "<ul>" + "".join(f"<li>{esc(x)}</li>" for x in items) + "</ul>"


def render_paras(paras):
    return "".join(f"<p>{esc(p)}</p>" for p in paras or [])


# ---------------------------------------------------------------------------
# template + post-patches (same fixups build_pages_3.py applies to every
# generated page: GTM host gate, .wrap.nav header padding, schema logo/image,
# plus the footer "Toiletten" link every existing page already carries but
# the stale FOOTER constant in transform.py does not)
# ---------------------------------------------------------------------------
def clean_template():
    t = (ROOT / "inloopdouche.html").read_text(encoding="utf-8")
    t = re.sub(r'<link rel="canonical".*?</script>\n(?=</head>)', "", t, flags=re.S)
    t = re.sub(r"<noscript><iframe src=\"https://www.googletagmanager.com[^\n]*\n", "", t)
    return t


def apply_post_patches(x):
    x = x.replace(
        "<script>(function(w,d,s,l,i){w[l]=w[l]||[];",
        "<script>if(/(^|\\.)ckservice\\.be$/.test(location.hostname)||location.hostname==='localhost'){"
        "(function(w,d,s,l,i){w[l]=w[l]||[];",
        1,
    )
    x = x.replace(
        "})(window,document,'script','dataLayer','GTM-T8J62JH');</script>",
        "})(window,document,'script','dataLayer','GTM-T8J62JH');}</script>",
        1,
    )
    x = x.replace(
        ".hero .media img{background:#eaf0fb}",
        ".wrap.nav{padding:12px 24px} .nav .logo{flex:none} "
        "@media(max-width:880px){.nav{gap:12px}.nav .tel{font-size:1rem}.logo{font-size:1.2rem}}\n"
        ".hero .media img{background:#eaf0fb}",
        1,
    )
    x = x.replace(
        '"logo": "https://ckservice.be/img/favicon-192.jpg"',
        '"logo": "https://ckservice.be/img/logo-ck-service.webp"',
    )
    x = x.replace(
        '"image": "https://ckservice.be/img/hero-vrouw.jpg", "logo"',
        '"image": "https://ckservice.be/img/logo-ck-service.webp", "logo"',
    )
    if "/onze-toiletten/" not in x:
        x = x.replace(
            '<a href="/badkamer-renovatie-wandpanelen/">Wandpanelen</a><br/>',
            '<a href="/badkamer-renovatie-wandpanelen/">Wandpanelen</a><br/>'
            '<a href="/onze-toiletten/">Toiletten</a><br/>',
            1,
        )
    return x


def build_page(relname, clean_path, title, desc, body, template):
    """Build one nested page reusing T.shell -> T.patch_forms -> T.patch_head,
    same order build_pages_2.main() uses for new pages off the same template."""
    T.PAGES[relname] = clean_path
    h = T.shell(template, attr_esc(title), attr_esc(desc), body, None)
    h = T.patch_forms(h)
    h = T.patch_head(h, relname)
    h = apply_post_patches(h)
    out = ROOT / relname
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(h, encoding="utf-8")
    return h


# ---------------------------------------------------------------------------
# FAQ pages
# ---------------------------------------------------------------------------
def faq_body(slug, entry):
    q = entry["q"]
    paras = entry.get("paras", [])
    lis = clean_lis(entry.get("lis", []))
    body = f"""<section class="block">
  <div class="wrap">
    <article class="article">
      <span class="eyebrow">Veelgestelde vraag</span>
      <h1>{esc(q)}</h1>
      <div class="prose">
        {render_paras(paras)}
        {render_ul(lis)}
      </div>
      <p style="margin-top:24px"><a href="/faq/" style="color:var(--color-primary);font-weight:600">← Alle veelgestelde vragen</a></p>
    </article>
  </div>
</section>

""" + T.CTA_FORM.format(interest="faq") + "\n\n" + faq_jsonld([(q, " ".join(p.strip() for p in paras))])
    return body


def build_faq_pages(template):
    data = json.loads(FAQ_JSON.read_text(encoding="utf-8"))
    built = []
    for slug, entry in data.items():
        q = entry["q"]
        paras = entry.get("paras", [])
        title = f"{q} | CK Service"
        desc = meta_desc(paras[0] if paras else q)
        relname = f"faq/{slug}.html"
        clean_path = f"/faq/{slug}/"
        build_page(relname, clean_path, title, desc, faq_body(slug, entry), template)
        built.append(slug)
    return built, data


# ---------------------------------------------------------------------------
# Realisation (project) pages
# ---------------------------------------------------------------------------
def ext_for(url):
    base = url.split("?")[0]
    ext = pathlib.Path(base).suffix
    return ext if ext else ".jpg"


def download_image(url, dest):
    try:
        r = subprocess.run(
            ["curl", "-sSfL", "--max-time", "30", "-o", str(dest), url],
            capture_output=True,
        )
        return r.returncode == 0 and dest.exists() and dest.stat().st_size > 0
    except Exception:
        return False


def download_project_images(projects):
    """Returns {slug: [local filenames in original order]}, and list of failures."""
    img_dir = ROOT / "img" / "projecten"
    img_dir.mkdir(parents=True, exist_ok=True)
    downloaded = {}
    failures = []
    for p in projects:
        slug = p["slug"]
        ok = []
        for i, url in enumerate(p.get("imgs", []), start=1):
            fname = f"{slug}-{i}{ext_for(url)}"
            dest = img_dir / fname
            if download_image(url, dest):
                ok.append(fname)
            else:
                if dest.exists():
                    dest.unlink()
                failures.append((slug, url))
        downloaded[slug] = ok
    return downloaded, failures


def project_body(entry, imgs):
    title = entry["title"]
    municipality = (entry.get("municipality") or "").strip()
    paras = entry.get("paras", [])
    eyebrow = "Realisatie" + (f" · {esc(municipality)}" if municipality else "")

    hero_img = ""
    grid = ""
    if imgs:
        first = imgs[0]
        hero_img = f"""<section class="block" style="padding-top:0">
  <div class="wrap">
    <img src="/img/projecten/{first}" alt="{attr_esc(title)}" loading="eager" style="width:100%;height:auto;border-radius:var(--radius-lg);box-shadow:var(--shadow-card)" />
  </div>
</section>
"""
        rest = imgs[1:]
        if rest:
            cells = "".join(
                f'<img src="/img/projecten/{fn}" alt="{attr_esc(title)}" loading="lazy" />'
                for fn in rest
            )
            grid = f'<div class="wrap split" style="margin-top:24px">{cells}</div>'

    body = f"""<section class="block">
  <div class="wrap">
    <article class="article">
      <span class="eyebrow">{eyebrow}</span>
      <h1>{esc(title)}</h1>
    </article>
  </div>
</section>
{hero_img}
<section class="block">
  <div class="wrap">
    <article class="article">
      <div class="prose">
        {render_paras(paras)}
      </div>
      {grid}
      <p style="margin-top:24px"><a href="/onze-projecten/" style="color:var(--color-primary);font-weight:600">← Alle realisaties</a></p>
    </article>
  </div>
</section>

""" + T.CTA_FORM.format(interest="realisatie")
    return body


def build_project_pages(template, projects, imgs_by_slug):
    built = []
    for p in projects:
        slug = p["slug"]
        title = p["title"]
        paras = p.get("paras", [])
        desc = meta_desc(paras[0] if paras else title)
        relname = f"projecten/{slug}.html"
        clean_path = f"/projecten/{slug}/"
        build_page(relname, clean_path, f"{title} | CK Service", desc, project_body(p, imgs_by_slug.get(slug, [])), template)
        built.append(slug)
    return built


CARD_CSS = (
    '<style>.ck-cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:24px}'
    ".ck-card{background:#fff;border-radius:22px;box-shadow:0 10px 30px rgba(33,38,46,.08);overflow:hidden}"
    ".ck-card img{width:100%;aspect-ratio:1/1;object-fit:cover}"
    ".ck-card .b{padding:18px 20px 22px}.ck-card h3{font-size:1.3rem;margin-bottom:.4em}"
    ".ck-card p{font-size:1rem;color:#5a626c}</style>"
)


def projecten_index_body(projects, imgs_by_slug):
    cards = []
    for p in projects:
        slug = p["slug"]
        title = p["title"]
        municipality = (p.get("municipality") or "").strip()
        imgs = imgs_by_slug.get(slug, [])
        img_html = (
            f'<img src="/img/projecten/{imgs[0]}" alt="{attr_esc(title)}" loading="lazy" />'
            if imgs
            else ""
        )
        sub = f"<p>{esc(municipality)}</p>" if municipality else ""
        cards.append(
            f'<a class="ck-card" href="/projecten/{slug}/" style="display:block;color:inherit;text-decoration:none">'
            f"{img_html}<div class=\"b\"><h3>{esc(title)}</h3>{sub}</div></a>"
        )
    body = CARD_CSS + f"""
<section class="block">
  <div class="wrap center" style="margin-bottom:32px">
    <h1>Onze realisaties</h1>
  </div>
  <div class="wrap ck-cards">
{''.join(cards)}
  </div>
  <div class="wrap center" style="margin-top:32px">
    <a class="btn btn--ghost" href="/onze-projecten/">Bekijk ook de voor-en-na foto's</a>
  </div>
</section>
"""
    return body


def build_projecten_index(template, projects, imgs_by_slug):
    # Reuse existing, already-approved footer copy for the meta description
    # instead of inventing new marketing text for this index page.
    desc = "Veilige badkamer- en doucherenovaties. Klaar in 1 dag, door eigen vakmensen."
    build_page(
        "projecten/index.html",
        "/projecten/",
        "Realisaties van CK Service | badkamers en douches",
        desc,
        projecten_index_body(projects, imgs_by_slug),
        template,
    )


# ---------------------------------------------------------------------------
# faq.html hub: add "lees het volledige antwoord" links under matched Q&As.
# Conservative, hand-verified mapping (hub summary text -> faq slug) — built
# by comparing every hub <summary> against every faq_extract.json "q" for a
# shared distinctive keyword/topic; ambiguous or topic-mismatched pairs are
# left unmatched rather than guessed.
# ---------------------------------------------------------------------------
HUB_TO_SLUG = {
    "Op welke premie heb ik recht?": "krijg-je-een-aanpassingspremie-voor-je-badkamer-van-ck-service",
    "In welke regio werken jullie?": "in-welke-regios-is-ck-service-actief",
    "Kan CK Service mijn douche aanpassen voor senioren?": "kan-ck-service-mijn-douche-aanpassen-voor-senioren",
    "Vanaf welke leeftijd heb ik een aangepaste badkamer nodig?": "vanaf-welke-leeftijd-heb-ik-een-senioren-badkamer-nodig",
    "Kan CK Service een douchestoel plaatsen?": "kan-ckservice-een-douchestoel-plaatsen",
    "Wat zijn de voordelen van een lage instapdouche?": "wat-zijn-de-voordelen-van-een-lage-douchebak",
    "Een bad vervangen door een douche, hoe gaat dat?": "een-bad-vervangen-door-een-douche-hoe-gaat-dat-in-zijn-werk",
    "Wat zijn de voordelen van een gesloten douchecabine?": "wat-zijn-de-voordelen-van-een-gesloten-douchecabine",
    "Hoe verloopt een badkamerrenovatie bij CK Service?": "hoe-verloopt-de-renovatie-van-je-badkamer-bij-ckservice",
    "Hoelang duurt een badkamerrenovatie?": "hoelang-duurt-badkamer-renovatie",
    "Kan CK Service ook alleen een nieuwe douche plaatsen?": "alleen-douche-plaatsen",
    "Wat zijn de nadelen van renoveren zonder breken?": "nadelen-badkamer-renovatie-zonder-breken",
    "Kan CK Service mijn kleine badkamer renoveren?": "kan-ck-service-mijn-kleine-badkamer-renoveren",
    "Richt CK Service ook mijn badkamer in?": "kan-ck-service-mijn-badkamer-inrichten",
    "Waarop moet ik letten als ik zelf een inloopdouche plaats?": "zelf-inloopdouche-plaatsen",
    "Heeft CK Service een showroom?": "heeft-ck-service-showroom-badkamers",
    "Kan CK Service een hangtoilet plaatsen?": "hangtoilet-plaatsen",
    "Wat is een Japans toilet of douchetoilet?": "wat-is-japans-toilet",
    "Mag een wasmachine in de badkamer staan?": "een-wasmachine-in-de-badkamer-plaatsen-mag-dat",
}

HUB_UNMATCHED = [
    "Hoe lang duurt het om een veilige douche te plaatsen?",
    "Geeft dat veel breekwerk en stof in huis?",
    "Werken jullie met eigen mensen of onderaannemers?",
    "Wat kost een veilige douche?",
    "Moet ik mijn hele badkamer laten renoveren?",
    "Hoe blijft de douche makkelijk schoon?",
    "Is een adviesgesprek echt gratis en vrijblijvend?",
]


def patch_faq_hub(faq_data):
    p = ROOT / "faq.html"
    h = p.read_text(encoding="utf-8")
    applied = []
    for summary, slug in HUB_TO_SLUG.items():
        if slug not in faq_data:
            continue
        link = f'\n<p><a href="/faq/{slug}/" style="color:var(--color-primary);font-weight:600">Lees het volledige antwoord →</a></p>'
        pattern = re.compile(
            r"(<summary>" + re.escape(summary) + r'</summary>\s*<div class="answer">.*?)(</div>\s*</details>)',
            flags=re.S,
        )
        new_h, n = pattern.subn(lambda m: m.group(1) + link + m.group(2), h, count=1)
        if n == 1:
            h = new_h
            applied.append((summary, slug))
        else:
            print(f"  WARNING: hub summary not found verbatim, skipped: {summary!r}")
    p.write_text(h, encoding="utf-8")
    return applied


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    template = clean_template()

    faq_slugs, faq_data = build_faq_pages(template)
    print(f"faq pages built: {len(faq_slugs)}")

    projects = json.loads(PROJECTS_JSON.read_text(encoding="utf-8"))
    imgs_by_slug, img_failures = download_project_images(projects)
    total_imgs = sum(len(p.get("imgs", [])) for p in projects)
    total_ok = sum(len(v) for v in imgs_by_slug.values())
    print(f"project images: {total_ok}/{total_imgs} downloaded, {len(img_failures)} failed")
    for slug, url in img_failures:
        print(f"  FAILED image: {slug} <- {url}")

    project_slugs = build_project_pages(template, projects, imgs_by_slug)
    print(f"project pages built: {len(project_slugs)}")

    build_projecten_index(template, projects, imgs_by_slug)
    print("projecten/index.html built")

    applied = patch_faq_hub(faq_data)
    matched_slugs = {slug for _, slug in applied}
    unmatched_slugs = [s for s in faq_data if s not in matched_slugs]
    print(f"\nhub link mapping applied ({len(applied)}):")
    for summary, slug in applied:
        print(f"  {summary!r} -> /faq/{slug}/")
    print(f"\nhub questions left unmatched ({len(HUB_UNMATCHED)}):")
    for q in HUB_UNMATCHED:
        print(f"  {q!r}")
    if unmatched_slugs:
        print(f"\nfaq slugs with no hub link ({len(unmatched_slugs)}): {unmatched_slugs}")

    # docs/ PDF referenced by the new REDIRECTS entry (server.js edited separately)
    docs_dir = ROOT / "docs"
    docs_dir.mkdir(exist_ok=True)
    pdf_dest = docs_dir / "algemene-aannemingsvoorwaarden-CK-Service.pdf"
    if download_image(CK_LIVE_PDF, pdf_dest):
        print(f"\ndownloaded {pdf_dest.name}")
    else:
        if pdf_dest.exists():
            pdf_dest.unlink()
        print(f"\nFAILED to download PDF: {CK_LIVE_PDF}")

    print("\ndone.")


if __name__ == "__main__":
    main()
