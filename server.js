'use strict';
/**
 * ckservice.be — static site server + lead relay (no dependencies).
 *
 * WHAT THIS IS (CLIENT DELIVERY EXCEPTION, CK Service, 2026-09):
 *  - serves the client-approved reference pages under clean URLs (/inloopdouche/),
 *  - carries the 301 map that preserves every URL of the previous WordPress site,
 *  - relays the contact form: canonical lead evidence goes to Sherlock
 *    (POST /api/leads/capture — ConversionEvent + GA4), the client notification
 *    goes out via Resend. The relay is TRANSPORT + NOTIFICATION only; it stores
 *    nothing and is not a second lead truth.
 *  - EXPIRY: when Sherlock's lead-capture pipeline notifies the site contact
 *    itself (email_service wiring), drop the Resend step here.
 *
 * Secrets come from the environment only (Coolify): RESEND_API_KEY, LEAD_TO,
 * LEAD_FROM, LEAD_BCC, SHERLOCK_CAPTURE_URL, SITE_DOMAIN. Nothing is committed.
 */
const http = require('http');
const fs = require('fs');
const path = require('path');
const { URL } = require('url');

const PORT = parseInt(process.env.PORT || '80', 10);
const ROOT = __dirname;
const SITE_DOMAIN = process.env.SITE_DOMAIN || 'ckservice.be';
const ORIGIN = `https://${SITE_DOMAIN}`;
const RESEND_API_KEY = process.env.RESEND_API_KEY || '';
const LEAD_TO = (process.env.LEAD_TO || 'info@ckservice.be').split(',').map(s => s.trim()).filter(Boolean);
const LEAD_BCC = (process.env.LEAD_BCC || '').split(',').map(s => s.trim()).filter(Boolean);
const LEAD_FROM = process.env.LEAD_FROM || 'CK Service website <leads@sherlockseo.com>';
const SHERLOCK_CAPTURE_URL = process.env.SHERLOCK_CAPTURE_URL || 'https://mcp-audit-platform-production.up.railway.app/api/leads/capture';
const LEAD_DRY_RUN = process.env.LEAD_DRY_RUN === '1';

// ---------------------------------------------------------------------------
// Page map: clean URL -> html file. Order = sitemap order.
// ---------------------------------------------------------------------------
const PAGES = {
  '/': 'index.html',
  '/inloopdouche/': 'inloopdouche.html',
  '/veilige-douche/': 'veilige-douche.html',
  '/seniorendouches/': 'seniorendouches.html',
  '/onze-toiletten/': 'toiletten.html',
  '/douchecabine/': 'douchecabine.html',
  '/douche-plaatsen/': 'douche-plaatsen.html',
  '/badkamer-renovatie-wandpanelen/': 'wandpanelen.html',
  '/premie/': 'premie.html',
  '/badkamer-renovatie-geel/': 'badkamer-renovatie-geel.html',
  '/onze-projecten/': 'projecten.html',
  '/over-ons/': 'over-ons.html',
  '/faq/': 'faq.html',
  '/contact/': 'contact.html',
  '/privacy-verklaring/': 'privacy-verklaring.html',
  '/cookiebeleid/': 'cookiebeleid.html',
  '/disclaimer/': 'disclaimer.html',
  '/bedankt/': 'bedankt.html',
};
const NOINDEX = new Set(['/bedankt/']);

