"""Render the FN Squad pages and legacy aliases using only the Python standard library."""
import argparse
import html
import json
import re
from datetime import date
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
DATA = json.loads((ROOT / "content/reference.json").read_text())
CONFIG = DATA["links"]
EMAIL = "fnsquadofficial@gmail.com"
DISCORD = CONFIG["discordInviteUrl"]
HOME = "/"
PAGES_BASE_PATH = "/v2"
PAGES_URL = f"https://fnsquadofficial.github.io{PAGES_BASE_PATH}"
ROOT_LINK = re.compile(r'(\b(?:href|src)=")(/(?!/)[^"]*)')
NAV = {"Home": HOME, "FreakyNews": "/freakynews/", "FN SMP": "/fn-smp/", "Community": "/community/", "About": "/about/"}
SUPPORT = {"Help centre": "/help/", "Contact": "/contact/", "Policies": "/legal/", "Privacy": "/privacy/"}
GROUP_NOTE = "Other group members can see your phone number."
GITHUB_PRIVACY = "https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages"
OPENAI_PRIVACY = "https://openai.com/policies/"
MY_PRIVACY = "https://www.pdp.gov.my/en/akta709/"
MY_SCOPE = "https://www.pdp.gov.my/en/akta/application-and-non-application-of-the-act/"
MY_COMPLAINT = "https://www.pdp.gov.my/en/public/"
MCMC_GUIDE = "https://cfm.my/complaint-channels/?lang=en"
MCMC_GUIDE_MS = "https://cfm.my/saluran-portal-aduan/"
ISO_SECURITY = "https://www.iso.org/standard/27001"
ISO_PRIVACY = "https://www.iso.org/standard/27701"
W3C = "https://www.w3.org/TR/WCAG22/"
WHATSAPP_PRIVACY = "https://www.whatsapp.com/legal/privacy-policy"
WHATSAPP_CHANNELS = "https://faq.whatsapp.com/1318001139066835"
WHATSAPP_GROUPS = "https://faq.whatsapp.com/3307102709559968/"
DISCORD_PRIVACY = "https://discord.com/privacy"
DISCORD_AGE = "https://support.discord.com/hc/en-us/articles/360040724612-Why-is-Discord-asking-for-my-birthday"
PUBLIC_POLICY = "https://github.com/fnsquadofficial/fnsquadofficial.github.io/blob/main/docs/fn-squad-public-transparency-policy.md"
ARCHIVE = "https://faizzzlol.github.io/freakyniggas/"
ARCHIVE_HISTORY = "https://github.com/faizzzlol/freakyniggas/commits/"
PUBLIC_SOURCE = "https://github.com/FNSquadOfficial/fnsquadofficial.github.io"


def esc(value):
    return html.escape(str(value), quote=True)


def icon(name):
    return f'<img class="platform-icon" src="/assets/{name}.svg" alt="" width="22" height="22">'


def link(label, url, *, cls="", mark="", arrow=False):
    is_external = url.startswith("https://")
    attrs = ' target="_blank" rel="noopener noreferrer"' if is_external else ""
    style = f' class="{cls}"' if cls else ""
    decoration = icon(mark) if mark else ""
    indicator = f'<span class="arrow {"arrow-up" if is_external or url.startswith("mailto:") else "arrow-right"}" aria-hidden="true"></span>' if arrow else ""
    return f'<a href="{esc(url)}"{attrs}{style}>{decoration}{esc(label)}{indicator}</a>'


def button(label, url, variant="plain", mark=""):
    return link(label, url, cls=f"button button-{variant}", mark=mark, arrow=not mark)


def email(subject=""):
    return f"mailto:{EMAIL}" + ("?subject=" + quote("FN Squad | " + subject) if subject else "")


def platform_links(kind):
    return {
        "discord": DISCORD,
        "main": CONFIG["whatsappGroupUrl"],
        "news": CONFIG["whatsappChannelUrl"],
        "updates": CONFIG["updatesChannelUrl"],
        "smp": CONFIG["minecraftWhatsappUrl"],
    }[kind]


def brand():
    return '<a class="brand" href="/" aria-label="FN Squad home"><img src="/assets/fn-mark-128.webp" alt="" width="38" height="38"><span>FN Squad</span></a>'


def navigation(routes, current=""):
    return "".join(f'<a href="{url}"' + (' aria-current="page"' if url == current else '') + f'>{title}</a>' for title, url in routes.items())


