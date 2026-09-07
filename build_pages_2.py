#!/usr/bin/env python3
"""Step 1+2 of the post-launch build: /seniorendouches/ (brief 42) and
/veilige-douche/ (brief 41, bad→douche money page). Content = canonical brief
title/meta/PAA + CK's own live facts + the client-approved reference pattern.
Run from repo root after transform.py has produced the launch pages."""
import json, re, pathlib
import transform as T

ROOT = pathlib.Path(__file__).resolve().parent
T.PAGES['seniorendouches.html'] = '/seniorendouches/'
T.PAGES['veilige-douche.html'] = '/veilige-douche/'

def faq_jsonld(qas):
    return '<script type="application/ld+json">' + json.dumps({
        '@context': 'https://schema.org', '@type': 'FAQPage',
        'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': re.sub(r'<[^>]+>', '', a)}} for q, a in qas]
    }, ensure_ascii=False) + '</script>'

def faq_block(eyebrow, title, qas):
    items = ''.join(f'<h3>{q}</h3><p>{a}</p>' for q, a in qas)
    return f'''<section class="block alt" id="faq">
  <div class="wrap">
    <div class="center" style="margin-bottom:24px"><span class="eyebrow">{eyebrow}</span><h2 class="h2">{title}</h2></div>
    <div class="prose article" style="margin:0 auto">{items}</div>
  </div>
</section>
{faq_jsonld(qas)}'''

# ---------------------------------------------------------------------------
SENIOR_QAS = [
    ("Wat is een seniorendouche?", "Een douche die is aangepast aan wie minder mobiel wordt: een lage instap van zo'n 3 cm, een antisliplaag, stevige handgrepen en een opklapbaar zitje. Zo blijf je veilig en zelfstandig douchen in je eigen huis."),
    ("Wat kost een seniorendouche?", "Dat hangt af van je badkamer en de opties die je kiest (zitje, grepen, glas, wandpanelen). Je krijgt vooraf een heldere offerte zonder verrassingen, en wij zoeken de aanpassingspremie tot €1.250 voor je uit. Het adviesgesprek aan huis is gratis en vrijblijvend."),
    ("Hoe kan ik mijn badkamer aanpassen voor senioren?", "Meestal is het vervangen van het bad of de oude douche door een seniorendouche de grootste stap: geen hoge badrand meer, antislip onder je voeten en houvast waar je die nodig hebt. Wil je meer aanpassen, dan bekijken we dat samen tijdens het adviesgesprek."),
    ("Kan mijn oude bad of douchebak vervangen worden zonder veel breekwerk?", "Ja. We halen het oude bad of de oude douche weg, passen de afvoer en aansluitingen aan en plaatsen de nieuwe douche op één dag, met een minimum aan breekwerk, stofafzuiging en afvalafvoer inbegrepen."),
]

