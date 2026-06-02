import json
import re
from datetime import date
from xml.etree.ElementTree import Element, SubElement, tostring

from django.contrib import messages
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify

from .models import InternalLink, OutboundLink, SEOPage, SEOPageTemplate, contact


SITE_URL = "https://www.inkagrowth.com"
BRAND_NAME = "InkaGROWTH"
CONTACT_EMAIL = "info@inkagrowth.com"
CONTACT_PHONE = "+91 9389826074"
TRANSITION_WORDS = [
    "additionally",
    "furthermore",
    "moreover",
    "however",
    "therefore",
    "meanwhile",
    "consequently",
    "as a result",
    "in addition",
    "for example",
    "similarly",
    "finally",
]

DEFAULT_INTERNAL_LINKS = [
    {"title": "SEO services", "url": "/seo-services/", "category": "seo"},
    {"title": "website development", "url": "/website-development/", "category": "web"},
    {"title": "social media marketing", "url": "/social-media-marketing/", "category": "social"},
    {"title": "Google Ads management", "url": "/google-ads-services/", "category": "ads"},
    {"title": "digital marketing services", "url": "/digital-marketing-services/", "category": "marketing"},
    {"title": "contact our growth team", "url": "/contact/", "category": "general"},
    {"title": "meet the INKAGROWTH team", "url": "/team/", "category": "general"},
]

DEFAULT_OUTBOUND_LINKS = [
    {"title": "Google Search Central", "url": "https://developers.google.com/search", "category": "seo"},
    {"title": "Google Business Profile", "url": "https://www.google.com/business/", "category": "local"},
    {"title": "Google Analytics", "url": "https://analytics.google.com", "category": "analytics"},
    {"title": "Google Ads", "url": "https://ads.google.com/home/", "category": "ads"},
    {"title": "Search Console", "url": "https://search.google.com/search-console", "category": "seo"},
    {"title": "PageSpeed Insights", "url": "https://pagespeed.web.dev", "category": "performance"},
]

STATIC_FRONTEND_PATHS = {
    "/",
    "/seo-services/",
    "/social-media-marketing/",
    "/google-ads-services/",
    "/website-development/",
    "/digital-marketing-services/",
    "/privacy-policy/",
    "/terms-and-conditions/",
    "/disclaimer/",
    "/cookie-policy/",
    "/contact/",
    "/team/",
}

GLOBAL_FAQS = [
    {
        "question": "How long does SEO take to show results?",
        "answer": "Most SEO campaigns begin showing measurable movement within 3 to 6 months, depending on competition, technical health, content depth, and authority.",
    },
    {
        "question": "Do you build SEO-friendly websites?",
        "answer": "Yes. We build fast, mobile-friendly websites with clean structure, optimized metadata, schema markup, and conversion-focused page layouts.",
    },
    {
        "question": "Can InkaGROWTH manage Google Ads campaigns?",
        "answer": "Yes. We manage Google Search, Display, Performance Max, remarketing, and lead generation campaigns with clear tracking and ongoing optimization.",
    },
    {
        "question": "Do you provide social media marketing?",
        "answer": "Yes. We create content plans, manage publishing, improve engagement, and run paid social campaigns for brand awareness and lead generation.",
    },
    {
        "question": "What is included in digital marketing services?",
        "answer": "Digital marketing can include SEO, content strategy, social media, paid ads, website improvements, analytics, and conversion optimization.",
    },
    {
        "question": "Will my website be optimized for Core Web Vitals?",
        "answer": "We optimize page structure, image loading, static assets, responsive behavior, and technical SEO signals that affect Core Web Vitals.",
    },
    {
        "question": "Do you provide monthly reports?",
        "answer": "Yes. Campaigns include practical reporting on traffic, rankings, leads, ad spend, conversions, and next-step recommendations.",
    },
    {
        "question": "Can you help local businesses rank in Google?",
        "answer": "Yes. We optimize local landing pages, Google Business Profile signals, citations, reviews, and location-focused content.",
    },
    {
        "question": "How do you measure marketing performance?",
        "answer": "We align tracking with business goals and monitor search visibility, qualified traffic, leads, conversion rates, ad performance, and ROI.",
    },
    {
        "question": "How can I start working with InkaGROWTH?",
        "answer": "Send a message through the contact page or call +91 9389826074. We will review your goals and recommend the right growth plan.",
    },
]