def layout(route, title, description, body, *, public=False, error=False):
    name = title if route == "/" else f"{title} · FN Squad"
    og_image = "og-fn-smp.png" if route == "/fn-smp/" else "og-fn-squad.png"
    origin = PAGES_URL if public else ""
    indexing = '<meta name="robots" content="noindex, nofollow">'
    if public and not error:
        indexing = f'<link rel="canonical" href="{origin}{route}">\n  <meta property="og:url" content="{origin}{route}">'
    support_links = {**SUPPORT, "Terms of use": "/terms/", "Editorial standards": "/editorial/"}
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  {indexing}
  <meta name="theme-color" content="#f2f3f4" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#111214" media="(prefers-color-scheme: dark)">
  <meta name="description" content="{esc(description)}">
  <meta property="og:title" content="{esc(name)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:image" content="{origin}/assets/{og_image}">
  <title>{esc(name)}</title>
  <link rel="icon" href="/assets/fn-mark-128.webp" type="image/webp">
  <link rel="apple-touch-icon" href="/assets/fn-icon-192.png">
  <link rel="manifest" href="/site.webmanifest">
  <link rel="stylesheet" href="/styles.css">
  <script src="/theme.js"></script>
  <script defer src="/app.js"></script>
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="header">
    <div class="wrap header-row" id="top">
      {brand()}
      <nav id="navigation" class="navigation" aria-label="Main navigation">{navigation({**NAV, "Help": "/help/"}, route)}
        <div class="mobile-only">{navigation({title: url for title, url in SUPPORT.items() if url != "/help/"}, route)}</div>
      </nav>
      <div class="header-actions">
        <button class="icon-button" id="theme-button" type="button" hidden aria-label="Switch colour theme"><span class="theme-glyph" aria-hidden="true"></span></button>
        <button class="icon-button menu-button" id="menu-button" type="button" hidden aria-controls="navigation" aria-expanded="false" aria-label="Open navigation"><span aria-hidden="true"></span></button>
        <div class="header-join">{button("Join Discord", DISCORD, "discord", "discord")}</div>
      </div>
    </div>
  </header>
  <main id="main" class="wrap{' error-page' if error else ''}">{body}</main>
  <footer class="footer" id="footer"><div class="wrap">
    <div class="footer-top">
      <div>{brand()}<p>Independent creator and gaming community in Malaysia.</p></div>
      <nav aria-label="Explore FN Squad"><h2>Explore</h2>{navigation(NAV)}</nav>
      <nav aria-label="Support and policies"><h2>Support &amp; policies</h2>{navigation(support_links)}</nav>
      <nav aria-label="Community platforms"><h2>Connect</h2>{link("Discord", DISCORD, mark="discord")}{link("WhatsApp directory", "/community/#official-links", mark="whatsapp")}{link("Social accounts", "/community/#socials")}</nav>
    </div>
    <div class="footer-bottom"><span>© FN Squad</span><span>Platform names and marks identify their respective services.</span></div>
  </div></footer>
