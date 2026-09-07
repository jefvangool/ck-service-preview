#!/usr/bin/env python3
"""One-shot launch transform for the CK reference site (run from repo root).

- clean URLs (root-relative links/assets), footer NAP + legal links, no blog
- head: canonical, robots, OG, favicon, JSON-LD (values copied from the live site),
  GTM-T8J62JH with Consent Mode default=denied, /js/ck.js
- forms -> POST /api/lead (email optional, consent, honeypot, attribution)
- generates: wandpanelen.html, bedankt.html, 404.html, privacy/cookie/disclaimer pages
Idempotent: re-running re-applies from the marker-free originals (git checkout first).
"""
import json, re, sys, pathlib, html as H

ROOT = pathlib.Path(__file__).resolve().parent
LIVE = pathlib.Path('/private/tmp/claude-501/-Users-jefvangool-Documents-GitHub-mcp-audit-platform/66b1f551-7c16-420d-a557-3d348fc2afa5/scratchpad/ck')
ORIGIN = 'https://ckservice.be'

PAGES = {  # file -> clean path
    'index.html': '/', 'inloopdouche.html': '/inloopdouche/', 'douchecabine.html': '/douchecabine/',
    'douche-plaatsen.html': '/douche-plaatsen/', 'wandpanelen.html': '/badkamer-renovatie-wandpanelen/',
    'premie.html': '/premie/', 'badkamer-renovatie-geel.html': '/badkamer-renovatie-geel/',
    'projecten.html': '/onze-projecten/', 'over-ons.html': '/over-ons/', 'faq.html': '/faq/',
    'contact.html': '/contact/', 'privacy-verklaring.html': '/privacy-verklaring/',
    'cookiebeleid.html': '/cookiebeleid/', 'disclaimer.html': '/disclaimer/', 'bedankt.html': '/bedankt/',
    '404.html': '/404/',
}
NOINDEX = {'bedankt.html', '404.html'}
LINKMAP = {
    'index.html#diensten': '/#diensten', 'index.html#premie': '/premie/', 'index.html#contact': '/contact/',
    'index.html': '/', 'inloopdouche.html': '/inloopdouche/', 'douchecabine.html': '/douchecabine/',
    'douche-plaatsen.html': '/douche-plaatsen/', 'premie.html': '/premie/',
    'badkamer-renovatie-geel.html': '/badkamer-renovatie-geel/', 'projecten.html': '/onze-projecten/',
    'over-ons.html': '/over-ons/', 'faq.html': '/faq/', 'contact.html': '/contact/',
    'blog-post.html': '/premie/', 'blog.html': '/faq/',
}

GTM_ID = 'GTM-T8J62JH'

def live_jsonld():
    h = (LIVE / 'live_home.html').read_text(encoding='utf-8', errors='replace')
    org = lb = None
    for m in re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', h, flags=re.S):
        try:
            d = json.loads(m)
        except Exception:
            continue
        for n in d.get('@graph', [d]):
            if n.get('@type') == 'Organization': org = n
            if n.get('@type') == 'LocalBusiness': lb = n
    assert org and lb, 'live JSON-LD not found'
    logo = f'{ORIGIN}/img/favicon-192.jpg'
    org = {'@type': 'Organization', 'name': 'CK Service', 'url': ORIGIN, 'logo': logo,
           'email': 'info@ckservice.be', 'telephone': '+32 493 33 39 88', 'vatID': 'BE0845.789.223',
           'sameAs': [s for s in org.get('sameAs', []) if s != ORIGIN]}
    lb = {'@type': 'LocalBusiness', '@id': f'{ORIGIN}/#localbusiness', 'name': 'CK Service', 'url': ORIGIN,
          'image': f'{ORIGIN}/img/hero-vrouw.jpg', 'logo': logo, 'telephone': '+32 493 33 39 88',
          'email': 'info@ckservice.be', 'priceRange': lb.get('priceRange', '€€'), 'vatID': 'BE0845.789.223',
          'address': {'@type': 'PostalAddress', 'streetAddress': 'Zammelseweg 92', 'addressLocality': 'Geel',
                      'postalCode': '2440', 'addressCountry': 'BE'},
          'geo': lb.get('geo'), 'areaServed': lb.get('areaServed'), 'sameAs': org['sameAs'],
          'description': 'CK Service vervangt je oude bad door een veilige inloopdouche, klaar in 1 dag door eigen vakmensen. Badkamer- en doucherenovaties, wandpanelen en aanpassingspremie tot €1.250.'}
    return json.dumps({'@context': 'https://schema.org', '@graph': [org, lb]}, ensure_ascii=False)