SERVICE_PAGES = {
    "seo-services": {
        "title": "SEO Services | InkaGROWTH",
        "description": "Professional SEO services by InkaGROWTH to improve rankings, organic traffic, local visibility, and qualified leads.",
        "service": "SEO Services",
        "icon": "fas fa-chart-line",
        "hero": "SEO Services That Build Sustainable Organic Growth",
        "intro": "InkaGROWTH helps businesses improve search visibility with technical SEO, keyword strategy, content optimization, local SEO, and authority building.",
        "benefits": [
            "Technical audits that remove crawl and indexing barriers.",
            "Keyword and content strategy mapped to buyer intent.",
            "Local SEO improvements for Google Business Profile visibility.",
            "Transparent reporting focused on rankings, leads, and revenue.",
        ],
        "process": [
            "Audit website health, search demand, competitors, and analytics.",
            "Fix technical SEO, metadata, internal links, and page structure.",
            "Publish optimized service content and supporting blog topics.",
            "Monitor rankings, conversions, and Core Web Vitals every month.",
        ],
    },
    "social-media-marketing": {
        "title": "Social Media Marketing Services | InkaGROWTH",
        "description": "Social media marketing services for brand awareness, content planning, engagement, lead generation, and paid social growth.",
        "service": "Social Media Marketing",
        "icon": "fas fa-hashtag",
        "hero": "Social Media Marketing That Turns Attention Into Trust",
        "intro": "We plan, create, publish, and optimize social campaigns that help brands stay visible, credible, and memorable across Instagram, Facebook, LinkedIn, and more.",
        "benefits": [
            "Platform-specific content calendars and creative direction.",
            "Consistent brand voice across posts, reels, and campaigns.",
            "Community engagement that builds trust and repeat attention.",
            "Paid social campaigns optimized for reach, leads, and conversions.",
        ],
        "process": [
            "Define audience segments, content pillars, and campaign goals.",
            "Create monthly content plans with captions, creatives, and offers.",
            "Publish, manage engagement, and test high-performing formats.",
            "Report on reach, engagement, leads, and audience growth.",
        ],
    },
    "google-ads-services": {
        "title": "Google Ads Management Services | InkaGROWTH",
        "description": "Google Ads management for Search, Display, Performance Max, remarketing, and lead generation campaigns with ROI-focused optimization.",
        "service": "Google Ads Management",
        "icon": "fas fa-ad",
        "hero": "Google Ads Campaigns Built For Measurable Leads",
        "intro": "InkaGROWTH manages Google Ads campaigns with conversion tracking, landing page alignment, keyword control, and continuous budget optimization.",
        "benefits": [
            "Search campaigns targeting high-intent buyers.",
            "Conversion tracking configured for calls, forms, and sales.",
            "Negative keyword and bid optimization to reduce wasted spend.",
            "Clear reporting on cost per lead, conversions, and ROAS.",
        ],
        "process": [
            "Audit goals, offers, landing pages, and tracking readiness.",
            "Build campaign structure, keywords, ads, audiences, and extensions.",
            "Launch with daily checks for spend, search terms, and conversions.",
            "Optimize bids, budgets, creatives, and landing pages for ROI.",
        ],
    },
    "website-development": {
        "title": "Website Development Services | InkaGROWTH",
        "description": "Website development services for fast, mobile-friendly, SEO-ready business websites designed to convert visitors into leads.",
        "service": "Website Development",
        "icon": "fas fa-code",
        "hero": "Fast, SEO-Ready Websites Built To Convert",
        "intro": "We design and develop responsive websites with clean structure, strong messaging, optimized performance, and lead-generation flows.",
        "benefits": [
            "Mobile-first layouts that match modern user behavior.",
            "SEO-ready page architecture, metadata, and schema support.",
            "Fast-loading pages with optimized images and static assets.",
            "Conversion-focused CTAs, forms, and service page structure.",
        ],
        "process": [
            "Plan sitemap, messaging, user journeys, and conversion goals.",
            "Design pages that match the brand and existing visual system.",
            "Develop responsive templates with SEO and performance best practices.",
            "Test forms, links, metadata, schema, mobile layout, and launch readiness.",
        ],
    },
    "digital-marketing-services": {
        "title": "Digital Marketing Services | InkaGROWTH",
        "description": "Full-service digital marketing agency services including SEO, Google Ads, social media marketing, website development, and analytics.",
        "service": "Digital Marketing",
        "icon": "fas fa-bullhorn",
        "hero": "Digital Marketing Services For Predictable Business Growth",
        "intro": "InkaGROWTH combines SEO, paid media, social, website strategy, and analytics into one growth system for businesses that want measurable results.",
        "benefits": [
            "Integrated strategy across search, social, ads, and website.",
            "Unified reporting across channels and lead sources.",
            "Stronger brand visibility with conversion-focused execution.",
            "Flexible campaigns for local businesses, startups, and service brands.",
        ],
        "process": [
            "Review business goals, current channels, analytics, and competitors.",
            "Build a channel plan with priorities, budget, content, and offers.",
            "Execute campaigns across SEO, ads, social, and web improvements.",
            "Measure performance and refine the strategy every month.",
        ],
    },
}

