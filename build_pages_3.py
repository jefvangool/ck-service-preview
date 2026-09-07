#!/usr/bin/env python3
"""Step 4 (/onze-toiletten/) and step 5 (real before/after pairs on /onze-projecten/).
Facts and images are the client's own (live ckservice.be). Run from repo root."""
import re, json, pathlib
import transform as T
from build_pages_2 import faq_block

ROOT = pathlib.Path(__file__).resolve().parent
T.PAGES['toiletten.html'] = '/onze-toiletten/'

CARD_CSS = '<style>.ck-cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:24px}.ck-card{background:#fff;border-radius:22px;box-shadow:0 10px 30px rgba(33,38,46,.08);overflow:hidden}.ck-card img{width:100%;aspect-ratio:1/1;object-fit:cover}.ck-card .b{padding:18px 20px 22px}.ck-card h3{font-size:1.3rem;margin-bottom:.4em}.ck-card p{font-size:1rem;color:#5a626c}.ck-pair{background:#fff;border-radius:22px;box-shadow:0 10px 30px rgba(33,38,46,.08);overflow:hidden}.ck-pair .imgs{display:grid;grid-template-columns:1fr 1fr}.ck-pair img{width:100%;aspect-ratio:3/4;object-fit:cover}.ck-pair .lbl{display:flex;justify-content:space-between;padding:12px 18px;font-family:var(--font-heading,Oswald,sans-serif);text-transform:uppercase;letter-spacing:.06em;font-size:.95rem}.ck-pair .lbl b{color:var(--color-primary,#4472C4)}</style>'

TOILET_QAS = [
    ("Hoelang duurt het om een nieuw toilet te plaatsen?", "Een nieuw toilet plaatsen doen we in 1 dag, ook een hangtoilet of een Japans douchetoilet."),
    ("Wat is een verhoogd toilet?", "Een toilet met een hogere zithoogte, zodat gaan zitten en opstaan minder inspanning vraagt. Ideaal voor wie minder mobiel is, en te combineren met steunbeugels."),
    ("Wat is een Japans toilet of douchetoilet?", "Een toilet dat je met warm water reinigt en met lucht droogt, zodat je geen wc-papier meer nodig hebt. Met een verwarmde bril, automatisch deksel en geurneutralisatie. Comfortabel en hygiënisch."),
    ("Wat als er geen afvoer is waar ik een toilet wil?", "Dan plaatsen we een toilet met vergruizer (sanibroyeur): die vermaalt het afvalwater en pompt het door een dunne leiding weg, zodat een toilet ook op een plek zonder klassieke afvoer kan."),
]