JSONLD = live_jsonld()

HEAD_EXTRA = '''<link rel="icon" href="/img/favicon-32.jpg" sizes="32x32" />
<link rel="icon" href="/img/favicon-192.jpg" sizes="192x192" />
<link rel="apple-touch-icon" href="/img/favicon-192.jpg" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="CK Service" />
<meta property="og:locale" content="nl_BE" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{desc}" />
<meta property="og:url" content="{url}" />
<meta property="og:image" content="{origin}/img/hero-vrouw.jpg" />
<meta name="twitter:card" content="summary_large_image" />
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}
gtag('consent','default',{{'ad_storage':'denied','ad_user_data':'denied','ad_personalization':'denied','analytics_storage':'denied','wait_for_update':500}});</script>
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','{gtm}');</script>
<script defer src="/js/ck.js"></script>
<style>
.ck-consent{{position:fixed;left:0;right:0;bottom:0;z-index:100;padding:16px;background:rgba(33,38,46,.35)}}
.ck-consent__box{{max-width:820px;margin:0 auto;background:#fff;border-radius:22px;box-shadow:0 10px 30px rgba(33,38,46,.18);padding:22px 24px;display:grid;gap:14px}}
.ck-consent__box p{{font-size:1rem;line-height:1.5;margin:0}} .ck-consent__box a{{color:#2F5597;text-decoration:underline}}
.ck-consent__actions{{display:flex;flex-wrap:wrap;gap:10px}} .ck-consent__actions .btn{{min-height:48px;padding:12px 22px;font-size:.95rem}}
.ck-form-extra{{display:grid;gap:8px;margin-top:6px}} .ck-form-extra label.chk{{display:flex;gap:10px;align-items:flex-start;font-size:.9rem;line-height:1.4;text-transform:none;letter-spacing:0;font-family:inherit;font-weight:500}}
.ck-form-extra label.chk input{{width:22px;height:22px;margin-top:2px;flex:none}} .ck-form-note{{font-size:.85rem;opacity:.85;line-height:1.4}} .ck-form-note a{{text-decoration:underline}}
.ck-form-error{{background:#fff3f0;color:#8a2a1a;border-radius:14px;padding:12px 16px;font-size:.95rem;margin-bottom:12px}} .hp{{position:absolute;left:-9999px;top:-9999px;opacity:0;height:0;width:0}}
.article{{max-width:820px;margin:0 auto}} .article h1{{font-size:clamp(2.2rem,5vw,3.4rem);margin-bottom:.6em}} .article h2{{font-size:1.5rem;margin:1.4em 0 .5em}} .article p,.article li{{margin:.6em 0;font-size:1.05rem}} .article ul{{padding-left:1.3em}}
.hero .media img{{background:#eaf0fb}}
</style>
<script type="application/ld+json">{jsonld}</script>
'''

GTM_NOSCRIPT = '<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={gtm}" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>\n'

FOOTER = '''<footer>
  <div class="wrap grid">
    <div>
      <a class="logo" href="/" aria-label="CK Service home"><b>CK</b><span>SERVICE</span></a>
      <p style="margin-top:12px;max-width:36ch">Veilige badkamer- en douche&shy;renovaties. Klaar in 1 dag, door eigen vakmensen.</p>
      <p style="margin-top:12px;max-width:36ch;opacity:.7;font-size:.9rem">Thuisbasis Geel (Kempen). Volledige renovaties tot zo'n 43 km rond Geel en Antwerpen, douche-installaties in heel België.</p>
    </div>
    <div><strong style="color:#fff">Diensten</strong><br/><a href="/inloopdouche/">Inloopdouche</a><br/><a href="/douchecabine/">Douchecabine</a><br/><a href="/douche-plaatsen/">Douche plaatsen</a><br/><a href="/badkamer-renovatie-wandpanelen/">Wandpanelen</a><br/><a href="/badkamer-renovatie-geel/">Badkamerrenovatie Geel</a></div>
    <div><strong style="color:#fff">Meer</strong><br/><a href="/premie/">Premie &amp; kosten</a><br/><a href="/onze-projecten/">Realisaties</a><br/><a href="/over-ons/">Over ons</a><br/><a href="/faq/">Veelgestelde vragen</a><br/><a href="/contact/">Contact</a></div>
    <div><strong style="color:#fff">CK Service</strong><br/>Zammelseweg 92<br/>2440 Geel<br/><a href="tel:+32493333988">0493 33 39 88</a><br/><a href="mailto:info@ckservice.be">info@ckservice.be</a><br/><span style="opacity:.7">BTW BE0845.789.223</span></div>
  </div>
  <div class="wrap" style="margin-top:28px;opacity:.6;font-size:.85rem">© 2026 CK Service · Badkamergevoel? · <a href="/privacy-verklaring/">Privacyverklaring</a> · <a href="/cookiebeleid/">Cookiebeleid</a> · <a href="/disclaimer/">Disclaimer</a> · <a href="#" data-consent-reset>Cookie-instellingen</a></div>
</footer>'''