LEGAL_PAGES = {
    "privacy-policy": {
        "title": "Privacy Policy | InkaGROWTH",
        "description": "Read the InkaGROWTH Privacy Policy for how we collect, use, protect, and manage information submitted through our website.",
        "heading": "Privacy Policy",
        "sections": [
            ("Information We Collect", "We may collect your name, email address, phone number, website details, and message when you submit a form or contact us about our services."),
            ("How We Use Information", "We use submitted information to respond to enquiries, provide consultations, improve our services, manage client communication, and maintain business records."),
            ("Data Protection", "We use reasonable administrative and technical safeguards to protect information from unauthorized access, misuse, disclosure, or alteration."),
            ("Third-Party Services", "We may use analytics, advertising, hosting, CRM, and communication tools to operate the website and deliver digital marketing services."),
            ("Your Choices", "You can request access, correction, or deletion of your personal information by contacting info@inkagrowth.com."),
        ],
    },
    "terms-and-conditions": {
        "title": "Terms & Conditions | InkaGROWTH",
        "description": "Review the InkaGROWTH Terms & Conditions for website use, service enquiries, intellectual property, and professional engagement terms.",
        "heading": "Terms & Conditions",
        "sections": [
            ("Website Use", "By using this website, you agree to access it lawfully and avoid actions that may disrupt, damage, or misuse the website or its content."),
            ("Service Information", "Website content describes our digital marketing services for general information and does not guarantee identical outcomes for every business."),
            ("Intellectual Property", "All text, branding, graphics, layouts, and website materials are owned by InkaGROWTH or used with appropriate permission."),
            ("Engagement Terms", "Project scope, deliverables, pricing, timelines, and responsibilities are confirmed separately in written proposals or agreements."),
            ("Limitation of Liability", "InkaGROWTH is not liable for indirect losses arising from website use, third-party platform changes, search algorithm updates, or ad platform policy changes."),
        ],
    },
    "disclaimer": {
        "title": "Disclaimer | InkaGROWTH",
        "description": "Read the InkaGROWTH Disclaimer covering marketing information, expected results, third-party platforms, and professional advice.",
        "heading": "Disclaimer",
        "sections": [
            ("General Information", "The content on this website is provided for general business and marketing information only."),
            ("Performance Results", "SEO, advertising, social media, and website outcomes depend on market competition, budget, website history, offer quality, and external platform changes."),
            ("Third-Party Platforms", "We are not responsible for policy, pricing, algorithm, or product changes made by Google, Meta, LinkedIn, hosting providers, analytics tools, or other third parties."),
            ("Professional Advice", "Website content should not be treated as legal, financial, or tax advice. Please consult qualified professionals for those matters."),
        ],
    },
    "cookie-policy": {
        "title": "Cookie Policy | InkaGROWTH",
        "description": "Read the InkaGROWTH Cookie Policy to understand how cookies and similar technologies may be used on our website.",
        "heading": "Cookie Policy",
        "sections": [
            ("What Cookies Are", "Cookies are small files stored by your browser that help websites remember preferences, measure activity, and improve user experience."),
            ("How We Use Cookies", "We may use cookies for website functionality, analytics, performance measurement, lead attribution, and advertising effectiveness."),
            ("Third-Party Cookies", "Analytics, advertising, embedded media, and social platforms may place cookies according to their own policies."),
            ("Managing Cookies", "You can control or delete cookies through your browser settings. Blocking some cookies may affect website functionality or measurement accuracy."),
        ],
    },
}

TEAM_MEMBERS = [
    {
        "name": "Arpit Kumar",
        "position": "CEO & Founder",
        "employee_id": "INKA2026-CE-001",
        "mobile": "+91 9389826074",
        "email": "arpit@inkagrowth.com",
        "bio": "Founder of InkaGROWTH with expertise in digital marketing, SEO, web development, and business growth strategies.",
        "image": "img/Arpit.jpeg",
    },
    {
        "name": "Prabhat Kumar",
        "position": "Product Manager",
        "employee_id": "INKA2026-PM-002",
        "mobile": "+91 7983837923",
        "email": "prabhat@inkagrowth.com",
        "bio": "Responsible for product planning, execution, and delivering exceptional digital solutions to clients.",
        "image": "img/Prabhat.png",
    },
    {
        "name": "Arvind Pal",
        "position": "Sales Manager",
        "employee_id": "INKA2026-SM-003",
        "mobile": "+91 8168724206",
        "email": "arvind@inkagrowth.com",
        "bio": "Leads client acquisition, business development, and customer relationship management.",
        "image": "img/Arvind.png",
    },
]