// 301 map for every URL of the previous site (page-sitemap.xml 2026-09-07) and
// the reference's .html paths. Target = the canonical surface per proposal 123
// where the reference has a page; otherwise the closest existing page.
const REDIRECTS = {
  '/index.html': '/',
  '/onze-douches/': '/douchecabine/',
  '/kocoon/': '/douchecabine/',
  '/vervang-je-bad-door-een-veilige-kinemagic-douchecabine/': '/veilige-douche/',
  '/voor-en-na/': '/onze-projecten/',
  '/projecten/page/2/': '/projecten/',
  '/projecten/page/3/': '/projecten/',
  '/projecten/page/4/': '/projecten/',
  '/blog/': '/',
  '/blog-post/': '/premie/',
  '/wp-content/uploads/2024/02/CK-Service-ROCKO_TILES.pdf': '/docs/CK-Service-ROCKO_TILES.pdf',
  '/wp-content/uploads/2024/03/CK-Service-Wandpanelen-1.pdf': '/docs/CK-Service-Wandpanelen.pdf',
  '/wp-content/uploads/2020/05/algemene-aannemingsvoorwaarden-CK-Service.pdf': '/docs/algemene-aannemingsvoorwaarden-CK-Service.pdf',
  '/page-sitemap.xml': '/sitemap.xml',
  '/sitemap_index.xml': '/sitemap.xml',
  '/wp-sitemap.xml': '/sitemap.xml',
};
// The 22 /faq/<slug>/ pages and /projecten/ (realisation index) are now real
// pages (see faq/*.html, projecten/*.html, projecten/index.html) — no longer
// redirected. Directory-based routing for both lives further down.


const MIME = {
  '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.js': 'application/javascript; charset=utf-8',
  '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png', '.webp': 'image/webp', '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon', '.pdf': 'application/pdf', '.xml': 'application/xml; charset=utf-8', '.txt': 'text/plain; charset=utf-8',
  '.woff2': 'font/woff2', '.json': 'application/json; charset=utf-8',
};

function log(obj) { process.stdout.write(JSON.stringify({ ts: new Date().toISOString(), ...obj }) + '\n'); }

function securityHeaders(res, extra) {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');
  res.setHeader('X-Frame-Options', 'SAMEORIGIN');
  res.setHeader('Permissions-Policy', 'camera=(), microphone=(), geolocation=()');
  if (extra) for (const [k, v] of Object.entries(extra)) res.setHeader(k, v);
}

function sendFile(res, file, status, headers) {
  const abs = path.join(ROOT, file);
  fs.readFile(abs, (err, data) => {
    if (err) return notFound(res);
    const ext = path.extname(abs).toLowerCase();
    securityHeaders(res, headers);
    res.setHeader('Content-Type', MIME[ext] || 'application/octet-stream');
    res.setHeader('Cache-Control', ext === '.html' ? 'no-cache' : 'public, max-age=604800');
    res.writeHead(status || 200);
    res.end(data);
  });
}

function notFound(res) {
  sendFile(res, '404.html', 404, { 'X-Robots-Tag': 'noindex' });
}

function redirect(res, location, status) {
  securityHeaders(res);
  res.writeHead(status || 301, { Location: location, 'Cache-Control': 'no-cache' });
  res.end();
}

// Directory-based pages (ported 1:1 from the live site): read once at
// startup, same as PAGES above but keyed by slug instead of a fixed map.
function listDirPages(dir, prefix) {
  try {
    return fs.readdirSync(path.join(ROOT, dir))
      .filter(f => f.endsWith('.html') && f !== 'index.html')
      .map(f => `${prefix}${f.slice(0, -5)}/`);
  } catch (e) { return []; }
}
const FAQ_PAGES = listDirPages('faq', '/faq/');
const PROJECT_PAGES = listDirPages('projecten', '/projecten/');

function sitemap() {
  const today = new Date().toISOString().slice(0, 10);
  const all = [...Object.keys(PAGES).filter(p => !NOINDEX.has(p)), '/projecten/', ...FAQ_PAGES, ...PROJECT_PAGES];
  const urls = all.map(p => `  <url><loc>${ORIGIN}${p}</loc><lastmod>${today}</lastmod></url>`).join('\n');
  return `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls}\n</urlset>\n`;
}

// ---------------------------------------------------------------------------
// Lead relay
// ---------------------------------------------------------------------------
const rate = new Map(); // ip -> [timestamps]
function rateLimited(ip) {
  const now = Date.now();
  const hits = (rate.get(ip) || []).filter(t => now - t < 60000);
  if (hits.length >= 10) { rate.set(ip, hits); return true; }
  hits.push(now); rate.set(ip, hits); return false;
}