FORM_EXTRA = '''      <div class="ck-form-extra">
        <label for="email-{n}">E-mail <span style="opacity:.7;font-weight:400">(optioneel, voor je bevestiging)</span></label>
        <input id="email-{n}" name="email" type="email" autocomplete="email" placeholder="naam@voorbeeld.be" />
        <label class="chk"><input type="checkbox" name="consent" value="on" /> <span>CK Service mag me ook later informeren over premies en acties (optioneel).</span></label>
        <p class="ck-form-note">We gebruiken je gegevens enkel om je aanvraag op te volgen. <a href="/privacy-verklaring/">Privacyverklaring</a>.</p>
      </div>
      <div class="hp" aria-hidden="true"><label>Website<input type="text" name="website" tabindex="-1" autocomplete="off" /></label></div>
      <input type="hidden" name="t0" value="" /><input type="hidden" name="page" value="" /><input type="hidden" name="referrer" value="" />
      <input type="hidden" name="gclid" value="" /><input type="hidden" name="wbraid" value="" /><input type="hidden" name="gbraid" value="" />
      <input type="hidden" name="utm_source" value="" /><input type="hidden" name="utm_medium" value="" /><input type="hidden" name="utm_campaign" value="" /><input type="hidden" name="utm_term" value="" /><input type="hidden" name="utm_content" value="" />
'''

def fix_links(h):
    def repl(m):
        q, target = m.group(1), m.group(2)
        return f'href={q}{LINKMAP.get(target, target)}{q}'
    h = re.sub(r'href=(["\'])([a-z0-9-]+\.html(?:#[a-z-]+)?)\1', repl, h)
    h = h.replace('href="css/ck.css"', 'href="/css/ck.css"')
    h = re.sub(r'(src|href)="(img|css|docs)/', r'\1="/\2/', h)
    return h

def patch_head(h, fname):
    title = re.search(r'<title>(.*?)</title>', h, flags=re.S).group(1).strip()
    desc_m = re.search(r'<meta name="description" content="([^"]*)"', h)
    desc = desc_m.group(1) if desc_m else ''
    url = ORIGIN + PAGES[fname]
    robots = '<meta name="robots" content="noindex,follow" />' if fname in NOINDEX else '<meta name="robots" content="index,follow,max-image-preview:large" />'
    extra = f'<link rel="canonical" href="{url}" />\n{robots}\n' + HEAD_EXTRA.format(
        title=H.escape(H.unescape(title), quote=True), desc=H.escape(H.unescape(desc), quote=True), url=url, origin=ORIGIN, gtm=GTM_ID, jsonld=JSONLD)
    h = h.replace('</head>', extra + '</head>', 1)
    h = re.sub(r'<body>\s*', '<body>\n' + GTM_NOSCRIPT.format(gtm=GTM_ID), h, count=1)
    return h

def patch_footer(h):
    return re.sub(r'<footer>.*?</footer>', FOOTER, h, flags=re.S)

def patch_forms(h):
    n = [0]
    def repl(m):
        n[0] += 1
        inner = m.group(1)
        inner = inner.replace('<input id="naam" name="naam"', '<input id="naam" name="naam" required minlength="2"')
        inner = inner.replace('<input id="tel" name="tel" type="tel"', '<input id="tel" name="tel" type="tel" required minlength="8"')
        inner = re.sub(r'(\s*)(<button class="btn" type="submit">)', lambda b: '\n' + FORM_EXTRA.format(n=n[0]) + b.group(1) + b.group(2), inner, count=1)
        return f'<form action="/api/lead" method="post">{inner}</form>'
    return re.sub(r'<form action="#" method="post">(.*?)</form>', repl, h, flags=re.S)