def build_url(path):
    return f"{SITE_URL}{path}"


def word_count(text):
    return len(re.findall(r"\b[\w'-]+\b", text or ""))


def keyword_count(text, keyword):
    return len(re.findall(re.escape(keyword), text or "", flags=re.IGNORECASE))


def transition_word_percentage(text):
    sentences = [part.strip().lower() for part in re.split(r"[.!?]+", text or "") if part.strip()]
    if not sentences:
        return 0
    sentences_with_transition = 0
    for sentence in sentences:
        if any(word in sentence for word in TRANSITION_WORDS):
            sentences_with_transition += 1
    return round((sentences_with_transition / len(sentences)) * 100, 2)


def link_category_terms(page):
    service_slug = slugify(page.service)
    return {
        "general",
        service_slug,
        service_slug.replace("-", " "),
        page.service.lower(),
        page.primary_keyword.lower(),
    }


def unique_links(records, fallback_links, focus_keyword):
    seen_urls = set()
    seen_titles = set()
    links = []
    for item in list(records) + fallback_links:
        title = item["title"] if isinstance(item, dict) else item.title
        url = item["url"] if isinstance(item, dict) else item.url
        category = item.get("category", "general") if isinstance(item, dict) else item.category
        if not title or not url:
            continue
        if url in seen_urls or title.lower() in seen_titles:
            continue
        if title.strip().lower() == focus_keyword.lower():
            continue
        seen_urls.add(url)
        seen_titles.add(title.lower())
        links.append({"title": title, "url": url, "category": category})
        if len(links) == 4:
            break
    return links


def rotate_links(records, seed):
    if not records:
        return []
    offset = sum(ord(char) for char in seed) % len(records)
    return records[offset:] + records[:offset]


def select_relevant_links(model, page, fallback_links):
    categories = link_category_terms(page)
    preferred = list(model.objects.filter(category__in=categories).order_by("category", "title").values("title", "url", "category"))
    remaining = list(model.objects.exclude(category__in=categories).order_by("category", "title").values("title", "url", "category"))
    return unique_links(
        [*rotate_links(preferred, page.slug), *rotate_links(remaining, page.slug)],
        fallback_links,
        page.primary_keyword,
    )


def is_internal_link_resolvable(url):
    if not url.startswith("/"):
        return False
    if url in STATIC_FRONTEND_PATHS:
        return True
    slug = url.strip("/")
    if "/" in slug or not slug:
        return False
    return SEOPageTemplate.objects.filter(slug=slug, is_published=True).exists()