TOILETTEN = CARD_CSS + '''
<section class="hero">
  <div class="wrap">
    <div>
      <span class="eyebrow">Comfortabel en veilig naar het toilet</span>
      <h1>Toiletten<em>.</em></h1>
      <p class="lead">Een nieuw toilet, geplaatst in 1 dag: <strong>staand, hangend, verhoogd</strong> of een Japans douchetoilet. Comfort voor nu en voor later.</p>
      <div class="cta-row">
        <a class="btn" href="#contact">Plan je gratis adviesgesprek</a>
        <a class="btn btn--ghost" href="#toiletten">Bekijk de toiletten</a>
      </div>
    </div>
    <div class="media">
      <img src="/img/toiletten/hangtoilet.webp" alt="Hangtoilet geplaatst door CK Service" />
      <span class="logo badge"><b>CK</b><span>SERVICE</span></span>
    </div>
  </div>
</section>

<div class="trust">
  <div class="wrap">
    <div class="item"><b>1 dag</b> en je toilet is geplaatst</div>
    <div class="item"><b>Verhoogd</b> voor makkelijk opstaan</div>
    <div class="item"><b>Japans</b> douchetoilet voor extra hygiëne</div>
    <div class="item"><b>Eigen</b> vakmensen &amp; afwerking</div>
  </div>
</div>

<section class="block" id="toiletten">
  <div class="wrap center" style="margin-bottom:32px">
    <span class="eyebrow">Ons aanbod</span>
    <h2 class="h2">Welk toilet past bij jou?</h2>
    <p>Comfortabel in de eerste plaats, en gerust ook mooi. Het ene toilet is het andere niet.</p>
  </div>
  <div class="wrap ck-cards">
    <div class="ck-card"><img src="/img/toiletten/staand-toilet.webp" alt="Staand toilet" /><div class="b"><h3>Staand toilet</h3><p>Het klassieke toilet zoals we het kennen, van klassiek tot modern design.</p></div></div>
    <div class="ck-card"><img src="/img/toiletten/hangtoilet.webp" alt="Hangtoilet" /><div class="b"><h3>Hangtoilet</h3><p>Makkelijker te poetsen en je kiest zelf de hoogte. Ook in een compacte versie voor kleine ruimtes.</p></div></div>
    <div class="ck-card"><img src="/img/toiletten/verhoogd-toilet.webp" alt="Verhoogd toilet" /><div class="b"><h3>Verhoogd toilet</h3><p>Hogere zit, dus minder moeite bij het gaan zitten en opstaan. Te combineren met steunbeugels.</p></div></div>
    <div class="ck-card"><img src="/img/toiletten/lima-douchetoilet.webp" alt="Lima Japans douchetoilet" /><div class="b"><h3>Japans douchetoilet</h3><p>Reinigt met warm water en droogt met lucht. Verwarmde bril, automatisch deksel, geen wc-papier meer nodig.</p></div></div>
    <div class="ck-card"><img src="/img/toiletten/vergruizer.webp" alt="Toilet met vergruizer" /><div class="b"><h3>Toilet met vergruizer</h3><p>Voor een plek zonder klassieke afvoer: de vergruizer pompt het afvalwater door een dunne leiding weg.</p></div></div>
  </div>
</section>

<section class="block alt">
  <div class="wrap split">
    <div>
      <span class="eyebrow">Samen met je douche</span>
      <h2 class="h2">Eén dag, één ploeg, alles klaar</h2>
      <div class="prose">
        <p>Vervang je je bad door een veilige douche? Dan plaatsen we vaak meteen ook je nieuwe toilet. Onze eigen vakmensen doen alles in één beweging, met minimale breekwerken en alles netjes opgeruimd.</p>
      </div>
      <ul class="usp">
        <li>Geplaatst in 1 dag</li>
        <li>Verhoogd toilet of hangtoilet op de hoogte die jij kiest</li>
        <li>Douchetoilet voor extra comfort en hygiëne</li>
        <li>Eigen vakmensen, de zaakvoerder werkt mee</li>
      </ul>
      <p style="margin-top:18px"><a class="btn" href="/veilige-douche/">Van bad naar douche in 1 dag</a></p>
    </div>
    <img src="/img/toiletten/lima-douchetoilet.webp" alt="Lima douchetoilet" />
  </div>
</section>

''' + faq_block("Veelgestelde vragen", "Over toiletten", TOILET_QAS) + '''

<section class="block">
  <div class="wrap center" style="margin-bottom:28px">
    <span class="eyebrow">Ook interessant</span>
    <h2 class="h2">Andere oplossingen</h2>
  </div>
  <div class="wrap related">
    <a href="/veilige-douche/">Bad vervangen door een douche →</a>
    <a href="/inloopdouche/">Inloopdouche →</a>
    <a href="/badkamer-renovatie-wandpanelen/">Wandpanelen →</a>
    <a href="/premie/">Premie &amp; kosten →</a>
  </div>
</section>

''' + T.CTA_FORM.format(interest='toilet')

PAIRS = ['Geel', 'Aartselaar', 'Berchem', 'Schoten', 'Lommel', 'Diest', 'Hallaar', 'Evere', 'Zaventem', 'Gentbrugge', 'Destelbergen', 'Kerksken', 'Wachtebeke']