def nav_current(h, fname):
    # aria-current on the matching nav item
    path = PAGES[fname]
    h = re.sub(r' aria-current="page"', '', h)
    return h.replace(f'<a href="{path}">', f'<a href="{path}" aria-current="page">', 1) if path != '/' else h

def process_existing(fname):
    p = ROOT / fname
    h = p.read_text(encoding='utf-8')
    h = fix_links(h)
    h = patch_footer(h)
    h = patch_forms(h)
    if fname == 'contact.html':
        h = h.replace('<form action="/api/lead"', '<div class="ck-form-error" hidden>Er ontbreekt nog iets: vul je naam en telefoonnummer in (en een geldig e-mailadres als je dat invult).</div>\n    <form action="/api/lead"', 1)
    h = nav_current(h, fname)
    h = patch_head(h, fname)
    p.write_text(h, encoding='utf-8')
    return h

# ---------------------------------------------------------------------------
# New pages from the inloopdouche template
# ---------------------------------------------------------------------------
def shell(template, title, desc, body_sections, current=None):
    head = re.search(r'<head>.*?</head>', template, flags=re.S).group(0)
    head = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', head, flags=re.S)
    head = re.sub(r'<meta name="description" content="[^"]*"', f'<meta name="description" content="{desc}"', head)
    header = re.search(r'<header>.*?</header>', template, flags=re.S).group(0)
    header = header.replace(' aria-current="page"', '')
    if current: header = header.replace(f'<a href="{current}">', f'<a href="{current}" aria-current="page">', 1)
    return f'<!DOCTYPE html>\n<html lang="nl">\n{head}\n<body>\n\n{header}\n\n{body_sections}\n\n{FOOTER}\n</body>\n</html>\n'

CTA_FORM = '''<section class="cta" id="contact">
  <div class="wrap">
    <div>
      <h2>Klaar voor jouw badkamergevoel?</h2>
      <p class="lead">Plan een gratis, vrijblijvend adviesgesprek. We bekijken je badkamer, leggen alles helder uit en zoeken je premie uit.</p>
      <p class="lead" style="margin-top:18px">📞 Liever bellen? <strong><a href="tel:+32493333988">0493 33 39 88</a></strong> &nbsp;·&nbsp; ✉️ <a href="mailto:info@ckservice.be">info@ckservice.be</a></p>
    </div>
    <form action="#" method="post">
      <label for="naam">Naam</label>
      <input id="naam" name="naam" autocomplete="name" placeholder="Voor- en achternaam" />
      <label for="tel">Telefoon</label>
      <input id="tel" name="tel" type="tel" autocomplete="tel" placeholder="Zodat we je kunnen bellen" />
      <input type="hidden" name="interesse" value="{interest}" />
      <button class="btn" type="submit">Plan mijn gratis adviesgesprek</button>
    </form>
  </div>
</section>'''