SENIOREN = f'''<section class="hero">
  <div class="wrap">
    <div>
      <span class="eyebrow">Veilig en zelfstandig blijven douchen</span>
      <h1>Senioren&shy;douche<em>.</em></h1>
      <p class="lead">Een lage instap van zo'n <strong>3 cm</strong>, antislip, stevige handgrepen en een opklapbaar zitje. Geplaatst in 1 dag door onze eigen vakmensen, zodat je thuis veilig blijft douchen.</p>
      <div class="cta-row">
        <a class="btn" href="#contact">Plan je gratis adviesgesprek</a>
        <a class="btn btn--ghost" href="#premie">Check je premie</a>
      </div>
    </div>
    <div class="media">
      <img src="/img/products/serenite-plus.jpg" alt="Seniorendouche met zitje en handgrepen, geplaatst door CK Service" />
      <span class="logo badge"><b>CK</b><span>SERVICE</span></span>
    </div>
  </div>
</section>

<div class="trust">
  <div class="wrap">
    <div class="item"><b>3 cm</b> lage instap</div>
    <div class="item"><b>Antislip</b> &amp; handgrepen</div>
    <div class="item"><b>Zitje</b> opklapbaar</div>
    <div class="item"><b>tot €1.250</b> aanpassingspremie</div>
  </div>
</div>

<section class="block">
  <div class="wrap split">
    <div>
      <span class="eyebrow">Ongelukken zijn snel gebeurd</span>
      <h2 class="h2">Een badkamer die met je meegroeit</h2>
      <div class="prose">
        <p>Zo lang mogelijk thuis blijven wonen: dat willen de meeste mensen. Alleen is de badkamer daar zelden op voorzien. De stap over de badrand of een gladde douchebak zorgt snel voor gevaarlijke situaties.</p>
        <p>CK Service vervangt je huidige bad of douche door een seniorendouche. Veiligheid kiezen is gezond verstand, niet oud worden.</p>
      </div>
      <ul class="usp">
        <li>Lage instap van zo'n 3 cm, of volledig drempelloos ingebouwd</li>
        <li>Antisliplaag tegen uitglijden</li>
        <li>Handgrepen voor extra steun bij in- en uitstappen</li>
        <li>Opklapbaar douchezitje dat niemand in de weg staat</li>
        <li>Geplaatst in 1 dag, minimale breekwerken</li>
        <li>Eigen vakmensen, de zaakvoerder werkt mee</li>
      </ul>
    </div>
    <img src="/img/seniorendouche-plaatsen.jpg" alt="Geplaatste seniorendouche met lage instap in een badkamer van een klant van CK Service" />
  </div>
</section>

<section class="block alt">
  <div class="wrap">
    <div class="center">
      <span class="eyebrow">Zo gaan we te werk</span>
      <h2 class="h2">Vandaag beslissen, morgen genieten</h2>
      <p>Van het eerste gesprek tot de laatste uitleg: wij ontzorgen je.</p>
    </div>
    <div class="steps">
      <div class="step"><div class="n">1</div><h3>Voorbereiding</h3><p>We overlopen samen de plannen, sluiten het water af en beschermen je badkamer.</p></div>
      <div class="step"><div class="n">2</div><h3>Afbraak</h3><p>Je oude bad of douche gaat eruit, afvoer en aansluitingen worden aangepast. Het oude materiaal nemen we mee.</p></div>
      <div class="step"><div class="n">3</div><h3>Plaatsing</h3><p>Douchebak, glas en wandpanelen, daarna handgrepen en zitje naar keuze.</p></div>
      <div class="step"><div class="n">4</div><h3>Controle en uitleg</h3><p>We testen alles, leggen uit hoe je de douche gebruikt en onderhoudt, en laten je badkamer netjes achter.</p></div>
    </div>
  </div>
</section>

<section class="premie" id="premie">
  <div class="wrap">
    <img src="/img/premie-500.jpg" alt="Laat je premie niet door de afvoer verdwijnen" />
    <div>
      <span class="eyebrow">Geen geld door de afvoer</span>
      <h2 class="h2">Premie tot €1.250 voor je seniorendouche</h2>
      <p class="prose">Voor de aanpassing van je badkamer bestaat een aanpassingspremie tot €1.250. Wij zoeken uit waar je recht op hebt en helpen je met de aanvraag.</p>
      <p style="margin-top:18px"><a class="btn" href="#contact">Bereken mijn premie</a></p>
    </div>
  </div>
</section>

{faq_block("Veelgestelde vragen", "Alles over de seniorendouche", SENIOR_QAS)}

<section class="block">
  <div class="wrap center" style="margin-bottom:28px">
    <span class="eyebrow">Ook interessant</span>
    <h2 class="h2">Andere oplossingen</h2>
  </div>
  <div class="wrap related">
    <a href="/veilige-douche/">Bad vervangen door een douche →</a>
    <a href="/inloopdouche/">Inloopdouche →</a>
    <a href="/douchecabine/">Douchecabine →</a>
    <a href="/premie/">Premie &amp; kosten →</a>
  </div>
</section>

''' + T.CTA_FORM.format(interest='seniorendouche')

# ---------------------------------------------------------------------------
VD_QAS = [
    ("Wat kost het om een bad te vervangen door een inloopdouche?", "Er is geen vaste prijs: het hangt af van je badkamer, de douche die je kiest en de afwerking. Je krijgt vooraf een heldere offerte zonder verrassingen achteraf, en we verrekenen de aanpassingspremie tot €1.250 waar je recht op hebt. Het adviesgesprek aan huis is gratis."),
    ("Kan ik een inloopdouche in mijn bestaande badkamer plaatsen?", "Ja. In de meeste badkamers komt de nieuwe douche op de plaats van het oude bad. We passen de afvoer en aansluitingen aan en werken alles netjes af, in 1 dag."),
    ("Hoe lang duurt het om een bad te vervangen door een douche?", "Eén dag. 's Morgens gaat je oude bad eruit, 's avonds staat je veilige douche klaar. Dankzij ons douchesysteem zonder siliconen kun je ze meteen gebruiken."),
    ("Wat zijn de nadelen van een inloopdouche?", "Een open inloopdouche zonder deur kan spatwater geven en vraagt voldoende ruimte. Daarom bekijken we tijdens het adviesgesprek welke oplossing bij jouw badkamer past: een inloopdouche met glazen wand, een douchecabine of een seniorendouche met zitje."),
]