def default_content_blocks(page):
    keyword = page.primary_keyword
    service = page.service
    city = page.city
    state = page.state
    return {
        "h1": f"{service} in {city} for Measurable Local Growth",
        "hero_subheadline": (
            f"{keyword} helps local businesses earn attention, leads, and trust with a clear digital growth plan."
        ),
        "intro_para_1": (
            f"{keyword} gives local businesses a practical way to reach buyers when they are ready to act. "
            f"Additionally, it helps your brand appear with a clear offer, useful content, and stronger proof. "
            f"For example, a shop, clinic, institute, or service company in {city} can use focused pages, local search, "
            f"ads, and tracking to turn online visits into enquiries. Therefore, INKAGROWTH builds each plan around "
            f"simple goals: more visibility, better leads, and steady growth."
        ),
        "intro_para_2": (
            f"Furthermore, our team understands how customers compare options across {city} and nearby areas in {state}. "
            f"We write short, clear pages, improve technical signals, and connect campaigns with contact forms and calls. "
            f"However, we do not rely on one channel alone. Instead, we combine content, search, analytics, and conversion "
            f"improvements so your {service} plan keeps working after launch."
        ),
        "sections": [
            {
                "heading_level": "h2",
                "heading": f"Why Businesses Need {service} in {city}",
                "paragraphs": [
                    f"{keyword} matters because customers now research before they call, visit, or buy. Moreover, local competitors are improving their websites and search presence every month. As a result, brands that explain their services clearly and show trust signals win more qualified enquiries.",
                    f"In addition, INKAGROWTH maps your offers to real customer questions. We then build pages, campaigns, and reports that make decisions easier for your audience. Consequently, your business can spend less time guessing and more time serving serious prospects.",
                ],
            },
            {
                "heading_level": "h2",
                "heading": f"Benefits of {service} in {city}",
                "paragraphs": [
                    f"A strong {service} plan improves visibility, website quality, and lead flow. Additionally, it gives your team cleaner data about what people search, which pages convert, and which offers create calls. Similarly, your sales process becomes easier because visitors already understand your value.",
                    f"{keyword} also supports long-term brand trust. For example, helpful content, fast pages, and clear contact options make your company easier to choose. Therefore, each improvement supports both search performance and customer confidence.",
                ],
            },
            {
                "heading_level": "h3",
                "heading": f"Why Choose INKAGROWTH in {city}",
                "paragraphs": [
                    f"INKAGROWTH keeps campaigns practical and transparent. Furthermore, we explain what we are doing, why it matters, and how it affects leads. Meanwhile, your page structure, internal links, outbound references, and schema stay aligned with modern SEO standards.",
                    f"We also keep the design familiar with the existing INKAGROWTH theme. However, the copy changes for each city and service so every page feels relevant instead of duplicated. Finally, that balance helps programmatic pages stay useful for readers and search engines.",
                ],
            },
            {
                "heading_level": "h3",
                "heading": f"Getting Started with {service}",
                "paragraphs": [
                    f"Getting started is simple. First, we review your current website, search visibility, and local competition. Next, we create a focused plan for {keyword} with page content, tracking, and calls to action. Moreover, we check the page before publishing so the core SEO rules are met.",
                    f"Finally, our team monitors performance after the page goes live. As a result, your {service} campaign in {city} can improve with better data, stronger content, and clearer next steps. In addition, we review search terms, page engagement, form quality, and call intent so future updates are based on real customer behaviour.",
                    f"Similarly, we keep recommendations simple for owners and teams. You see what changed, what improved, and what needs attention next. Therefore, the page supports daily business decisions as well as search visibility while staying useful for readers.",
                ],
            },
        ],
    }


def page_content(page):
    defaults = default_content_blocks(page)
    custom = page.content_blocks or {}
    sections = custom.get("sections") or defaults["sections"]
    return {
        **defaults,
        **{key: value for key, value in custom.items() if value not in (None, "", [], {})},
        "sections": sections,
    }


def default_nearby_areas(page):
    areas = page.nearby_areas or ["Moradabad", "Sambhal", "Bhajoi", "Badaun", "Amroha", page.city]
    area_slugs = {area: f"{slugify(page.service)}-in-{slugify(area)}" for area in areas}
    published_slugs = set(
        SEOPageTemplate.objects.filter(slug__in=area_slugs.values(), is_published=True).values_list("slug", flat=True)
    )
    nearby_areas = []
    for area in areas:
        slug = area_slugs[area]
        url = f"/{slug}/" if slug in published_slugs else ""
        nearby_areas.append({"name": area, "url": url})
    return nearby_areas


def default_faqs(page):
    if page.faqs:
        return page.faqs
    return [
        {
            "question": f"Why should businesses invest in {page.service} in {page.city}?",
            "answer": f"{page.primary_keyword} helps local businesses improve visibility, trust, and enquiries. Additionally, a focused plan makes it easier for customers to find the right offer quickly.",
        },
        {
            "question": f"How much does {page.service} cost in {page.city}?",
            "answer": f"Cost depends on goals, competition, and scope. However, INKAGROWTH keeps pricing transparent and recommends the right plan after reviewing your current digital presence.",
        },
        {
            "question": f"How long does it take to see results from {page.service} in {page.city}?",
            "answer": "SEO-led work often needs 3 to 6 months, while paid campaigns can move faster. Meanwhile, tracking helps us improve pages and campaigns every month.",
        },
        {
            "question": f"Does INKAGROWTH serve nearby areas outside {page.city}?",
            "answer": f"Yes. We serve businesses across {page.state}. Furthermore, our remote workflow keeps planning, reporting, and support simple for nearby cities.",
        },
    ]


def seo_page_schema(page, canonical, faqs):
    return jsonld(
        {
            "@context": "https://schema.org",
            "@type": "Service",
            "name": page.service,
            "serviceType": page.service,
            "provider": {"@type": "Organization", "name": BRAND_NAME, "url": SITE_URL},
            "areaServed": {"@type": "City", "name": page.city},
            "url": canonical,
            "description": page.meta_description,
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": faq["question"],
                    "acceptedAnswer": {"@type": "Answer", "text": faq["answer"]},
                }
                for faq in faqs
            ],
        },
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "Home",
                    "item": SITE_URL,
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": f"{page.service} in {page.city}",
                    "item": canonical,
                },
            ],
        },
    )