WANDPANELEN = '''<section class="hero">
  <div class="wrap">
    <div>
      <span class="eyebrow">Badkamer renoveren zonder breken</span>
      <h1>Wand&shy;panelen<em>.</em></h1>
      <p class="lead">Nieuwe wanden <strong>over je bestaande tegels</strong>: waterdichte Rocko wandpanelen zonder voegen, geplaatst met een minimum aan stof en breekwerk.</p>
      <div class="cta-row">
        <a class="btn" href="#contact">Plan je gratis adviesgesprek</a>
        <a class="btn btn--ghost" href="/docs/CK-Service-Wandpanelen.pdf">Bekijk de brochure (PDF)</a>
      </div>
    </div>
    <div class="media">
      <img src="/img/wandpanelen/wandpanelen-1.webp" alt="Badkamer gerenoveerd met Rocko wandpanelen door CK Service" />
      <span class="logo badge"><b>CK</b><span>SERVICE</span></span>
    </div>
  </div>
</section>

<div class="trust">
  <div class="wrap">
    <div class="item"><b>4 mm</b> dun, over je bestaande tegels</div>
    <div class="item"><b>Waterdicht</b> en zonder voegen</div>
    <div class="item"><b>Minimum</b> stof &amp; breekwerk</div>
    <div class="item"><b>Eigen</b> vakmensen &amp; afwerking</div>
  </div>
</div>

<section class="block">
  <div class="wrap split">
    <div>
      <span class="eyebrow">Wat is het</span>
      <h2 class="h2">Een nieuwe badkamer zonder de verbouwing</h2>
      <div class="prose">
        <p>Zin in een frisse badkamer, maar geen zin in weken stof en lawaai? Rocko wandpanelen worden met amper 4 mm dikte bovenop je bestaande wandbekleding geplaatst. Geen tegels uitbreken, geen weken zonder badkamer.</p>
        <p>De panelen zijn waterdicht en hebben geen voegen. Dat oogt strak, en er is niets dat kan verkleuren of beschimmelen. Je laat ze plaatsen door onze eigen vakmensen, of je plaatst ze zelf.</p>
      </div>
      <ul class="usp">
        <li>Over je bestaande tegels of muren, dus geen breekwerk</li>
        <li>Waterdicht en zonder voegen, eenvoudig schoon te houden</li>
        <li>Snelle plaatsing met een minimum aan stof</li>
        <li>Ook om te combineren met een nieuwe, veilige douche</li>
        <li>Laten plaatsen door CK Service of zelf plaatsen</li>
        <li>Eigen vakmensen, de zaakvoerder werkt mee</li>
      </ul>
    </div>
    <img src="/img/wandpanelen/rocko-7.webp" alt="Detail van Rocko wandpanelen in een gerenoveerde badkamer" />
  </div>
</section>

<section class="block alt">
  <div class="wrap">
    <div class="center">
      <span class="eyebrow">Zo werkt het</span>
      <h2 class="h2">Vandaag beslissen, snel genieten</h2>
      <p>Wij ontzorgen je van het eerste advies tot de laatste afwerking. Een badkamer met wandpanelen is vaak binnen de week klaar.</p>
    </div>
    <div class="steps">
      <div class="step"><div class="n">1</div><h3>Gratis adviesgesprek</h3><p>We bekijken je badkamer en bespreken welke panelen en afwerking bij je passen.</p></div>
      <div class="step"><div class="n">2</div><h3>Helder voorstel</h3><p>Een duidelijke offerte, zonder verrassingen.</p></div>
      <div class="step"><div class="n">3</div><h3>Plaatsing</h3><p>De panelen gaan over je bestaande tegels. Weinig stof, weinig breekwerk, alles netjes afgewerkt.</p></div>
      <div class="step"><div class="n">4</div><h3>Zorgeloos genieten</h3><p>Alles opgeruimd en afgevoerd. Jij geniet van je nieuwe badkamer.</p></div>
    </div>
  </div>
</section>

<section class="block">
  <div class="wrap split">
    <img src="/img/wandpanelen/rocko-11.webp" alt="Badkamer met Rocko wandpanelen en nieuwe douche" />
    <div>
      <span class="eyebrow">Combineer slim</span>
      <h2 class="h2">Meteen ook je bad vervangen?</h2>
      <div class="prose">
        <p>Veel klanten combineren wandpanelen met een veilige inloopdouche of douchecabine. Je oude bad eruit, een drempelloze douche erin en nieuwe wanden errond: in één beweging een veilige én frisse badkamer.</p>
        <p>Vervang je je bad door een veilige douche? Dan zoeken we meteen de <a href="/premie/" style="text-decoration:underline">aanpassingspremie tot €1.250</a> voor je uit.</p>
      </div>
      <p style="margin-top:18px"><a class="btn btn--ghost" href="/docs/CK-Service-ROCKO_TILES.pdf">Rocko Tiles brochure (PDF)</a></p>
    </div>
  </div>
</section>

<section class="block alt">
  <div class="wrap center" style="margin-bottom:28px">
    <span class="eyebrow">Ook interessant</span>
    <h2 class="h2">Andere oplossingen</h2>
  </div>
  <div class="wrap related">
    <a href="/inloopdouche/">Inloopdouche →</a>
    <a href="/douchecabine/">Douchecabine →</a>
    <a href="/douche-plaatsen/">Douche plaatsen →</a>
    <a href="/badkamer-renovatie-geel/">Badkamerrenovatie Geel →</a>
  </div>
</section>

''' + CTA_FORM.format(interest='wandpanelen')