VEILIGE = f'''<section class="hero">
  <div class="wrap">
    <div>
      <span class="eyebrow">Veilige inloopdouche in 1 dag</span>
      <h1>Van bad naar douche<em>.</em></h1>
      <p class="lead">De stap over de badrand wordt elke dag iets hoger. <strong>Veiligheid kiezen is gezond verstand, niet oud worden:</strong> je oude bad eruit, een veilige drempelloze douche erin, in 1 dag.</p>
      <div class="cta-row">
        <a class="btn" href="#contact">Plan je gratis adviesgesprek</a>
        <a class="btn btn--ghost" href="#premie">Check je premie</a>
      </div>
    </div>
    <div class="media">
      <img src="/img/projecten/veilig-douchen-na.webp" alt="Badkamer na de renovatie: veilige douche op de plaats van het oude bad, geplaatst door CK Service" />
      <span class="logo badge"><b>CK</b><span>SERVICE</span></span>
    </div>
  </div>
</section>

<div class="trust">
  <div class="wrap">
    <div class="item"><b>1 dag</b> van bad naar douche</div>
    <div class="item"><b>Antislip</b>, zitje &amp; grepen</div>
    <div class="item"><b>tot €1.250</b> aanpassingspremie</div>
    <div class="item"><b>Eigen</b> vakmensen &amp; afwerking</div>
  </div>
</div>

<section class="block">
  <div class="wrap split">
    <div>
      <span class="eyebrow">Waarom je bad vervangen</span>
      <h2 class="h2">Een mooie, comfortabele en veilige douche</h2>
      <div class="prose">
        <p>In en uit het bad stappen is voor veel mensen de gevaarlijkste beweging van de dag. Een douche van CK Service combineert design, comfort en veiligheid: antislip afwerking, een uitklapbaar zitje en ergonomische veiligheidsgrepen.</p>
        <p>Geen zin in een lange verbouwing? Dat hoeft niet. In 1 dag vervangen we je bad door een veilige douche, en dankzij ons douchesysteem zonder siliconen kun je ze meteen gebruiken.</p>
      </div>
      <ul class="usp">
        <li>Drempelloze of lage instap, antislip onder je voeten</li>
        <li>Uitklapbaar zitje en ergonomische grepen naar keuze</li>
        <li>Douchebak en glazen panelen in 1 dag geplaatst</li>
        <li>Zonder siliconen, meteen te gebruiken</li>
        <li>Minimale breekwerken, stofafzuiging en afvalafvoer inbegrepen</li>
        <li>Eigen vakmensen, de zaakvoerder werkt mee</li>
      </ul>
    </div>
    <img src="/img/seniorendouche-plaatsen.jpg" alt="Nieuwe veilige douche op de plaats van het oude bad bij een klant van CK Service" />
  </div>
</section>

<section class="block alt">
  <div class="wrap">
    <div class="center">
      <span class="eyebrow">Zo gaan we te werk</span>
      <h2 class="h2">'s Morgens je bad, 's avonds je douche</h2>
      <p>Vier stappen, één dag. Wij ontzorgen je van begin tot eind.</p>
    </div>
    <div class="steps">
      <div class="step"><div class="n">1</div><h3>Voorbereiden</h3><p>We overlopen de plannen, sluiten het water af en beschermen je badkamer tegen schade.</p></div>
      <div class="step"><div class="n">2</div><h3>Afbreken</h3><p>Je oude bad gaat eruit, het oude materiaal gaat mee. Aansluitingen en afvoer passen we aan op je nieuwe douche.</p></div>
      <div class="step"><div class="n">3</div><h3>Plaatsen</h3><p>Eerst de douchebak, dan de glazen panelen. Zonder siliconen, dus meteen bruikbaar.</p></div>
      <div class="step"><div class="n">4</div><h3>Testen en opruimen</h3><p>We testen alles, leggen uit hoe je de douche onderhoudt en laten je badkamer netjes achter.</p></div>
    </div>
  </div>
</section>

<section class="block">
  <div class="wrap center" style="margin-bottom:28px">
    <span class="eyebrow">Voor en na</span>
    <h2 class="h2">Zo ziet badkamergevoel eruit</h2>
    <p>Eén van onze realisaties: van bad naar veilige douche, in één dag.</p>
  </div>
  <div class="wrap split">
    <img src="/img/projecten/veilig-douchen-voor.jpg" alt="Voor: badkamer met oud bad" />
    <img src="/img/projecten/veilig-douchen-na.webp" alt="Na: veilige douche met lage instap op de plaats van het bad" />
  </div>
</section>

<section class="premie" id="premie">
  <div class="wrap">
    <img src="/img/premie-500.jpg" alt="Laat je premie niet door de afvoer verdwijnen" />
    <div>
      <span class="eyebrow">Geen geld door de afvoer</span>
      <h2 class="h2">Premie tot €1.250 als je je bad vervangt</h2>
      <p class="prose">Vervang je je bad door een veilige douche, dan kom je mogelijk in aanmerking voor de aanpassingspremie tot €1.250. Wij zoeken het uit en verrekenen waar je recht op hebt.</p>
      <p style="margin-top:18px"><a class="btn" href="#contact">Bereken mijn premie</a></p>
    </div>
  </div>
</section>

{faq_block("Veelgestelde vragen", "Bad vervangen door een douche", VD_QAS)}

<section class="block">
  <div class="wrap center" style="margin-bottom:28px">
    <span class="eyebrow">Welke douche past bij jou?</span>
    <h2 class="h2">Kies je oplossing</h2>
  </div>
  <div class="wrap related">
    <a href="/inloopdouche/">Inloopdouche →</a>
    <a href="/seniorendouches/">Seniorendouche →</a>
    <a href="/douchecabine/">Douchecabine →</a>
    <a href="/premie/">Premie &amp; kosten →</a>
  </div>
</section>

''' + T.CTA_FORM.format(interest='bad vervangen door douche')