</body></html>"""


def intro(label, title, description, actions=""):
    return f'<header class="page-intro"><p class="eyebrow"><i></i>{label}</p><h1>{title}</h1><p class="lede">{description}</p>{f"<div class=actions>{actions}</div>" if actions else ""}</header>'


def section_head(title, detail="", action=""):
    return f'<div class="section-heading"><div><h2>{title}</h2>{f"<p>{detail}</p>" if detail else ""}</div>{action}</div>'


def writing_section(anchor, title, body):
    return f'<section id="{anchor}"><h2>{title}</h2>{body}</section>'


def faq(items):
    return '<div class="faq">' + "".join(f'<details><summary>{question}</summary><div>{answer}</div></details>' for question, answer in items) + '</div>'


def document(title, description, entries, malay=""):
    toc = "".join(f'<a href="#{key}">{section_title}</a>' for key, section_title, _ in entries)
    if malay:
        toc += '<a href="#bm" lang="ms">Bahasa Melayu</a>'
    return f'''{intro("FN Squad policies", title, description)}
    <div class="document-layout"><nav class="toc" aria-label="On this page"><span>On this page</span>{toc}</nav>
    <div class="prose">{''.join(writing_section(*entry) for entry in entries)}{malay}</div></div>'''


def home():
    projects = [
        ("smp", "Minecraft", "FN SMP", "Explore our Minecraft community, server rules and whitelist process.", "/fn-smp/"),
        ("news", "News & culture", "FreakyNews", "Catch up on gaming, tech and culture, with links to the original sources.", "/freakynews/"),
        ("community", "Chat & updates", "Community", "Find our WhatsApp groups, Discord server and announcement channels.", "/community/"),
    ]
    art = {
        "smp": '<div class="voxel-layer" aria-hidden="true"></div><img src="/assets/fn-smp-logo-512.webp" alt="" width="100" height="100">',
        "news": '<div class="news-lines"></div><div class="news-stamp"><span>FREAKY</span><strong>NEWS</strong></div>',
        "community": f'<div class="community-orbit"></div><div class="chat-visual"><div>{icon("discord")}</div><div>{icon("whatsapp")}</div></div>',
    }
    cards = "".join(f'''<a class="project-card" id="{"smp" if key == "smp" else url.strip("/")}" href="{url}"><div class="project-art art-{key}" aria-hidden="true">{art[key]}</div><div class="project-body"><span class="meta-label">{kind}</span><h3>{title}</h3><p>{desc}</p><span class="circle-arrow" aria-hidden="true"><span class="arrow arrow-up"></span></span></div></a>''' for key, kind, title, desc, url in projects)
    return f'''
    <section class="hero" aria-labelledby="home-title">
      <div class="hero-copy">
        <p class="eyebrow"><i></i> Malaysian creator community</p>
        <h1 id="home-title">Good games.<br>Good company.</h1>
        <p class="lede">Play Minecraft, catch up with FreakyNews, or find the squad on Discord and WhatsApp.</p>
        <div class="actions">{button("Join Discord", DISCORD, "discord", "discord")}{button("Find your group", "/community/#official-links")}</div>
      </div>
      <div class="hero-art" aria-hidden="true">
        <div class="hero-grid"></div><div class="hero-ring ring-1"></div><div class="hero-ring ring-2"></div><div class="hero-ring ring-3"></div><div class="hero-track"></div><span class="hero-dot"></span><span class="corner top-left"></span><span class="corner bottom-right"></span>
        <img width="668" height="412" src="/assets/fn-hero.webp" alt="" fetchpriority="high">
        <div class="hero-tags"><span>FN SQUAD</span><span>MY</span></div>
      </div>
    </section>
    <section id="projects" class="section projects">{section_head("Explore FN Squad")}{f'<div class="project-grid">{cards}</div>'}</section>
    <section id="official-links" class="section">{section_head("Start here", "Find the right place to chat, play or follow updates.", link("View all official links", "/community/#official-links", cls="text-link", arrow=True))}
      <div class="shortcut-grid">
        {shortcut("FreakyHomie", "WhatsApp group · Main community chat", platform_links("main"), "whatsapp", GROUP_NOTE)}
        {shortcut("FreakyNews", "WhatsApp channel · News and culture updates", platform_links("news"), "whatsapp")}
        {shortcut("FN Squad Discord", "Discord server · Chat and FN SMP whitelist", DISCORD, "discord")}
      </div>
    </section>
    <aside class="notice home-notice"><div><h2>Need a hand?</h2><p>Find joining instructions, contact options and help with community reports.</p></div>{button("Visit Help Centre", "/help/")}</aside>'''


def shortcut(title, desc, url, platform, note=""):
    return f'''<a class="shortcut" href="{esc(url)}" target="_blank" rel="noopener noreferrer"><span class="brand-chip {platform}">{icon(platform)}</span><span><strong>{title}</strong><small>{desc}</small>{f'<small class="small-note">{note}</small>' if note else ''}</span><span class="arrow arrow-up" aria-hidden="true"></span></a>'''


def social_link(label, url):
    slug = label.lower()
    return (
        f'<a class="social-link" href="{esc(url)}" target="_blank" rel="noopener noreferrer">'
        f'<span class="social-mark {esc(slug)}">{icon(slug)}</span>'
        f'<span class="social-name">{esc(label)}</span>'
        '<span class="arrow arrow-up" aria-hidden="true"></span></a>'
    )


def community():
    primary = [
        ("FreakyHomie", "WhatsApp group · Main community chat", "main", "whatsapp", GROUP_NOTE),
        ("FN Squad Discord", "Discord server · Chat, moderation and FN SMP applications", "discord", "discord", ""),
        ("FreakyNews", "WhatsApp channel · News and culture updates", "news", "whatsapp", ""),
        ("FN Squad Updates", "WhatsApp channel · Community announcements", "updates", "whatsapp", ""),
        ("FN SMP", "WhatsApp group · Minecraft community chat", "smp", "whatsapp", GROUP_NOTE),
    ]
    directory = "".join(shortcut(title, desc, platform_links(key), platform, note) for title, desc, key, platform, note in primary)
    socials = "".join(social_link(item["name"], item["url"]) for item in CONFIG["socialLinks"])
    return f'''{intro("Community", "Find your people.", "Join the squad on Discord or WhatsApp, follow announcements, and see how to get help.", button("Official links", "#official-links", "ink") + button("Community rules", "#rules"))}
    <section id="official-links" class="section inset">
      {section_head("Official links", "Groups are for conversation. Channels are for following updates.")}
      <div class="shortcut-grid community-grid">{directory}</div>
      <p class="subtle">{link("WhatsApp channel privacy", WHATSAPP_CHANNELS, arrow=True)} <span aria-hidden="true">·</span> {link("Discord age requirements", DISCORD_AGE, arrow=True)}</p>
    </section>
    <section class="section" id="socials">{section_head("Follow FN Squad elsewhere")}<div class="social-grid">{socials}</div></section>
    <div class="document-layout">
      <nav class="toc" aria-label="On this page"><span>Community guide</span><a href="#rules">House rules</a><a href="#report">Report an issue</a><a href="#consequences">Moderation &amp; appeals</a></nav>
      <div class="prose">
        <section id="rules"><h2>House rules</h2><ul>
          <li>Respect other members. Harassment, hate, bullying, doxxing, and attacks on race, religion or royalty are prohibited.</li>
          <li>Keep private information and screenshots out of public chats. Avoid unverified rumours, explicit content, gore, scams and gambling.</li>
          <li>Stay on topic, use the right channels, and ask an admin before posting promotions.</li>
          <li>Keep banter mutual and stop when asked. Adults should contact minors privately only for community-related reasons.</li>
        </ul></section>
        <section id="report"><h2>Report an issue</h2><p>Send a brief description privately to an FN Squad admin or moderator. Include the channel, message link if available, and approximate time. Redact unrelated names and details from screenshots. Read the <a href="/privacy/#reports">reporting privacy notice</a> before sharing evidence.</p><div class="actions">{button("Open Discord", DISCORD, "discord", "discord")}{button("Other contact options", "/contact/#safety")}</div></section>
        <section id="consequences"><h2>Moderation &amp; appeals</h2><p>Moderators may issue a warning or mute, a temporary suspension of 3 to 14 days, or removal. Serious violations may lead to an immediate ban. The first two strikes expire after 90 days without further violations.</p><p>Appeal within 14 days. Include the case number if you have one so a different admin can review it.</p></section>
      </div>
    </div>'''


def smp():
    address = CONFIG["minecraftServerAddress"]
    details = (
        f'<p>Address <code id="server-address">{esc(address)}</code> <button type="button" class="button button-plain" data-copy="{esc(address)}" hidden>Copy address</button></p><p>{esc(CONFIG["minecraftEdition"])} {esc(CONFIG["minecraftVersion"])}</p>'
        if address else '<p>Ask the team for the confirmed address, edition and version after your whitelist application is approved.</p>'
    )
    return f'''<div class="split-intro">{intro("Minecraft community", "FN SMP", "Build, explore and play Minecraft with the squad. Apply for the whitelist in Discord to get started.", button("Open Discord to apply", DISCORD, "discord", "discord") + button("How to join", "#join"))}<div class="smp-intro-art"><img src="/assets/fn-smp-logo-512.webp" width="170" height="170" alt=""></div></div>
    <section id="join" class="section">{section_head("How to join")}
      <ol class="steps"><li><h3>Join Discord</h3><p>Open the FN Squad server and read <code>#rules</code>. Check the {link("age requirements", DISCORD_AGE)} for your country.</p></li><li><h3>Apply for the whitelist</h3><p>Find <code>#whitelist-apply</code> and answer the questions there.</p></li><li><h3>Wait for approval</h3><p>The team will follow up in Discord. Use the connection details they confirm.</p></li></ol>
    </section>
    <aside id="details" class="notice"><div><h2>Server details</h2>{details}<span class="status-copy" role="status"></span></div>{button("FN SMP WhatsApp group", platform_links("smp"), "plain", "whatsapp")}</aside>
    <p class="subtle">{GROUP_NOTE}</p>
    <section class="section" id="rules">{section_head("Server rules")}
      {faq([("Fair play", "<p>No hacked clients, x-ray, autoclickers, exploits or lag machines. Report bugs to staff. Check which client mods are allowed before using them.</p>"),
      ("Claims, builds and PvP", "<p>No griefing, theft, trapping or spawn-killing. Build at least 100 blocks from existing bases unless the owner agrees. PvP requires mutual consent or a designated arena.</p>"),
      ("Accounts, chat and inactive claims", "<p>Use one main account and declare alternate accounts. Keep signs, builds and chat respectful. Claims may be released after 90 days of inactivity with a Discord warning. Ask staff about holding a claim if you are taking a break.</p>"),
      ("Reports and appeals", '<p>Send evidence to staff privately. You can appeal a ban within 14 days using the Discord appeal process. See the <a href="/community/#consequences">community moderation policy</a>.</p>')])}
    </section>
    <section class="section" id="faq">{section_head("FN SMP FAQ")}
      {faq([("Do I need mods?", "<p>Confirm the server mode and any required modpack with the team in Discord.</p>"), ("Is FN SMP pay-to-win?", "<p>Playing does not require a donation. FN SMP does not sell in-game items, claims or rule exceptions.</p>"), ("How do I find the server address?", '<p>Ask the team through Discord once they approve your whitelist application. See <a href="#details">server details</a>.</p>')])}
    </section>'''


TOPICS = {"all": "All stories", "gaming": "Gaming", "tech": "Tech", "malaysia": "Malaysia", "entertainment": "Entertainment", "sports": "Sports"}


def news():
    stories = sorted(DATA["stories"], key=lambda story: story["date"], reverse=True)
    last_updated = date.fromisoformat(DATA["updated"]).strftime("%d %B %Y")
    filters = "".join(f'<button class="chip" type="button" data-filter="{key}" aria-pressed="{str(key == "all").lower()}">{label}</button>' for key, label in TOPICS.items())
    cards = []
    for item in stories:
        tags = " ".join(key for key in item["category"].split() if key in TOPICS)
        label = " · ".join(TOPICS[key] for key in tags.split())
        published = date.fromisoformat(item["date"]).strftime("%d %b %Y")
        cards.append(f'''<article class="story" id="{item["id"]}" data-topics="{esc(tags)}"><div class="story-meta"><span>{label}</span><time datetime="{item["date"]}">{published}</time></div><h3>{esc(item["title"])}</h3><p>{esc(item["body"])}</p><div class="story-source">{link(item["source"], item["sourceUrl"], cls="text-link", arrow=True)}<small>{esc(item["sourceType"])}</small></div></article>''')
    return f'''<div class="split-intro">{intro("News and culture", "FreakyNews", "A community-curated feed about gaming, tech, Malaysia and culture. Each summary links to its source.", button("Follow on WhatsApp", platform_links("news"), "whatsapp", "whatsapp") + button("Editorial standards", "/editorial/"))}<div class="news-intro-art" aria-hidden="true"><div class="news-lines"></div><div class="news-stamp"><span>FREAKY</span><strong>NEWS</strong></div></div></div>
    <section class="section" id="feed"><div id="how-it-works">{section_head("The feed", f"Last curated on {last_updated}.")}</div>
      <div id="news-controls" hidden><div class="filters" role="group" aria-label="Filter news by topic">{filters}</div><div class="search-row"><label for="news-search">Search stories</label><input id="news-search" type="search" autocomplete="off" placeholder="Title, topic or source"><span id="story-count" role="status"></span></div></div>
      <div class="story-grid">{''.join(cards)}</div>
      <aside class="notice" id="no-stories" hidden><div><h3>No stories found</h3><p>Try another search or clear your filters.</p></div><button class="button button-plain" id="clear-news" type="button">Clear filters</button></aside>
    </section>
    <aside class="notice" id="tips"><div><h2>Spotted a mistake?</h2><p>Send the story link and the detail that needs a closer look.</p></div>{button("Request a correction", "/contact/#editorial")}</aside>'''


def help_page():
    topics = [
        ("Joining and updates", [
            ("Which WhatsApp group is the main one?", f'<p>{link("FreakyHomie", platform_links("main"), mark="whatsapp")} is the main FN Squad WhatsApp group. {GROUP_NOTE}</p>'),
            ("Where do I follow announcements?", f'<p>Follow the {link("FreakyNews WhatsApp channel", platform_links("news"))} for news and {link("FN Squad Updates", platform_links("updates"))} for community announcements.</p>'),
        ]),
        ("Minecraft", [
            ("How do I join FN SMP?", '<p>Apply for the whitelist in Discord. The <a href="/fn-smp/#join">FN SMP joining guide</a> shows where to apply and where to get the connection details.</p>'),
        ]),
        ("FreakyNews", [
            ("How do I correct a FreakyNews story?", '<p>Use the <a href="/contact/#editorial">editorial contact</a> and include the story link, what needs correction and a source if available.</p>'),
        ]),
        ("Reports and privacy", [
            ("How do I report bullying, a scam or unsafe behaviour?", '<p>Contact a moderator privately. The <a href="/community/#report">reporting guide</a> explains what to include and what to redact.</p>'),
                ("How can I request access, correction or deletion of my data?", '<p>See <a href="/privacy/#choices">privacy requests</a> for the contact route and the information to include.</p>'),
        ]),
    ]
    topic_sections = "".join(f'<section class="section" id="{key}">{section_head(title)}{faq(questions)}</section>' for key, (title, questions) in zip(("joining", "minecraft", "news", "safety"), topics))
    return f'''{intro("Support", "Help centre", "Find out where to join, how to apply for FN SMP, and who to contact when something goes wrong.", button("Contact FN Squad", "/contact/", "ink"))}
    <div id="help-topics">{topic_sections}</div>
    <section class="notice" id="bm" lang="ms"><div><h2>Bantuan dalam Bahasa Melayu</h2><p>Gunakan <a href="/community/#official-links">direktori rasmi</a> untuk menyertai komuniti. Untuk pertanyaan atau bantuan, gunakan <a href="/contact/#bm">saluran hubungan FN Squad</a>.</p></div></section>'''


def contact():
    options = [
        ("general", "General enquiries", "Ask about the community or its projects.", "General enquiry"),
        ("collaboration", "Collaborations", "Share an idea for a creator project or partnership.", "Collaboration and partnership"),
        ("editorial", "Editorial & copyright", "Include the story link and explain the issue.", "FreakyNews correction or copyright"),
        ("privacy", "Privacy & personal data", "Request access, a correction or deletion.", "Privacy or personal data request"),
    ]
    cards = "".join(f'<article class="contact-card" id="{key}"><h3>{esc(title)}</h3><p>{desc}</p>{link("Open email draft", email(subject), cls="text-link", arrow=True)}</article>' for key, title, desc, subject in options)
    return f'''{intro("Support", "Contact FN Squad", "Email the team directly or choose a topic to open a draft with a subject line.")}
    <section class="notice email-notice"><div><h2>Official inbox</h2><p>{link(EMAIL, email())}</p></div><div class="actions">{button("Open email", email(), "ink")}<button type="button" class="button button-plain" data-copy="{EMAIL}" hidden>Copy address</button></div><span class="status-copy" role="status"></span></section>
    <section class="section">{section_head("Choose a topic")}<div class="contact-grid">{cards}</div></section>
    <section class="notice" id="safety"><div><h2>Community reports</h2><p>Contact an admin or moderator privately and redact unrelated information from evidence.</p></div>{button("Reporting instructions", "/community/#report")}</section>
    <section class="section compact-prose" id="bm" lang="ms"><h2>Hubungi FN Squad</h2><p>Hantar pertanyaan anda ke {link(EMAIL, email())}. Untuk melaporkan isu keselamatan dalam komuniti, hubungi pentadbir atau moderator secara peribadi.</p></section>'''


def about():
    team = [
        ("Faiz", "Ares / Tron:Ares", "Founder, Owner & CEO", "Guides the squad’s direction, identity and community projects."),
        ("Harkesh", "Prometheus", "Co-Owner, Co-Founder & Creative Director", "Leads the visual identity and creative direction."),
        ("Asyraf", "Hera", "Finance & Marketing", "Coordinates finance, marketing and partnership enquiries."),
        ("Firas", "Daredevil", "Producer / Director", "Organises productions, scheduling and creative workflows."),
    ]
    cards = "".join(f'<article class="contact-card member"><span class="initial" aria-hidden="true">{title[0]}</span><span class="meta-label">{esc(alias)}</span><h3>{title}</h3><strong>{esc(role)}</strong><p>{description}</p></article>' for title, alias, role, description in team)
    return f'''{intro("About FN Squad", "Meet the squad.", "We’re an independent Malaysian creator and gaming community. Our projects bring together Minecraft, news, culture and the people who make them happen.", button("Contact the team", "/contact/", "ink") + button("Website history", "#origins"))}
    <section class="section" id="the-four">{section_head("The team")}<div class="team-grid">{cards}</div></section>
    <section class="section" id="origins" aria-labelledby="history-title">
      <div class="section-heading"><h2 id="history-title">How this site was built</h2></div>
      <ol class="site-history" role="list">
        <li>
          <span class="meta-label">Original Era archive</span>
          <h3>From a gaming homepage</h3>
          <p>The archive repository’s first commit dates to <time datetime="2024-09">September 2024</time>. The <time datetime="2026-04">April 2026</time> snapshot shows the site’s dark gaming layout, animated FN branding, Minecraft server pages and feedback page.</p>
          <p>The archive retains its historical wording and artwork. Use the <a href="/fn-smp/#join">current FN SMP guide</a> for joining and connection information.</p>
          <div class="history-links">{link("Browse the archive", ARCHIVE, cls="text-link", arrow=True)}{link("Commit history", ARCHIVE_HISTORY, cls="text-link", arrow=True)}</div>
        </li>
        <li>
          <span class="meta-label">Official FN Squad site</span>
          <h3>Into a community hub</h3>
          <p>The current GitHub repository began in <time datetime="2026-10">October 2026</time>. It brought FreakyNews, FN SMP and community links together under the FN Squad name, using the monochrome FN identity, light and dark modes, and a frosted, floating menu.</p>
          <p>The following updates added cleaner URLs, an official links directory and source links for FreakyNews.</p>
          <div class="history-links">{link("Explore the public repository", PUBLIC_SOURCE, cls="text-link", arrow=True)}</div>
        </li>
        <li>
          <span class="meta-label">Liquid Glass redesign</span>
          <h3>A clearer way to explore</h3>
          <p>The redesign builds on the frosted menu with a Liquid Glass header and controls that work in both themes. It reworks the mobile menu and social directory, with clearer paths to news, Minecraft and community help.</p>
          <p>FreakyNews search and topic filters run in the browser. Saved links to the old page URLs lead to the new pages.</p>
          <div class="history-links">{link("Explore FreakyNews", "/freakynews/", cls="text-link", arrow=True)}{link("See official community links", "/community/#official-links", cls="text-link", arrow=True)}</div>
        </li>
      </ol>
      <aside class="craft-notes"><h3>Under the hood</h3><p>A small Python build script generates the static HTML from shared templates. CSS shapes the responsive layout and glass effects. JavaScript handles the menu, theme switch and news filters. Fonts and logos are served with the site, and the public build is packaged for GitHub Pages.</p></aside>
    </section>
    <section class="section compact-prose" id="bm" lang="ms"><h2>Mengenali FN Squad</h2><p>FN Squad ialah komuniti permainan video dan kumpulan pencipta kandungan bebas yang berpangkalan di Malaysia. Kami mengendalikan FN SMP dan FreakyNews serta berhubung melalui WhatsApp dan Discord.</p><p>Laman asal bermula sebagai laman permainan. Kini, FN Squad menghimpunkan FreakyNews, FN SMP dan pautan komuniti dalam reka bentuk Liquid Glass. {link("Lihat arkib laman asal", ARCHIVE)}.</p></section>'''


def privacy(public):
    github_notice = 'GitHub Pages hosts the public FN Squad site and records visitor IP addresses for security.'
    github_notice_ms = 'GitHub Pages mengehoskan laman awam FN Squad dan merekodkan alamat IP untuk tujuan keselamatan.'
    if public:
        hosting = f'<p>{github_notice} See {link("GitHub Pages data collection", GITHUB_PRIVACY)}.</p>'
        hosting_ms = f'<p>{github_notice_ms} Rujuk {link("maklumat GitHub Pages", GITHUB_PRIVACY)}.</p>'
    else:
        hosting = (f'<p>This private review is hosted through ChatGPT Sites. The provider handles sign-in and hosting data. '
                   f'See {link("OpenAI privacy resources", OPENAI_PRIVACY)}.</p><p>{github_notice} '
                   f'See {link("GitHub Pages data collection", GITHUB_PRIVACY)}.</p>')
        hosting_ms = (f'<p>Versi semakan ini dihoskan melalui ChatGPT Sites. Rujuk {link("sumber privasi OpenAI", OPENAI_PRIVACY)}. '
                      f'{github_notice_ms} Rujuk {link("maklumat GitHub Pages", GITHUB_PRIVACY)}.</p>')
    return document("Privacy notice", "How this site handles your browser preferences, external links and community reports.", [
        ("website", "Website visits", f'''<p>FN Squad is an independent community based in Malaysia. The website itself has no registration or upload forms, analytics scripts, advertising trackers or social embeds. FreakyNews search and topic filters run in your browser.</p>
        <p>Your browser saves your appearance choice under <code>fn-theme</code>. Clear the site’s browser data to remove it.</p>
        {hosting}'''),
        ("platforms", "External platforms", f'''<p>When you open a link to a third-party service, that provider handles your visit, account activity and settings under its own policies. In a WhatsApp group, other members can see your phone number. WhatsApp Channels apply different visibility rules for followers.</p>
        <p>{link("WhatsApp privacy policy", WHATSAPP_PRIVACY, arrow=True)} · {link("Group privacy settings", WHATSAPP_GROUPS, arrow=True)} · {link("Channel privacy", WHATSAPP_CHANNELS, arrow=True)} · {link("Discord privacy policy", DISCORD_PRIVACY, arrow=True)}</p>'''),
        ("reports", "Community reports", '''<p>Staff may receive usernames, messages, screenshots, timestamps and relevant Minecraft server logs when investigating reports, enforcing rules or reviewing appeals. Send reports privately and limit them to relevant information. Redact unrelated personal details from screenshots.</p><p>Ask staff who can see the report and how long it may be retained before sharing sensitive evidence.</p>'''),
        ("choices", "Requests and complaints", f'''<p>Email {link(EMAIL, email("Privacy or personal data request"))} to ask about the information FN Squad holds, request a correction or deletion, or raise a concern. Include the platform and approximate date. Send provider-held data requests to that provider.</p>
        <p>For Malaysian personal data complaints, see {link("the Personal Data Protection Commissioner (JPDP)", MY_COMPLAINT, arrow=True)}. For communications and multimedia matters, see {link("MCMC complaint channels", MCMC_GUIDE, arrow=True)}.</p>'''),
        ("retention", "Retention and security", '''<p>FN Squad’s public materials do not specify a fixed retention schedule for reports or server logs. Ask about the retention period for your case. External providers apply their own retention practices.</p><p>Report suspected unauthorised disclosure privately using the contact options above.</p>'''),
        ("standards", "Laws and references", f'''<p>Malaysia’s Personal Data Protection Act 2010 and its amendments address personal data processing in connection with commercial transactions. Applicable obligations depend on the activity and circumstances. The JPDP sources explain the Act and its scope.</p><p>{link("Act 709 and amendments", MY_PRIVACY, arrow=True)} · {link("JPDP guidance on scope", MY_SCOPE, arrow=True)}</p>'''),
        ("transparency", "Transparency", f'''<p>The statement on GitHub records the public site’s original privacy review and the governance questions it identified, including {link("ISO/IEC 27001", ISO_SECURITY)} and {link("ISO/IEC 27701", ISO_PRIVACY)} as planning references.</p><p>{link("Public transparency statement on GitHub", PUBLIC_POLICY, arrow=True)}</p>'''),
    ], f'''<section id="bm" lang="ms"><h2>Notis Privasi FN Squad</h2>
    <h3>Lawatan laman web</h3><p>Kod laman ini tidak menggunakan analitik, penjejak iklan, borang pendaftaran atau borang muat naik. Carian FreakyNews dijalankan dalam pelayar. Tetapan tema disimpan dalam storan setempat pelayar dan boleh dipadamkan melalui tetapan pelayar.</p>
    {hosting_ms}
    <h3>Platform luar dan laporan</h3><p>Ahli kumpulan WhatsApp boleh melihat nombor telefon anda. Saluran WhatsApp menggunakan tetapan keterlihatan yang berbeza. Hantar laporan terus kepada pentadbir atau moderator dan padamkan butiran peribadi yang tidak berkaitan. Sila tanya tempoh penyimpanan bagi laporan anda.</p>
    <h3>Pertanyaan dan aduan</h3><p>E-mel {link(EMAIL, email("Privacy or personal data request"))} untuk pertanyaan, pembetulan atau permohonan pemadaman. Rujuk {link("JPDP", MY_COMPLAINT)} bagi aduan berkaitan data peribadi dan {link("saluran aduan MCMC", MCMC_GUIDE_MS)} bagi perkara komunikasi dan multimedia. Skop {link("Akta 709", MY_PRIVACY)} bergantung pada aktiviti dan keadaan.</p></section>''')


def legal():
    policies = [
        ("Privacy notice", "Site visits, external platforms and personal data requests.", "/privacy/"),
        ("Terms of use", "Website use, conduct and content.", "/terms/"),
        ("Community rules", "House rules, moderation and how to report an issue.", "/community/#rules"),
        ("Editorial standards", "Sourcing, corrections and copyright enquiries.", "/editorial/"),
    ]
    cards = "".join(f'<a class="policy-card" href="{url}"><div><h2>{title}</h2><p>{description}</p></div><span class="arrow arrow-right" aria-hidden="true"></span></a>' for title, description, url in policies)
    return f'''{intro("FN Squad policies", "Policies & notices", "Find the rules and notices that apply to the website and our community spaces.")}
    <div class="policy-grid" id="directory">{cards}</div>
    <div class="prose compact-prose section">
      <section id="contact"><h2>Contact and requests</h2><p>Use the <a href="/contact/">FN Squad contact page</a> for private questions, reports and corrections.</p></section>
      <section id="accessibility"><h2>Accessibility</h2><p>FN Squad uses the {link("W3C Web Content Accessibility Guidelines (WCAG 2.2)", W3C, arrow=True)} as a reference. A full conformance audit is pending. <a href="/contact/">Contact FN Squad</a> if you encounter a barrier.</p></section>
      <section id="references"><h2>Privacy and transparency references</h2><p>See the <a href="/privacy/#standards">Malaysian legal references</a> and the <a href="/privacy/#transparency">transparency statement</a> for context and links to primary sources.</p></section>
      <section id="bm" lang="ms"><h2>Dasar dan notis FN Squad</h2><p>Semak <a href="/privacy/#bm">notis privasi</a>, <a href="/terms/#bm">terma penggunaan</a> dan <a href="/editorial/#bm">piawaian editorial</a> dalam Bahasa Melayu.</p></section>
    </div>'''


def terms():
    return document("Terms of use", "Terms for visiting this website and participating in FN Squad community spaces.", [
        ("scope", "Scope and operator", "<p>FN Squad is an independent Malaysian creator and gaming community. WhatsApp, Discord and Minecraft have their own terms, privacy policies and minimum age requirements.</p>"),
        ("conduct", "Acceptable use", '<p>Follow the <a href="/community/#rules">community rules</a>. Do not harass, defraud, dox or impersonate others, share harmful material, or attempt to interfere with the site or platforms. Moderators apply the published <a href="/community/#consequences">enforcement and appeal process</a>.</p>'),
        ("content", "Content and attribution", '<p>Creators and rights holders retain their rights. Credit the original source and obtain permission when required before reuse. Send rights and credit concerns through the <a href="/contact/#editorial">editorial contact</a>.</p>'),
        ("platforms", "External links and privacy", '<p>Linked services operate separately and may change availability or require sign-in. Read the <a href="/privacy/">privacy notice</a> before sending personal information or evidence.</p>'),
        ("risk", "Availability and corrections", '<p>Site content and community services may change or be interrupted. FreakyNews summaries link to the original sources. Use our <a href="/editorial/#corrections">correction process</a> to flag an error.</p>'),
        ("law", "Applicable rights and contact", '<p>Rights and duties under applicable law continue to apply. <a href="/contact/">Contact FN Squad</a> for questions or concerns.</p>'),
    ], '''<section id="bm" lang="ms"><h2>Terma Penggunaan FN Squad</h2>
    <p>FN Squad ialah komuniti bebas di Malaysia. Patuhi <a href="/community/#rules">peraturan komuniti</a> serta terma dan had umur platform yang anda gunakan. Gangguan, penipuan, penyamaran dan pendedahan maklumat peribadi tanpa izin adalah dilarang.</p>
    <p>Hak cipta kekal pada pemilik masing-masing. Nyatakan sumber asal dan dapatkan kebenaran jika perlu. Perkhidmatan dan kandungan boleh berubah. Hak di bawah undang-undang yang terpakai terus berkuat kuasa. <a href="/contact/#bm">Hubungi FN Squad</a> bagi pertanyaan, aduan atau pembetulan.</p></section>''')


def editorial():
    return document("Editorial standards", "How FreakyNews chooses sources, labels stories and handles corrections.", [
        ("purpose", "Scope and labels", "<p>FreakyNews publishes community-curated links and summaries. Identify company announcements, reported news and opinion so readers can tell them apart.</p>"),
        ("sources", "Sourcing and verification", "<p>Prefer identifiable primary sources and trustworthy reporting. Check the date, original context and corroboration, and include a link for readers. Attribute claims from companies and public figures to their source.</p>"),
        ("corrections", "Corrections and requests", '<p>Use the <a href="/contact/#editorial">editorial contact</a> and include the story link, the statement in question and any source that can help verify it. When we substantively correct a story, explain the change where readers can see it.</p>'),
        ("safety", "Care, fairness and rights", "<p>Take extra care with allegations, minors, private information and sensitive topics. Leave out unnecessary identifying information. Credit sources and respect copyright when using other people’s work.</p>"),
    ], '''<section id="bm" lang="ms"><h2>Piawaian Editorial FreakyNews</h2>
    <p>Utamakan sumber asal dan laporan yang boleh dipercayai. Semak tarikh, konteks dan bukti sokongan. Nyatakan sumber dan bezakan pengumuman, laporan berita dan pendapat.</p>
    <p>Berhati-hati dengan dakwaan dan maklumat yang mengenal pasti individu, terutamanya kanak-kanak. Untuk pembetulan, berikan pautan artikel dan butiran kesilapan melalui <a href="/contact/#editorial">saluran editorial</a>.</p></section>''')


PAGES = [
    ("/", "FN Squad", "Explore FN SMP, FreakyNews and the official FN Squad community directory.", home),
    ("/community/", "Community", "Official Discord and WhatsApp links, community rules and moderation.", community),
    ("/fn-smp/", "FN SMP", "FN Squad Minecraft whitelist application, server rules and FAQ.", smp),
    ("/freakynews/", "FreakyNews", "Curated news about gaming, tech, Malaysia, sports and culture.", news),
    ("/about/", "About", "Meet the FN Squad creator team and explore the site’s history.", about),
    ("/contact/", "Contact", "FN Squad’s official email and private reporting options.", contact),
    ("/help/", "Help centre", "Answers about FN Squad, FN SMP, joining, reports and privacy.", help_page),
    ("/legal/", "Policies & notices", "Terms of use, privacy, accessibility and community policies.", legal),
    ("/terms/", "Terms of use", "Rules for FN Squad’s website and community spaces.", terms),
    ("/editorial/", "Editorial standards", "FreakyNews sourcing, corrections and editorial practices.", editorial),
]


def build(output, public):
    pages = [*PAGES, ("/privacy/", "Privacy notice", "Website privacy, third-party platforms and data requests.", lambda: privacy(public))]
    base_path = PAGES_BASE_PATH if public else ""

    def write_page(path, document):
        # Templates use site-relative paths. Mount navigation and assets under the Pages project path.
        if base_path:
            document = ROOT_LINK.sub(lambda link: f"{link[1]}{base_path}{link[2]}", document)
        path.write_text(document, encoding="utf-8")

    for route, title, description, render in pages:
        directory = output / route.strip("/")
        directory.mkdir(parents=True, exist_ok=True)
        write_page(directory / "index.html", layout(route, title, description, render(), public=public))
        if route != "/":
            legacy = output / (route.strip("/") + ".html")
            canonical = f'<link rel="canonical" href="{PAGES_URL}{route}">' if public else ""
            write_page(legacy, f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="{'noindex, follow' if public else 'noindex, nofollow'}">{canonical}<title>{esc(title)} · FN Squad</title><noscript><meta http-equiv="refresh" content="0; url={base_path}{route}"></noscript></head>
<body><p>This page has moved. <a id="destination" href="{route}">Continue to {esc(title)}</a>.</p><script>const target = document.getElementById("destination"); window.location.replace(target.href + window.location.search + window.location.hash);</script></body></html>''')
    write_page(output / "404.html", layout("/404/", "Page not found", "Find your way back to FN Squad.", intro("404", "Page not found", "The link may have moved. Try the homepage or the official community directory.", button("Back to FN Squad", "/", "ink") + button("Official links", "/community/#official-links")), public=public, error=True))
    sitemap = output / "sitemap.xml"
    if public:
        urls = "".join(f"  <url><loc>{PAGES_URL}{route}</loc></url>\n" for route, *_ in pages)
        sitemap.write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + '</urlset>\n', encoding="utf-8")
        robots = f"User-agent: *\nAllow: {PAGES_BASE_PATH}/\nSitemap: {PAGES_URL}/sitemap.xml\n"
    else:
        sitemap.unlink(missing_ok=True)
        robots = "User-agent: *\nDisallow: /\n"
    (output / "robots.txt").write_text(robots, encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=("private-review", "github-pages"), default="private-review")
    parser.add_argument("--output", type=Path, default=DIST, help="Folder containing the site's static assets (default: dist).")
    args = parser.parse_args()
    build(args.output, public=args.target == "github-pages")