def rendered_text_parts(content, faqs, nearby_areas, internal_links, outbound_links):
    parts = [
        content["h1"],
        content["hero_subheadline"],
        content["intro_para_1"],
        content["intro_para_2"],
    ]
    for section in content["sections"]:
        parts.append(section["heading"])
        parts.extend(section.get("paragraphs", []))
    parts.extend(area["name"] for area in nearby_areas)
    parts.extend(link["title"] for link in internal_links + outbound_links)
    for faq in faqs:
        parts.extend([faq.get("question", ""), faq.get("answer", "")])
    return " ".join(parts)


def validate_seo_page(page, content, internal_links, outbound_links, nearby_areas, faqs, canonical, schema_json):
    errors = []
    keyword = page.primary_keyword
    body_text = rendered_text_parts(content, faqs, nearby_areas, internal_links, outbound_links)
    body_words = word_count(body_text)
    density = (keyword_count(body_text, keyword) / max(body_words, 1)) * 100
    heading_matches = 0
    expected_keyword = f"{page.service} in {page.city}"
    expected_title = f"{keyword} | INKAGROWTH"
    for section in content["sections"]:
        heading = section.get("heading", "")
        if page.service.lower() in heading.lower() or page.city.lower() in heading.lower() or keyword.lower() in heading.lower():
            heading_matches += 1

    if not page.is_published:
        errors.append("Page is marked unpublished.")
    if keyword != expected_keyword:
        errors.append('Focus keyphrase must use the "{Service} in {City}" format.')
    if page.meta_title != expected_title:
        errors.append('SEO title must use the "{Service} in {City} | INKAGROWTH" format.')
    if not page.meta_title.startswith(keyword):
        errors.append("SEO title must start with the focus keyphrase.")
    if not 50 <= len(page.meta_title) <= 60:
        errors.append("SEO title must be 50-60 characters.")
    if keyword.lower() not in page.meta_description.lower():
        errors.append("Meta description must contain the exact focus keyphrase.")
    if not 140 <= len(page.meta_description) <= 160:
        errors.append("Meta description must be 140-160 characters.")
    if content["h1"].lower().count(keyword.lower()) != 1:
        errors.append("H1 must contain the focus keyphrase exactly once.")
    if keyword.lower() not in " ".join(re.findall(r"\b[\w'-]+\b", content["intro_para_1"])[:100]).lower():
        errors.append("Focus keyphrase must appear in the first 100 words.")
    if keyword_count(body_text, keyword) < 5:
        errors.append("Focus keyphrase must appear at least 5 times naturally.")
    if body_words < 700:
        errors.append("Content must contain at least 700 words.")
    if not 0.8 <= density <= 2:
        errors.append("Focus keyphrase density must be between 0.8% and 2%.")
    if transition_word_percentage(body_text) <= 15:
        errors.append("Transition words must appear in more than 15% of sentences.")
    if heading_matches < 4:
        errors.append("At least 4 H2/H3 headings must contain service, city, or the service-city combination.")
    if len(internal_links) < 4:
        errors.append("At least 4 internal links are required.")
    if len(outbound_links) < 4:
        errors.append("At least 4 outbound links are required.")
    broken_internal_links = [link["url"] for link in internal_links if not is_internal_link_resolvable(link["url"])]
    if broken_internal_links:
        errors.append(f"Broken internal links are not allowed: {', '.join(broken_internal_links)}.")
    all_urls = [link["url"] for link in internal_links + outbound_links]
    if len(all_urls) != len(set(all_urls)):
        errors.append("Duplicate links are not allowed.")
    if keyword.lower().replace(" ", "-") not in page.slug.lower():
        errors.append("URL slug must contain the focus keyphrase.")
    if not canonical:
        errors.append("Canonical URL must be generated.")
    if not schema_json:
        errors.append("Schema must be generated.")
    if "BreadcrumbList" not in schema_json:
        errors.append("Breadcrumb schema must be generated.")
    return errors


def safe_contact_submit(request, redirect_to):
    if request.method != "POST":
        return False

    contact.objects.create(
        name=request.POST.get("name", "").strip(),
        email=request.POST.get("email", "").strip(),
        mobile=request.POST.get("mobile", "").strip(),
        message=request.POST.get("message", "").strip(),
    )
    messages.success(request, "Your message has been submitted successfully!")
    return redirect(redirect_to)


def faq_schema():
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": faq["question"],
                "acceptedAnswer": {"@type": "Answer", "text": faq["answer"]},
            }
            for faq in GLOBAL_FAQS
        ],
    }