def main():
    template = T.fix_links((ROOT / 'inloopdouche.html').read_text(encoding='utf-8')) if 'href="/inloopdouche/"' not in (ROOT / 'inloopdouche.html').read_text(encoding='utf-8') else (ROOT / 'inloopdouche.html').read_text(encoding='utf-8')
    # template head must be the clean one: strip a previously injected head block
    template = re.sub(r'<link rel="canonical".*?</script>\n(?=</head>)', '', template, flags=re.S)
    template = re.sub(r'<noscript><iframe src="https://www.googletagmanager.com[^\n]*\n', '', template)
    pages = {
        'seniorendouches.html': ('Seniorendouche plaatsen in 1 dag | CK Service',
            'Een seniorendouche met zitje, beugels en antislip, drempelvrij geplaatst in 1 dag. Zo blijf je veilig en zelfstandig douchen in je eigen huis. Premie tot €1.250.', SENIOREN, '/inloopdouche/'),
        'veilige-douche.html': ('Bad vervangen door een inloopdouche in 1 dag | CK Service',
            'Je bad vervangen door een veilige, drempelloze inloopdouche? CK Service doet het in 1 dag: kosten, stappenplan, premie tot €1.250 en eigen vakmensen. Gewoon gezond verstand.', VEILIGE, None),
    }
    for fname, (title, desc, body, cur) in pages.items():
        h = T.shell(template, title, desc, body, cur)
        h = T.patch_forms(h)
        h = T.patch_head(h, fname)
        (ROOT / fname).write_text(h, encoding='utf-8')
    # link mesh: add the two pages to the related blocks of the sibling service pages
    for fname, add in (('inloopdouche.html', ['/veilige-douche/|Bad vervangen door een douche →', '/seniorendouches/|Seniorendouche →']),
                       ('douchecabine.html', ['/veilige-douche/|Bad vervangen door een douche →', '/seniorendouches/|Seniorendouche →']),
                       ('douche-plaatsen.html', ['/veilige-douche/|Bad vervangen door een douche →', '/seniorendouches/|Seniorendouche →'])):
        p = ROOT / fname; h = p.read_text(encoding='utf-8')
        links = ''.join(f'\n    <a href="{a.split("|")[0]}">{a.split("|")[1]}</a>' for a in add if a.split('|')[0] not in h)
        h = h.replace('<div class="wrap related">', '<div class="wrap related">' + links, 1)
        p.write_text(h, encoding='utf-8')
    print('built', list(pages), 'canonicals:', [re.search(r'rel="canonical" href="([^"]+)"', (ROOT / f).read_text()).group(1) for f in pages])

if __name__ == '__main__':
    main()
