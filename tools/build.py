#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""בונה את האתר מ-tools/source (הדפים המקוריים), tools/config.py ו-tools/guides.py.
מריצים מתיקיית האתר: python3 tools/build.py"""
import json, os, re, sys, warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)
from urllib.parse import quote
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import config as C
from guides import GUIDES

SRC = os.path.join(HERE, 'source')
FONT = 'https://fonts.googleapis.com/css2?family=Heebo:wght@400;500;600;700;800;900&display=swap'
HAS_LOGO = os.path.exists(os.path.join(ROOT, 'assets/logo.webp'))
HAS_HERO = os.path.exists(os.path.join(ROOT, 'assets/hero-pipes.jpg'))
TEL = re.sub(r'\D', '', C.PHONE)
WA = '972' + TEL[1:] if TEL else ''
WA_TEXT = 'שלום, יש לי תקלת אינסטלציה. אפשר לקבל מחיר?'
WA_LINK = 'https://wa.me/%s?text=%s' % (WA, quote(WA_TEXT)) if WA else ''
PHONE_SVG = '<svg aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"></path></svg>'
ISSUES = ['סתימה', 'נזילה / רטיבות', 'פיצוץ צנרת', 'ניאגרה / אסלה', 'אחר']
CARD_ISSUE = {'פתיחת סתימות': 'סתימה', 'איתור נזילות במצלמה תרמית': 'נזילה / רטיבות', 'תיקון פיצוצי צנרת': 'פיצוץ צנרת', 'ניאגרות ואסלות סמויות': 'ניאגרה / אסלה'}


def write(rel, text):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)


def ld(obj):
    return '<script type="application/ld+json">%s</script>' % json.dumps(obj, ensure_ascii=False, separators=(',', ':'))


def business():
    b = {'@context': 'https://schema.org', '@type': 'Plumber', 'name': C.BRAND, 'url': C.DOMAIN + '/',
         'image': C.DOMAIN + '/assets/og-image.jpg',
         'description': 'אינסטלטור באזור המרכז: פתיחת סתימות, איתור נזילות במצלמה תרמית ותיקון פיצוצי צנרת, 24 שעות ביממה.',
         'priceRange': '₪₪', 'openingHours': 'Mo-Su 00:00-23:59',
         'address': {'@type': 'PostalAddress', 'addressRegion': 'מחוז המרכז', 'addressCountry': 'IL'},
         'areaServed': [{'@type': 'City', 'name': n, 'url': '%s/%s/' % (C.DOMAIN, s)} for s, n, _ in C.CITIES]}
    if TEL:
        b['telephone'] = '+972-' + TEL[1:]
    if HAS_LOGO:
        b['logo'] = C.DOMAIN + '/assets/logo.webp'
    return b


def head(title, desc, path, extra='', robots='index, follow', og_type='website'):
    url = C.DOMAIN + path
    site = {'leadEmail': C.LEAD_EMAIL, 'sheet': C.SHEET_ENDPOINT, 'ads': C.ADS_ID, 'ga4': C.GA4_ID,
            'labels': C.ADS_LABELS, 'phone': C.PHONE, 'tel': TEL, 'wa': WA}
    gid = C.ADS_ID or C.GA4_ID
    gtag = '<script async src="https://www.googletagmanager.com/gtag/js?id=%s"></script>\n' % gid if gid else ''
    preload = '<link rel="preload" as="image" href="/assets/hero-pipes.jpg" fetchpriority="high">\n' if HAS_HERO and path not in ('/thank-you.html',) and extra.find('"Plumber"') > -1 else ''
    return f'''<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<script>window.SITE={json.dumps(site, ensure_ascii=False)};</script>
{gtag}<script src="/assets/tracking.js"></script>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#073366">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="he_IL">
<meta property="og:site_name" content="{C.BRAND}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{C.DOMAIN}/assets/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<link rel="icon" type="image/png" sizes="48x48" href="/assets/favicon-48.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
{preload}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONT}" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">
{extra}
</head>'''


def lead_form_fields(prefix):
    opts = ''.join('<option>%s</option>' % i for i in ISSUES)
    return f'''<label>שם
<input type="text" name="name" autocomplete="name" placeholder="השם שלכם" maxlength="60" required></label>
<label>טלפון
<input type="tel" name="phone" autocomplete="tel" inputmode="tel" placeholder="050-0000000" maxlength="20" required style="direction:rtl">
<span class="field-error" hidden>נא להזין מספר טלפון תקין</span></label>
<label>מה התקלה?
<select name="issue">{opts}</select></label>
<div class="hp-field" aria-hidden="true"><label>אתר<input type="text" name="_honey" tabindex="-1" autocomplete="off"></label></div>
<div class="form-error" role="alert" hidden></div>
<button class="btn btn-call" data-cta="form-{prefix}" type="submit" style="min-height:54px;font:inherit;font-weight:900;font-size:18px">שלחו לי הצעת מחיר</button>
<p class="form-note">הפרטים משמשים רק כדי לחזור אליכם. <a href="/privacy.html">מדיניות פרטיות</a></p>'''


def bottom_form(form_id='contact', source='טופס תחתון'):
    return f'<form class="lead-form bottom-form" id="{form_id}" data-source="{source}">\n{lead_form_fields(form_id)}\n</form>\n'


def footer():
    cities = ''.join('<li><a href="/%s/">אינסטלטור %s</a></li>' % (s, i) for s, _, i in C.CITIES)
    guides = ''.join('<li><a href="/guides/%s/">%s</a></li>' % (g['slug'], g['short']) for g in GUIDES)
    lines = '<span>שירות בכל אזור המרכז</span>'
    if C.PHONE:
        lines += '<br><span>טלפון: <a href="tel:%s" dir="ltr">%s</a></span>' % (TEL, C.PHONE)
    if C.LICENSE:
        lines += '<br><span>רישיון אינסטלטור: %s</span>' % C.LICENSE
    return f'''<!-- FOOTER -->
<footer class="site-footer">
<div class="footer-in">
<div><strong>{C.BRAND}</strong>{lines}<br><span>שעות פעילות: 24/7, כולל שבת וחג</span></div>
<nav aria-label="אזורי שירות"><strong>אזורי שירות</strong><ul>{cities}</ul></nav>
<nav aria-label="מדריכים"><strong>מדריכים</strong><ul>{guides}</ul></nav>
<nav aria-label="מידע"><strong>מידע</strong><ul><li><a href="/accessibility.html">הצהרת נגישות</a></li><li><a href="/privacy.html">מדיניות פרטיות</a></li></ul></nav>
</div>
<p class="footer-copy">© 2026 {C.BRAND}</p>
</footer>
'''


def access_widget():
    return '''<button type="button" class="access-toggle" id="accessToggle" aria-label="תפריט נגישות" aria-expanded="false" aria-controls="accessPanel">
<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="12" cy="12" r="10.5" stroke="currentColor" stroke-width="1.6"/><circle cx="12" cy="7.3" r="1.4" fill="currentColor"/><path d="M6.5 9.8c3.6 1.1 7.4 1.1 11 0M12 9.8V14l-2.3 5.4M12 14l2.3 5.4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
</button>
<div class="access-panel" id="accessPanel">
<p>אפשרויות נגישות</p>
<button type="button" data-action="font-up">הגדלת תצוגה</button>
<button type="button" data-action="font-down">הקטנת תצוגה</button>
<button type="button" data-action="contrast">ניגודיות גבוהה</button>
<button type="button" data-action="links">הדגשת קישורים</button>
<button type="button" data-action="reset">איפוס</button>
<a href="/accessibility.html">הצהרת נגישות</a>
</div>
<script src="/assets/site.js"></script>
'''


def transform_page(src, slug, name, in_city):
    # מילוי פרטים או הסרה מסודרת של מה שעדיין חסר
    src = src.replace('זמינות מהיום למחר', 'זמינים עכשיו, 24/7')
    src = src.replace('בחרו את העיר שלכם ברשימה למטה', 'בחרו את העיר שלכם ברשימת אזורי השירות')
    src = src.replace('<div dir="rtl" style="', '<div class="site-root" dir="rtl" style="', 1)
    src = src.replace('<!-- HERO -->', '<a class="skip-link" href="#main">דילוג לתוכן הראשי</a>\n<main id="main">\n<!-- HERO -->', 1)

    # תמונות
    logo = '<a class="wordmark" href="/" aria-label="%s, לדף הבית">אינסטלציה <span>תיק תק</span></a>' % C.BRAND
    if HAS_LOGO:
        logo = '<a href="/" aria-label="%s, לדף הבית"><img src="/assets/logo.webp" alt="%s" width="200" height="100" style="height:100px;width:auto;display:block"></a>' % (C.BRAND, C.BRAND)
    src = re.sub(r'<img src="images/logo\.webp"[^>]*>', logo, src, 1)
    if HAS_HERO:
        src = src.replace('src="images/hero-pipes.jpg"', 'src="/assets/hero-pipes.jpg" fetchpriority="high"')
    else:
        src = re.sub(r'<div class="hphoto".*?</div>\n', '', src, 1)

    # טופס עליון
    src = src.replace('<form style="', '<form class="lead-form" id="quote" data-source="טופס עליון" style="', 1)
    src = src.replace('<input type="text" name="name"', '<input type="text" name="name" maxlength="60" required', 1)
    src = re.sub(r'(<input type="tel" name="phone"[^>]*?)></label>',
                 r'\1 maxlength="20" required><span class="field-error" hidden>נא להזין מספר טלפון תקין</span></label>', src, 1)
    src = src.replace('<button class="btn btn-soft" data-cta="form-hero" type="button"',
                      '<div class="hp-field" aria-hidden="true"><label>אתר<input type="text" name="_honey" tabindex="-1" autocomplete="off"></label></div>\n<div class="form-error" role="alert" hidden></div>\n<button class="btn btn-soft" data-cta="form-hero" type="submit"', 1)

    # כרטיסי שירות מובילים לטופס ובוחרים את סוג התקלה
    def card(m):
        found = re.search(r'<h3[^>]*>(.*?)</h3>', m.group(2))
        if not found:
            return m.group(0)
        title = found.group(1)
        issue = CARD_ISSUE.get(title, 'אחר')
        return '<a href="#quote" data-issue="%s" %s>%s</a>' % (issue, m.group(1), m.group(2).replace('לפרטים ←', 'להצעת מחיר ←'))
    src = re.sub(r'<a href="#" (style="[^"]*")>(.*?)</a>', card, src, flags=re.S)

    # קישורים פנימיים
    src = src.replace('href="index.html"', 'href="/"')
    src = re.sub(r'href="([a-z-]+)\.html"', r'href="/\1/"', src)

    # רישיון וניסיון
    lic = 'כן, אינסטלטור מוסמך'
    if C.LICENSE: lic += ' עם רישיון מספר ' + C.LICENSE
    if C.YEARS: lic += ' ו-%s שנות ניסיון' % C.YEARS
    src = re.sub(r'כן, אינסטלטור מוסמך עם רישיון מספר \[מספר\] ו-\[מספר\] שנות ניסיון\.', lic + ', חשבונית ואחריות בכתב על כל עבודה.', src)
    src = src.replace('אינסטלטור מוסמך · רישיון [מספר]', 'אינסטלטור מוסמך · רישיון ' + C.LICENSE if C.LICENSE else 'אינסטלטור מוסמך')

    # דירוג וביקורות: מוצגים רק כשיש נתונים אמיתיים
    if C.RATING and C.RATING_COUNT:
        src = src.replace('[דירוג]', C.RATING).replace('מ-[מספר] ביקורות', 'מ-%s ביקורות' % C.RATING_COUNT).replace('· [מספר] ביקורות', '· %s ביקורות' % C.RATING_COUNT)
    else:
        src = re.sub(r'<div[^>]*><span[^>]*>★</span> \[דירוג\].*?</div>\n', '', src, 1)
        src = re.sub(r'<p[^>]*><span[^>]*>★★★★★</span> <strong[^>]*>\[דירוג\].*?</p>\n', '', src, 1)
    if C.REVIEWS:
        figs = re.findall(r'<figure.*?</figure>', src, flags=re.S)
        place = name if name else 'מרכז'
        tpl = figs[0]
        new = []
        for r in C.REVIEWS:
            f = tpl.replace('[ציטוט ביקורת אמיתית מגוגל]', r['quote'])
            f = re.sub(r'<figcaption([^>]*)>.*?</figcaption>', lambda m: '<figcaption%s>%s · %s · %s</figcaption>' % (m.group(1), r['name'], place, r['job']), f, flags=re.S)
            new.append(f)
        src = re.sub(r'<figure.*</figure>', '\n\n'.join(new), src, 1, flags=re.S)
    else:
        src = re.sub(r'<!-- REVIEWS.*?(?=<!-- SERVICES -->)', '', src, 1, flags=re.S)

    # תמונות מהשטח: מוצגות רק כשיש תמונות אמיתיות
    if C.GALLERY:
        items = ''.join('<img src="/assets/%s" alt="%s" loading="lazy" style="width:100%%;aspect-ratio:4/3;object-fit:cover;border-radius:14px;display:block">\n' % (g['file'], g['alt']) for g in C.GALLERY)
        src = re.sub(r'(?:<div style="aspect-ratio: 4 / 3;[^\n]*\n)+', items, src, 1)
    else:
        src = re.sub(r'<!-- REAL PHOTOS -->.*?(?=<!-- LOCAL SEO CONTENT -->)', '', src, 1, flags=re.S)

    # טופס תחתון
    src = re.sub(r'(<p style="margin: 0; font-size: 14px; color: #B9CBE4">)', bottom_form() + r'\1', src, 1)
    # פוטר
    src = re.sub(r'<!-- FOOTER -->.*?</footer>\n', '</main>\n' + footer().replace('\\', '\\\\'), src, 1, flags=re.S)

    # טלפון ווואטסאפ
    if TEL:
        src = src.replace('tel:[מספר טלפון]', 'tel:' + TEL).replace('[מספר טלפון]', C.PHONE)
        src = src.replace('wa.me/972000000000', 'wa.me/' + WA)
    else:
        src = re.sub(r'<p[^>]*>דחוף\? <a[^>]*data-cta="call-form".*?</p>\n', '', src, 1, flags=re.S)
        src = re.sub(r'(<p[^>]*>לא מצאתם תשובה\? )<a[^>]*>.*?</a>', r'\1<a href="#quote" style="color:#0B7A3E;font-weight:900">השאירו פרטים ונחזור אליכם</a>', src, 1, flags=re.S)
        src = re.sub(r'<a [^>]*data-cta="wa-[^"]*"[^>]*>.*?</a>\n?', '', src, flags=re.S)
        src = re.sub(r'<a [^>]*data-cta="call-final"[^>]*>.*?</a>\n?', '', src, 1, flags=re.S)
        def call(m):
            label = 'להשארת פרטים' if m.group(2) == 'call-sticky' else 'להצעת מחיר'
            return '<a %s href="#quote"%s>%s</a>' % (m.group(1), m.group(3), label)
        src = re.sub(r'<a ((?:class="[^"]*" )?data-cta="(call-[^"]*)") href="tel:\[מספר טלפון\]"([^>]*)>.*?</a>', lambda m: call(m), src, flags=re.S)
        src = src.replace('<div class="mbar" style', '<div class="mbar single" style')
        src = src.replace('מתקשרים או שולחים תמונה', 'משאירים פרטים').replace('מתארים את התקלה בטלפון או שולחים תמונה בוואטסאפ.', 'בוחרים את סוג התקלה בטופס, ואנחנו חוזרים אליכם.')
        src = src.replace('עונים תוך שניות · ', '')
    return src


def build_pages():
    pages = [('index', '', None, None)] + [(s, s, n, i) for s, n, i in C.CITIES]
    for fname, slug, name, in_city in pages:
        with open(os.path.join(SRC, fname + '.html'), encoding='utf-8') as f:
            raw = f.read()
        desc = re.search(r'<meta name="description" content="([^"]*)"', raw).group(1)
        faq_src = re.search(r'<script type="application/ld\+json">(\{"@context":"https://schema.org","@type":"FAQPage".*?)</script>', raw).group(1)
        lic = 'כן, אינסטלטור מוסמך' + (' עם רישיון מספר ' + C.LICENSE if C.LICENSE else '') + (' ו-%s שנות ניסיון' % C.YEARS if C.YEARS else '') + ', חשבונית ואחריות בכתב על כל עבודה.'
        faq = json.loads(faq_src.replace('כן, אינסטלטור מוסמך עם רישיון מספר [מספר] ו-[מספר] שנות ניסיון.', lic))
        body = raw[raw.index('<body>'):]
        body = transform_page(body, slug, name, in_city)
        if slug:
            title = 'אינסטלטור %s – הגעה תוך 30 דקות | %s' % (in_city, C.BRAND)
            path = '/%s/' % slug
            biz = business()
            biz['areaServed'] = {'@type': 'City', 'name': name}
            biz['url'] = C.DOMAIN + path
            crumbs = {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'דף הבית', 'item': C.DOMAIN + '/'},
                {'@type': 'ListItem', 'position': 2, 'name': 'אינסטלטור ' + in_city, 'item': C.DOMAIN + path}]}
            extra = '\n'.join([ld(biz), ld(faq), ld(crumbs)])
        else:
            title = 'אינסטלטור במרכז 24/7 – הגעה תוך 30 דקות | %s' % C.BRAND
            path = '/'
            extra = '\n'.join([ld(business()), ld(faq)])
        out = head(title, desc, path, extra) + '\n' + body
        out = out.replace('<body>', '<body>', 1).replace('</body>', access_widget() + '</body>')
        write((slug + '/' if slug else '') + 'index.html', out)


def shell(title, desc, path, content, extra='', robots='index, follow', og='website', form=True):
    cta = ''
    if TEL:
        cta = '<a class="btn btn-call" data-cta="call-top" href="tel:%s" dir="ltr">%s</a>' % (TEL, C.PHONE)
    else:
        cta = '<a class="btn btn-call" data-cta="form-top" href="#quote">להצעת מחיר</a>' if form else ''
    brand = '<a class="wordmark" href="/" aria-label="%s, לדף הבית">אינסטלציה <span>תיק תק</span></a>' % C.BRAND
    if HAS_LOGO:
        brand = '<a href="/" aria-label="%s, לדף הבית"><img src="/assets/logo.webp" alt="%s"></a>' % (C.BRAND, C.BRAND)
    return head(title, desc, path, extra, robots, og) + f'''
<body class="page-body">
<a class="skip-link" href="#main">דילוג לתוכן הראשי</a>
<div class="site-root">
<header class="topbar"><div class="topbar-in">{brand}{cta}</div></header>
<main id="main">
{content}
</main>
{footer()}{mobile_bar(form)}
</div>
{access_widget()}</body>
</html>
'''


def mobile_bar(form=True):
    if TEL:
        return f'''<div class="mbar" style="position:sticky;bottom:0;z-index:40;grid-template-columns:3fr 2fr;background:#073366">
<a class="btn" data-cta="call-sticky" href="tel:{TEL}" style="border-radius:0;min-height:60px;background:#073366;color:#fff;font-size:19px">{PHONE_SVG}חייגו עכשיו</a>
<a class="btn" data-cta="wa-sticky" href="{WA_LINK}" style="border-radius:0;min-height:60px;background:#25D366;color:#062B16;font-size:18px">וואטסאפ</a>
</div>
'''
    return '<div class="mbar single" style="position:sticky;bottom:0;z-index:40;background:#073366"><a class="btn" data-cta="form-sticky" href="%s" style="border-radius:0;min-height:60px;background:#073366;color:#fff;font-size:19px">להשארת פרטים</a></div>\n' % ('#quote' if form else '/#quote')


def cta_band(title, sub):
    btns = ''
    if TEL:
        btns = f'<div class="cta-row"><a class="btn btn-light" data-cta="call-band" href="tel:{TEL}" style="min-height:56px;padding:0 24px;font-size:19px">חייגו – {C.PHONE}</a><a class="btn btn-wa" data-cta="wa-band" href="{WA_LINK}" style="min-height:56px;padding:0 22px;font-size:18px">וואטסאפ</a></div>'
    return f'<section class="cta-band"><div class="cta-band-in"><h2>{title}</h2><p>{sub}</p>{btns}{bottom_form("quote", "טופס במדריך")}</div></section>'


def build_guides():
    today = C.LAST_UPDATED
    for g in GUIDES:
        path = '/guides/%s/' % g['slug']
        toc = ''.join('<li><a href="#%s">%s</a></li>' % (i, t) for i, t, _ in g['sections'])
        secs = ''.join('<h2 id="%s">%s</h2>\n%s\n' % (i, t, h) for i, t, h in g['sections'])
        faq = ''.join('<details><summary>%s</summary><p>%s</p></details>\n' % q for q in g['faq'])
        others = ''.join('<li><a href="/guides/%s/">%s</a></li>' % (o['slug'], o['title']) for o in GUIDES if o is not g)
        content = f'''<article class="article">
<nav class="breadcrumb" aria-label="מיקום באתר"><a href="/">דף הבית</a> / <span>{g['short']}</span></nav>
<h1>{g['title']}</h1>
<p class="article-meta">מאת צוות {C.BRAND}</p>
<p class="lead">{g['lead']}</p>
<nav class="article-toc" aria-label="תוכן המדריך"><p>במדריך:</p><ol>{toc}<li><a href="#faq">שאלות נפוצות</a></li></ol></nav>
{secs}<h2 id="faq">שאלות נפוצות</h2>
{faq}<nav class="article-related" aria-label="מדריכים נוספים"><p>מדריכים נוספים:</p><ul>{others}</ul></nav>
</article>
{cta_band(g['cta'], 'אינסטלטור מוסמך במרכז, מחיר סגור לפני שמתחילים ואחריות 6 חודשים בכתב.')}'''
        art = {'@context': 'https://schema.org', '@type': 'Article', 'headline': g['title'], 'description': g['desc'],
               'datePublished': today, 'dateModified': today, 'inLanguage': 'he', 'image': C.DOMAIN + '/assets/og-image.jpg',
               'mainEntityOfPage': C.DOMAIN + path,
               'author': {'@type': 'Organization', 'name': C.BRAND, 'url': C.DOMAIN + '/'},
               'publisher': {'@type': 'Organization', 'name': C.BRAND, 'url': C.DOMAIN + '/'}}
        fq = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in g['faq']]}
        crumbs = {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'דף הבית', 'item': C.DOMAIN + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': g['short'], 'item': C.DOMAIN + path}]}
        write('guides/%s/index.html' % g['slug'], shell(g['title'] + ' | ' + C.BRAND, g['desc'], path, content,
              '\n'.join([ld(art), ld(fq), ld(crumbs)]), og='article'))


def contact_line(prefix):
    parts = []
    if C.PHONE:
        parts.append('טלפון <a href="tel:%s" dir="ltr">%s</a>' % (TEL, C.PHONE))
    parts.append('דוא"ל <a href="mailto:%s">%s</a>' % (C.CONTACT_EMAIL, C.CONTACT_EMAIL))
    return prefix + ' ' + ' או '.join(parts) + '.'


def build_static():
    who = 'לרכז הנגישות שלנו, %s,' % C.ACCESS_COORDINATOR if C.ACCESS_COORDINATOR else 'לרכז הנגישות שלנו'
    acc = f'''<article class="article">
<h1>הצהרת נגישות</h1>
<p>{C.BRAND} פועל כדי שהאתר יהיה נוח ונגיש לכל אדם, בהתאם לתקנות שוויון זכויות לאנשים עם מוגבלות (התאמות נגישות לשירות), התשע"ג-2013, ולתקן הישראלי ת"י 5568 ברמת AA, המבוסס על הנחיות WCAG.</p>
<h2>מה יש באתר</h2>
<ul><li>תפריט נגישות צף: הגדלה והקטנה של התצוגה, ניגודיות גבוהה והדגשת קישורים.</li><li>אפשר לנווט במקלדת, ויש קישור לדילוג לתוכן הראשי.</li><li>מבנה כותרות מסודר ותוויות לשדות הטפסים.</li><li>האנימציות נעצרות אצל מי שהגדיר במכשיר הפחתת תנועה.</li></ul>
<h2>נתקלתם בבעיה?</h2>
<p>אם משהו באתר לא נגיש לכם, או שיש לכם הצעה לשיפור, נשמח שתפנו {who}. {contact_line('אפשר ליצור קשר ב')}</p>
<p>ההצהרה עודכנה לאחרונה ב־2 בנובמבר 2026.</p>
</article>'''
    write('accessibility.html', shell('הצהרת נגישות | ' + C.BRAND, 'הצהרת הנגישות של %s: ההתאמות באתר ופרטי הקשר לפניות בנושא נגישות.' % C.BRAND, '/accessibility.html', acc, form=False))

    pri = f'''<article class="article">
<h1>מדיניות פרטיות</h1>
<p>{C.BRAND} הוא עסק לשירותי אינסטלציה. אנחנו מכבדים את הפרטיות שלכם ומשתמשים במידע רק כדי לתת לכם שירות. בדף הזה מוסבר איזה מידע נאסף באתר ומה אנחנו עושים איתו.</p>
<h2>איזה מידע נאסף</h2>
<p><strong>מידע שאתם מוסרים:</strong> השם, מספר הטלפון וסוג התקלה שאתם משאירים בטופס, וגם העמוד שממנו שלחתם את הפנייה.</p>
<p><strong>מידע טכני:</strong> האתר עשוי להשתמש בכלים של גוגל למדידת ביקורים ופרסום. הכלים האלה יכולים לאסוף מידע כמו סוג הדפדפן והמכשיר, העמודים שבהם ביקרתם, ואם הגעתם מתוך מודעה. לשם כך הם משתמשים בעוגיות (קבצים קטנים שנשמרים בדפדפן).</p>
<h2>למה אנחנו משתמשים במידע</h2>
<p>כדי לחזור אליכם, לתת לכם הצעת מחיר ולתאם את העבודה. בנוסף, כדי למדוד אילו מודעות מביאות פניות ולשפר את האתר.</p>
<p>כשמופעלת מדידת המרות, מספר הטלפון שנשלח בטופס עובר לגוגל אחרי הצפנה, כדי להתאים בין הפנייה למודעה שהובילה אליה.</p>
<h2>עם מי המידע משותף</h2>
<p>אנחנו לא מוכרים את המידע שלכם. הפרטים מהטופס מגיעים אלינו בדואר אלקטרוני דרך שירות חיצוני לשליחת טפסים (FormSubmit), ונשמרים אצלנו בגיליון לידים בחשבון גוגל. מידע המדידה עובר לגוגל, לפי מדיניות הפרטיות של גוגל.</p>
<h2>כמה זמן שומרים את המידע</h2>
<p>כל עוד הוא נחוץ לטיפול בפנייה, לביצוע העבודה ולניהול העסק.</p>
<h2>הזכויות שלכם</h2>
<p>אתם יכולים לבקש לעיין במידע שלכם, לתקן אותו או למחוק אותו. אפשר גם לחסום עוגיות בהגדרות הדפדפן, ולשנות את העדפות הפרסום בגוגל בכתובת <a href="https://adssettings.google.com" target="_blank" rel="noopener">adssettings.google.com</a>.</p>
<p>{contact_line('לכל שאלה או בקשה בנושא פרטיות:')}</p>
<p>המדיניות עודכנה לאחרונה ב־2 בנובמבר 2026.</p>
</article>'''
    write('privacy.html', shell('מדיניות פרטיות | ' + C.BRAND, 'מדיניות הפרטיות של %s: איזה מידע נאסף באתר, למה משתמשים בו ומה הזכויות שלכם.' % C.BRAND, '/privacy.html', pri, form=False))

    actions = '<a class="btn btn-light" style="border:2px solid #073366;min-height:52px;padding:0 22px" href="/">לדף הבית</a>'
    if TEL:
        actions = '<a class="btn btn-call" style="min-height:52px;padding:0 22px" href="tel:%s" dir="ltr">%s</a>' % (TEL, C.PHONE) + actions
    wa = ''
    if WA:
        wa = '<p>רוצים לזרז? שלחו תמונה של התקלה:</p><p><a class="btn btn-wa" id="waPhotos" style="min-height:52px;padding:0 22px" href="%s" target="_blank" rel="noopener">שליחת תמונה בוואטסאפ</a></p>' % WA_LINK
    script = '''<script>
(function(){
  var name = '';
  try {
    name = sessionStorage.getItem('lead_name') || '';
    // ההמרה נספרת רק אחרי שליחת טופס אמיתית, ופעם אחת בלבד
    if (sessionStorage.getItem('lead_sent')) {
      var phone = sessionStorage.getItem('lead_phone') || '';
      sessionStorage.removeItem('lead_sent');
      sessionStorage.removeItem('lead_phone');
      if (phone && window.SITE.ads) gtag('set', 'user_data', { phone_number: '+972' + phone.replace(/^0/, '') });
      if (window.trackConversion) trackConversion('form');
    }
  } catch(e) {}
  if (name) document.getElementById('nameSpan').textContent = ', ' + name;
})();
</script>'''
    ty = f'''<div class="notice-wrap"><div class="notice-card">
<h1>תודה<span id="nameSpan"></span>!</h1>
<p>קיבלנו את הפרטים ונחזור אליכם בהקדם עם מחיר סגור, בלי התחייבות.</p>
{wa}<div class="cta-row" style="margin-top:20px">{actions}</div>
</div></div>
{script}'''
    write('thank-you.html', shell('תודה שהשארתם פרטים | ' + C.BRAND, 'קיבלנו את הפרטים שלכם.', '/thank-you.html', ty, robots='noindex, nofollow', form=False))

    nf = f'''<div class="notice-wrap"><div class="notice-card">
<h1>העמוד הזה לא קיים</h1>
<p>אולי הקישור השתנה. אפשר לחזור לדף הבית או להשאיר לנו פרטים.</p>
<div class="cta-row" style="margin-top:20px">{actions}</div>
</div></div>'''
    write('404.html', shell('העמוד לא נמצא | ' + C.BRAND, 'העמוד לא נמצא.', '/404.html', nf, robots='noindex', form=False))


def build_seo():
    urls = [('/', '1.0')] + [('/%s/' % s, '0.8') for s, _, _ in C.CITIES] + [('/guides/%s/' % g['slug'], '0.6') for g in GUIDES] + [('/accessibility.html', '0.2'), ('/privacy.html', '0.2')]
    rows = ''.join('  <url><loc>%s%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>\n' % (C.DOMAIN, u, C.LAST_UPDATED, p) for u, p in urls)
    write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s</urlset>\n' % rows)
    write('robots.txt', 'User-agent: *\nAllow: /\nDisallow: /thank-you.html\nDisallow: /tools/\n\nSitemap: %s/sitemap.xml\n' % C.DOMAIN)
    write('CNAME', C.DOMAIN.split('//')[1] + '\n')
    write('.nojekyll', '')
    write('.htaccess', 'ErrorDocument 404 /404.html\nRedirectMatch 404 ^/tools(/|$)\n')


def build_css():
    with open(os.path.join(SRC, 'index.html'), encoding='utf-8') as f:
        raw = f.read()
    css = re.search(r'<style>(.*?)</style>', raw, re.S).group(1).strip()
    with open(os.path.join(HERE, 'extra.css'), encoding='utf-8') as f:
        write('assets/site.css', css + '\n' + f.read())


if __name__ == '__main__':
    build_css(); build_pages(); build_guides(); build_static(); build_seo()
    print('נבנה בהצלחה')