def jsonld(*items):
    return json.dumps([item for item in items if item], ensure_ascii=False)


def xml_response(root):
    xml = b'<?xml version="1.0" encoding="UTF-8"?>\n' + tostring(root, encoding="utf-8")
    response = HttpResponse(xml, content_type="application/xml")
    response.headers.pop("X-Robots-Tag", None)
    return response


def sitemap_urlset(items):
    urlset = Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

    for item in items:
        url = SubElement(urlset, "url")
        SubElement(url, "loc").text = item["loc"]
        SubElement(url, "lastmod").text = item["lastmod"]
        SubElement(url, "changefreq").text = item["changefreq"]
        SubElement(url, "priority").text = item["priority"]

    return urlset


def page_sitemap_items():
    today = date.today().isoformat()
    page_paths = [
        ("/", "daily", "1.0"),
        ("/team/", "monthly", "0.8"),
        ("/contact/", "monthly", "0.8"),
        ("/privacy-policy/", "yearly", "0.6"),
        ("/terms-and-conditions/", "yearly", "0.6"),
        ("/disclaimer/", "yearly", "0.5"),
        ("/cookie-policy/", "yearly", "0.5"),
    ]

    return [
        {
            "loc": build_url(path),
            "lastmod": today,
            "changefreq": changefreq,
            "priority": priority,
        }
        for path, changefreq, priority in page_paths
    ]


def service_sitemap_items():
    today = date.today().isoformat()
    service_paths = [
        ("/seo-services/", "weekly", "0.9"),
        ("/social-media-marketing/", "weekly", "0.9"),
        ("/google-ads-services/", "weekly", "0.9"),
        ("/website-development/", "weekly", "0.9"),
        ("/digital-marketing-services/", "weekly", "0.9"),
    ]
    items = [
        {
            "loc": build_url(path),
            "lastmod": today,
            "changefreq": changefreq,
            "priority": priority,
        }
        for path, changefreq, priority in service_paths
    ]

    for page in SEOPageTemplate.objects.filter(is_published=True).order_by("slug"):
        items.append(
            {
                "loc": build_url(f"/{page.slug}/"),
                "lastmod": today,
                "changefreq": "weekly",
                "priority": "0.7",
            }
        )

    return items


def robots_txt(request):
    response = render(request, "robots.txt", content_type="text/plain")
    response.headers.pop("X-Robots-Tag", None)
    return response


def sitemap_xml(request):
    sitemapindex = Element(
        "sitemapindex",
        xmlns="http://www.sitemaps.org/schemas/sitemap/0.9",
    )
    today = date.today().isoformat()

    for sitemap_path in ["/sitemap-services.xml", "/sitemap-pages.xml"]:
        sitemap = SubElement(sitemapindex, "sitemap")
        SubElement(sitemap, "loc").text = build_url(sitemap_path)
        SubElement(sitemap, "lastmod").text = today

    return xml_response(sitemapindex)


def sitemap_services_xml(request):
    return xml_response(sitemap_urlset(service_sitemap_items()))


def sitemap_pages_xml(request):
    return xml_response(sitemap_urlset(page_sitemap_items()))


def ping(request):
    return HttpResponse("OK")

# HOME PAGE
def index(request):
    submitted = safe_contact_submit(request, "/")
    if submitted:
        return submitted

    organization_schema = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": BRAND_NAME,
        "url": SITE_URL,
        "logo": build_url("/static/img/logo.png"),
        "email": CONTACT_EMAIL,
        "telephone": CONTACT_PHONE,
        "sameAs": [
            "https://www.linkedin.com/company/inkagrowth/",
            "https://www.instagram.com/inkagrowth/",
            "https://www.facebook.com/profile.php?id=61574394691962",
        ],
    }
    local_business_schema = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": BRAND_NAME,
        "url": SITE_URL,
        "image": build_url("/static/img/logo.png"),
        "email": CONTACT_EMAIL,
        "telephone": CONTACT_PHONE,
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Chandausi",
            "addressRegion": "Uttar Pradesh",
            "addressCountry": "IN",
        },
        "areaServed": "India",
        "priceRange": "$$",
    }

    return render(
        request,
        'index.html',
        {"faqs": GLOBAL_FAQS, "schema_json": jsonld(organization_schema, local_business_schema, faq_schema())},
    )