def voor_na_section():
    cards = ''.join(f'''    <div class="ck-pair"><div class="imgs"><img src="/img/voor-na/{c.lower()}-voor.webp" alt="Voor: badkamer in {c} vóór de renovatie door CK Service" loading="lazy" /><img src="/img/voor-na/{c.lower()}-na.webp" alt="Na: veilige douche in {c}, geplaatst door CK Service" loading="lazy" /></div><div class="lbl"><span>Voor</span><b>Na · {c}</b></div></div>
''' for c in PAIRS)
    return CARD_CSS + f'''
<section class="block alt" id="voor-en-na">
  <div class="wrap center" style="margin-bottom:32px">
    <span class="eyebrow">Voor en na</span>
    <h2 class="h2">Echte badkamers, echte klanten</h2>
    <p>Van oud bad naar veilige douche, telkens in één dag. Geen showroomfoto's: dit zijn realisaties bij onze klanten.</p>
  </div>
  <div class="wrap ck-cards">
{cards}  </div>
</section>

'''

def main():
    template = (ROOT / 'inloopdouche.html').read_text(encoding='utf-8')
    template = re.sub(r'<link rel="canonical".*?</script>\n(?=</head>)', '', template, flags=re.S)
    template = re.sub(r'<noscript><iframe src="https://www.googletagmanager.com[^\n]*\n', '', template)
    h = T.shell(template, 'Toilet plaatsen in 1 dag: staand, hangend, verhoogd of Japans | CK Service',
                'Een nieuw toilet geplaatst in 1 dag door CK Service: staand toilet, hangtoilet, verhoogd toilet, Japans douchetoilet of toilet met vergruizer. Comfortabel en veilig.', TOILETTEN, None)
    h = T.patch_forms(h); h = T.patch_head(h, 'toiletten.html')
    (ROOT / 'toiletten.html').write_text(h, encoding='utf-8')
    # realisaties: real before/after pairs before the CTA
    p = ROOT / 'projecten.html'; ph = p.read_text(encoding='utf-8')
    if 'id="voor-en-na"' not in ph:
        ph = ph.replace('<section class="cta"', voor_na_section() + '<section class="cta"', 1)
        p.write_text(ph, encoding='utf-8')
    # same post-patches as the other pages (GTM gate, header fix, logo)
    for f in ('toiletten.html',):
        x = (ROOT / f).read_text(encoding='utf-8')
        x = x.replace("<script>(function(w,d,s,l,i){w[l]=w[l]||[];", "<script>if(/(^|\\.)ckservice\\.be$/.test(location.hostname)||location.hostname==='localhost'){(function(w,d,s,l,i){w[l]=w[l]||[];", 1)
        x = x.replace("})(window,document,'script','dataLayer','GTM-T8J62JH');</script>", "})(window,document,'script','dataLayer','GTM-T8J62JH');}</script>", 1)
        x = x.replace(".hero .media img{background:#eaf0fb}", ".wrap.nav{padding:12px 24px} .nav .logo{flex:none} @media(max-width:880px){.nav{gap:12px}.nav .tel{font-size:1rem}.logo{font-size:1.2rem}}\n.hero .media img{background:#eaf0fb}", 1)
        x = x.replace('"logo": "https://ckservice.be/img/favicon-192.jpg"', '"logo": "https://ckservice.be/img/logo-ck-service.webp"').replace('"image": "https://ckservice.be/img/hero-vrouw.jpg", "logo"', '"image": "https://ckservice.be/img/logo-ck-service.webp", "logo"')
        (ROOT / f).write_text(x, encoding='utf-8')
    # footer: toiletten link under Diensten on every page
    for f in ROOT.glob('*.html'):
        x = f.read_text(encoding='utf-8')
        if '/onze-toiletten/' not in x:
            x = x.replace('<a href="/badkamer-renovatie-wandpanelen/">Wandpanelen</a><br/>', '<a href="/badkamer-renovatie-wandpanelen/">Wandpanelen</a><br/><a href="/onze-toiletten/">Toiletten</a><br/>', 1)
            f.write_text(x, encoding='utf-8')
    print('toiletten built; voor-na pairs:', ph.count('class="ck-pair"'))

if __name__ == '__main__':
    main()