function parseBody(req) {
  return new Promise((resolve, reject) => {
    let raw = '';
    req.on('data', c => { raw += c; if (raw.length > 20000) { reject(new Error('too_large')); req.destroy(); } });
    req.on('end', () => {
      const ct = (req.headers['content-type'] || '');
      try {
        if (ct.includes('application/json')) return resolve(JSON.parse(raw || '{}'));
        const out = {}; for (const [k, v] of new URLSearchParams(raw)) out[k] = v; resolve(out);
      } catch (e) { reject(e); }
    });
    req.on('error', reject);
  });
}

const esc = s => String(s || '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

async function withRetry(fn, attempts) {
  let last;
  for (let i = 0; i < attempts; i++) {
    try { return await fn(); } catch (e) { last = e; await new Promise(r => setTimeout(r, 500 * (i + 1))); }
  }
  throw last;
}

async function sendNotification(lead) {
  if (!RESEND_API_KEY && !LEAD_DRY_RUN) throw new Error('resend_not_configured');
  const rows = [
    ['Naam', lead.name], ['Telefoon', lead.phone], ['E-mail', lead.email || '—'],
    ['Interesse', lead.interest || '—'], ['Bericht', lead.message || '—'],
    ['Pagina', lead.landing_page || '—'], ['Marketingtoestemming', lead.consent ? 'ja' : 'nee'],
    ['Bron', lead.attribution.gclid ? 'Google Ads (gclid)' : (lead.attribution.referrer || 'direct')],
  ].map(([k, v]) => `<tr><td style="padding:6px 12px 6px 0;color:#5a626c">${esc(k)}</td><td style="padding:6px 0"><strong>${esc(v)}</strong></td></tr>`).join('');
  const html = `<div style="font-family:Arial,sans-serif;font-size:15px;color:#21262e"><p>Nieuwe aanvraag via ckservice.be:</p><table>${rows}</table><p style="color:#5a626c;font-size:13px">Bel de klant zo snel mogelijk terug. Deze mail is automatisch verstuurd door de website.</p></div>`;
  const body = {
    from: LEAD_FROM, to: LEAD_TO, subject: `Nieuwe aanvraag: ${lead.name} (${lead.phone})`, html,
  };
  if (LEAD_BCC.length) body.bcc = LEAD_BCC;
  if (lead.email) body.reply_to = lead.email;
  if (LEAD_DRY_RUN) { log({ event: 'lead_mail_dry_run', to: LEAD_TO }); return { dry_run: true }; }
  const r = await fetch('https://api.resend.com/emails', {
    method: 'POST', headers: { Authorization: `Bearer ${RESEND_API_KEY}`, 'Content-Type': 'application/json' }, body: JSON.stringify(body),
  });
  if (!r.ok) throw new Error(`resend_${r.status}`);
  return r.json();
}

async function sendSherlockCapture(lead) {
  // Canonical lead evidence. Sherlock requires a well-formed email; a phone-only
  // lead is notified but cannot be captured (documented gap, never invented).
  if (!lead.email) return { skipped: 'no_email' };
  const payload = {
    site: SITE_DOMAIN, name: lead.name, email: lead.email, phone: lead.phone,
    message: [lead.interest ? `Interesse: ${lead.interest}` : '', lead.message || ''].filter(Boolean).join('\n'),
    consent: !!lead.consent, hp: '', t0: lead.t0 || null,
    attribution: { ...lead.attribution, landing_page: lead.landing_page || '' },
  };
  if (LEAD_DRY_RUN) { log({ event: 'lead_capture_dry_run' }); return { dry_run: true }; }
  const r = await fetch(SHERLOCK_CAPTURE_URL, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
  const text = await r.text();
  if (!r.ok) throw new Error(`sherlock_${r.status}:${text.slice(0, 200)}`);
  return text.slice(0, 300);
}

async function handleLead(req, res, ip) {
  if (rateLimited(ip)) { securityHeaders(res); res.writeHead(429, { 'Content-Type': 'text/plain; charset=utf-8' }); return res.end('Te veel aanvragen. Bel ons op 0493 33 39 88.'); }
  let b;
  try { b = await parseBody(req); } catch (e) { securityHeaders(res); res.writeHead(400); return res.end('bad request'); }
  const name = String(b.naam || b.name || '').trim().slice(0, 200);
  const phone = String(b.tel || b.phone || '').trim().slice(0, 64);
  const email = String(b.email || '').trim().toLowerCase().slice(0, 320);
  const message = String(b.bericht || b.message || '').trim().slice(0, 5000);
  const interest = String(b.dienst || b.interesse || '').trim().slice(0, 120);
  const consent = b.consent === 'on' || b.consent === 'true' || b.consent === true || b.consent === '1';
  const hp = String(b.website || b.hp || '');
  const t0 = parseInt(b.t0 || '0', 10) || 0;
  const attribution = {};
  for (const k of ['gclid', 'wbraid', 'gbraid', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'referrer', 'ga_client_id']) {
    if (b[k]) attribution[k] = String(b[k]).slice(0, 300);
  }
  const landing_page = String(b.page || '').slice(0, 300);

  // Bot traps: honeypot filled or submitted within 2 s of render -> silent no-op.
  if (hp || (t0 && Date.now() - t0 < 2000)) { log({ event: 'lead_bot_noop', ip }); return redirect(res, '/bedankt/', 303); }
  const digits = phone.replace(/\D/g, '');
  const emailOk = !email || /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email);
  if (name.length < 2 || digits.length < 8 || !emailOk) {
    securityHeaders(res); res.writeHead(303, { Location: '/contact/?fout=1' }); return res.end();
  }
  const lead = { name, phone, email, message, interest, consent, t0, attribution, landing_page };
  const result = { notified: false, captured: false };
  try { await withRetry(() => sendNotification(lead), 3); result.notified = true; }
  catch (e) { result.notify_error = String(e.message || e); }
  try { const r = await withRetry(() => sendSherlockCapture(lead), 2); result.captured = !(r && r.skipped); result.capture = r && r.skipped ? r.skipped : 'ok'; }
  catch (e) { result.capture_error = String(e.message || e).slice(0, 200); }
  log({ event: 'lead', ip, name_len: name.length, has_email: !!email, interest, consent, gclid: !!attribution.gclid, ...result });
  if (!result.notified) {
    // The client would not see this lead: tell the visitor to call, never pretend.
    log({ event: 'lead_ALERT_notification_failed', ip });
    return sendFile(res, 'contact.html', 503, { 'X-Robots-Tag': 'noindex', 'X-Lead-Status': 'notify_failed' });
  }
  return redirect(res, '/bedankt/', 303);
}

// ---------------------------------------------------------------------------
// Server
// ---------------------------------------------------------------------------
const server = http.createServer(async (req, res) => {
  const ip = (req.headers['x-forwarded-for'] || req.socket.remoteAddress || '').split(',')[0].trim();
  const host = (req.headers['x-forwarded-host'] || req.headers.host || '').split(':')[0].toLowerCase();
  let u;
  try { u = new URL(req.url, ORIGIN); } catch (e) { securityHeaders(res); res.writeHead(400); return res.end(); }
  let p = u.pathname.replace(/\/{2,}/g, '/');

  if (host === `www.${SITE_DOMAIN}`) return redirect(res, ORIGIN + p + u.search, 301);
  // Preview/any non-production host: never indexable. Only the production domain is index,follow.
  const isProd = host === SITE_DOMAIN;

  if (req.method === 'POST' && p === '/api/lead') return handleLead(req, res, ip);
  if (req.method !== 'GET' && req.method !== 'HEAD') { securityHeaders(res); res.writeHead(405); return res.end(); }

  if (p === '/health') { securityHeaders(res); res.writeHead(200, { 'Content-Type': 'text/plain' }); return res.end('ok'); }
  if (p === '/sitemap.xml') { securityHeaders(res); res.writeHead(200, { 'Content-Type': MIME['.xml'], 'Cache-Control': 'no-cache' }); return res.end(sitemap()); }
  if (p === '/robots.txt') { securityHeaders(res); res.writeHead(200, { 'Content-Type': MIME['.txt'] }); return res.end(isProd ? `User-agent: *\nAllow: /\nDisallow: /api/\nDisallow: /bedankt/\nSitemap: ${ORIGIN}/sitemap.xml\n` : `User-agent: *\nDisallow: /\n`); }

  // .html -> clean URL
  if (/\.html$/.test(p)) {
    const clean = Object.entries(PAGES).find(([, f]) => '/' + f === p);
    return redirect(res, (clean ? clean[0] : '/') + u.search, 301);
  }
  // explicit legacy map (with and without trailing slash)
  const key = p.endsWith('/') ? p : p + '/';
  if (REDIRECTS[p] !== undefined) return redirect(res, REDIRECTS[p] + u.search, 301);
  if (REDIRECTS[key] !== undefined) return redirect(res, REDIRECTS[key] + u.search, 301);
  const noindexExtra = !isProd ? { 'X-Robots-Tag': 'noindex, nofollow' } : undefined;
  // /projecten/ — realisation index + one real page per slug (projecten/*.html)
  if (p === '/projecten' || p === '/projecten/') {
    if (!p.endsWith('/')) return redirect(res, '/projecten/' + u.search, 301);
    return sendFile(res, 'projecten/index.html', 200, noindexExtra);
  }
  if (p.startsWith('/projecten/')) {
    const m = key.match(/^\/projecten\/([a-z0-9-]+)\/$/);
    const file = m && `projecten/${m[1]}.html`;
    if (file && fs.existsSync(path.join(ROOT, file))) {
      if (!p.endsWith('/')) return redirect(res, key + u.search, 301);
      return sendFile(res, file, 200, noindexExtra);
    }
    // unknown slug: fall through to static/404 below
  }
  // /faq/ — hub (PAGES) + one real page per slug (faq/*.html); anything else
  // under /faq/ (a stale or unknown slug) redirects to the hub, as before.
  if (p.startsWith('/faq/') && p !== '/faq/') {
    const m = key.match(/^\/faq\/([a-z0-9-]+)\/$/);
    const file = m && `faq/${m[1]}.html`;
    if (file && fs.existsSync(path.join(ROOT, file))) {
      if (!p.endsWith('/')) return redirect(res, key + u.search, 301);
      return sendFile(res, file, 200, noindexExtra);
    }
    return redirect(res, '/faq/', 301);
  }
  // pages: enforce trailing slash
  if (PAGES[key] && !p.endsWith('/')) return redirect(res, key + u.search, 301);
  if (PAGES[p]) return sendFile(res, PAGES[p], 200, (!isProd || NOINDEX.has(p)) ? { 'X-Robots-Tag': 'noindex, nofollow' } : undefined);

  // static assets (css/img/js/docs, favicon)
  if (/^\/(css|img|js|docs)\//.test(p) || /^\/(favicon\.ico|favicon-\d+\.jpg|apple-touch-icon\.png)$/.test(p)) {
    const safe = path.normalize(p).replace(/^(\.\.[/\\])+/, '');
    if (safe.includes('..')) return notFound(res);
    if (p === '/favicon.ico') return sendFile(res, 'img/favicon-32.jpg');
    return sendFile(res, safe);
  }
  return notFound(res);
});

server.listen(PORT, () => log({ event: 'listening', port: PORT, domain: SITE_DOMAIN, resend: !!RESEND_API_KEY, dry_run: LEAD_DRY_RUN }));