def service_page(request, slug):
    page = SERVICE_PAGES.get(slug)
    if page is None:
        raise Http404("Service page not found")
    submitted = safe_contact_submit(request, f"/{slug}/")
    if submitted:
        return submitted

    canonical = build_url(f"/{slug}/")
    service_schema = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": page["service"],
        "serviceType": page["service"],
        "provider": {"@type": "Organization", "name": BRAND_NAME, "url": SITE_URL},
        "areaServed": {"@type": "Country", "name": "India"},
        "url": canonical,
        "description": page["description"],
    }
    return render(
        request,
        "service_page.html",
        {
            "page": page,
            "slug": slug,
            "canonical": canonical,
            "faqs": GLOBAL_FAQS,
            "schema_json": jsonld(service_schema, faq_schema()),
        },
    )


def legal_page(request, slug):
    page = LEGAL_PAGES.get(slug)
    if page is None:
        raise Http404("Legal page not found")
    return render(
        request,
        "legal_page.html",
        {
            "page": page,
            "canonical": build_url(f"/{slug}/"),
            "schema_json": jsonld(
                {
                    "@context": "https://schema.org",
                    "@type": "WebPage",
                    "name": page["heading"],
                    "url": build_url(f"/{slug}/"),
                    "description": page["description"],
                }
            ),
        },
    )


def contact_page(request):
    submitted = safe_contact_submit(request, "/contact/")
    if submitted:
        return submitted

    page = {
        "title": "Contact InkaGROWTH | Digital Marketing Agency",
        "description": "Contact InkaGROWTH for SEO, Google Ads, website development, social media marketing, and digital marketing services.",
        "heading": "Contact InkaGROWTH",
    }
    return render(
        request,
        "contact.html",
        {
            "page": page,
            "canonical": build_url("/contact/"),
            "schema_json": jsonld(
                {
                    "@context": "https://schema.org",
                    "@type": "ContactPage",
                    "name": page["heading"],
                    "url": build_url("/contact/"),
                    "description": page["description"],
                }
            ),
        },
    )


def team_page(request):
    canonical = build_url("/team/")
    person_schemas = [
        {
            "@context": "https://schema.org",
            "@type": "Person",
            "name": member["name"],
            "jobTitle": member["position"],
            "identifier": member["employee_id"],
            "telephone": member["mobile"],
            "email": member["email"],
            "image": build_url(f"/static/{member['image']}"),
            "description": member["bio"],
            "worksFor": {
                "@type": "Organization",
                "name": BRAND_NAME,
                "url": SITE_URL,
            },
        }
        for member in TEAM_MEMBERS
    ]
    return render(
        request,
        "team.html",
        {
            "canonical": canonical,
            "team_members": TEAM_MEMBERS,
            "schema_json": jsonld(*person_schemas),
        },
    )


# DYNAMIC SEO PAGE
def dynamic_page(request, slug):

    page = get_object_or_404(
        SEOPageTemplate,
        slug=slug,
    )

    # CONTACT FORM
    submitted = safe_contact_submit(request, f"/{slug}/")
    if submitted:
        return submitted

    # DYNAMIC IMAGES
    if page.service == "SEO Services":

        image_url = "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=700&h=500&fit=crop&auto=format"

    elif page.service == "Website Development":

        image_url = "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=700&h=500&fit=crop&auto=format"

    else:

        image_url = "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=700&h=500&fit=crop&auto=format"

    content = page_content(page)
    internal_links = select_relevant_links(InternalLink, page, DEFAULT_INTERNAL_LINKS)
    outbound_links = select_relevant_links(OutboundLink, page, DEFAULT_OUTBOUND_LINKS)
    nearby_areas = default_nearby_areas(page)
    faqs = default_faqs(page)
    canonical = build_url(f"/{page.slug}/")
    schema_json = seo_page_schema(page, canonical, faqs)
    validation_errors = validate_seo_page(
        page,
        content,
        internal_links,
        outbound_links,
        nearby_areas,
        faqs,
        canonical,
        schema_json,
    )

    if validation_errors:
        return HttpResponse(
            "SEO page validation failed:\n- " + "\n- ".join(validation_errors),
            status=422,
            content_type="text/plain",
        )

    context = {

        'service': page.service,

        'city': page.city,

        'image_url': image_url,

        'state': page.state,

        'primary_keyword': page.primary_keyword,

        'h1': content["h1"],

        'hero_subheadline': content["hero_subheadline"],

        'intro_para_1': content["intro_para_1"],

        'intro_para_2': content["intro_para_2"],

        'content_sections': content["sections"],

        'meta_title': page.meta_title,

        'meta_description': page.meta_description,

        'slug': page.slug,

        'canonical': canonical,

        'schema_json': schema_json,

        'internal_links': internal_links,

        'outbound_links': outbound_links,

        'nearby_areas': nearby_areas,

        'faqs': faqs,
    }

    return render(
        request,
        'seo_page.html',
        context
    )