BEDANKT = '''<section class="hero">
  <div class="wrap">
    <div>
      <span class="eyebrow">Aanvraag ontvangen</span>
      <h1>Bedankt<em>.</em></h1>
      <p class="lead">We hebben je aanvraag goed ontvangen en bellen je zo snel mogelijk terug om een gratis adviesgesprek in te plannen.</p>
      <p class="lead">Dringend? Bel ons gerust op <strong><a href="tel:+32493333988">0493 33 39 88</a></strong>.</p>
      <div class="cta-row">
        <a class="btn btn--ghost" href="/">Terug naar de homepage</a>
        <a class="btn btn--ghost" href="/onze-projecten/">Bekijk onze realisaties</a>
      </div>
    </div>
    <div class="media">
      <img src="/img/koppel.jpg" alt="Tevreden klanten van CK Service" />
      <span class="logo badge"><b>CK</b><span>SERVICE</span></span>
    </div>
  </div>
</section>'''

NOTFOUND = '''<section class="hero">
  <div class="wrap">
    <div>
      <span class="eyebrow">Fout 404</span>
      <h1>Pagina niet gevonden<em>.</em></h1>
      <p class="lead">Deze pagina bestaat niet (meer). Misschien zoek je een van deze?</p>
      <div class="cta-row">
        <a class="btn" href="/">Homepage</a>
        <a class="btn btn--ghost" href="/inloopdouche/">Inloopdouche</a>
        <a class="btn btn--ghost" href="/premie/">Premie &amp; kosten</a>
        <a class="btn btn--ghost" href="/contact/">Contact</a>
      </div>
    </div>
    <div class="media">
      <img src="/img/vrouw2.jpg" alt="CK Service" />
      <span class="logo badge"><b>CK</b><span>SERVICE</span></span>
    </div>
  </div>
</section>'''

def legal_page(name, h1):
    blocks = (LIVE / f'legal_{name}.html').read_text(encoding='utf-8')
    blocks = re.sub(r'<p>Home » [^<]*</p>\n?', '', blocks)
    return f'''<section class="block">
  <div class="wrap">
    <article class="article">
      <span class="eyebrow">Juridisch</span>
      <h1>{h1}</h1>
      {blocks}
    </article>
  </div>
</section>'''

def main():
    template = (ROOT / 'inloopdouche.html').read_text(encoding='utf-8')
    template = fix_links(template)
    new_pages = {
        'wandpanelen.html': ('Badkamer renoveren zonder breken met Rocko wandpanelen | CK Service',
            'Renoveer je badkamer zonder breekwerk: waterdichte Rocko wandpanelen zonder voegen, geplaatst over je bestaande tegels. Hygiënisch, onderhoudsvriendelijk en snel klaar.', WANDPANELEN, None),
        'bedankt.html': ('Bedankt voor je aanvraag | CK Service', 'We hebben je aanvraag ontvangen en bellen je snel terug.', BEDANKT, None),
        '404.html': ('Pagina niet gevonden | CK Service', 'Deze pagina bestaat niet (meer).', NOTFOUND, None),
        'privacy-verklaring.html': ('Privacyverklaring | CK Service', 'Hoe CK Service omgaat met je persoonsgegevens.', legal_page('privacy-verklaring', 'Privacy&shy;verklaring'), None),
        'cookiebeleid.html': ('Cookiebeleid | CK Service', 'Welke cookies ckservice.be gebruikt en hoe je je keuze aanpast.', legal_page('cookiebeleid', 'Cookie&shy;beleid'), None),
        'disclaimer.html': ('Disclaimer | CK Service', 'Disclaimer van de website van CK Service.', legal_page('disclaimer', 'Disclaimer'), None),
    }
    for fname, (title, desc, body, cur) in new_pages.items():
        (ROOT / fname).write_text(shell(template, title, desc, body, cur), encoding='utf-8')
    for fname in list(PAGES):
        if fname in new_pages:
            h = (ROOT / fname).read_text(encoding='utf-8')
            h = patch_forms(h)
            h = patch_head(h, fname)
            (ROOT / fname).write_text(h, encoding='utf-8')
        elif (ROOT / fname).exists():
            process_existing(fname)
    for stale in ('blog.html', 'blog-post.html'):
        if (ROOT / stale).exists(): (ROOT / stale).unlink()
    # sanity: no remaining relative .html links or relative assets
    bad = []
    for fname in PAGES:
        h = (ROOT / fname).read_text(encoding='utf-8')
        for m in re.findall(r'(?:href|src)="([^"]+)"', h):
            if m.endswith('.html') or re.match(r'^(img|css|js|docs)/', m) or m.startswith('index.html'):
                bad.append((fname, m))
    print('pages:', len(PAGES), 'link issues:', bad[:10])

if __name__ == '__main__':
    main()
