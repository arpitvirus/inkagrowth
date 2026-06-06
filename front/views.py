import json
from datetime import date
from xml.etree.ElementTree import Element, SubElement, tostring

from django.contrib import messages
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render

from .forms import ContactForm


SITE_URL = "https://www.inkagrowth.com"
BRAND_NAME = "INKAGROWTH"
BRAND_ALTERNATE_NAME = "Inka Growth"
CONTACT_EMAIL = "info@inkagrowth.com"
CONTACT_PHONE = "+91 9389826074"
LOCATION = "Chandausi, Uttar Pradesh, India"
SOCIAL_LINKS = {
    "Facebook": "https://www.facebook.com/profile.php?id=61574394691962",
    "Instagram": "https://www.instagram.com/inkagrowth/",
    "LinkedIn": "https://www.linkedin.com/company/inkagrowth/",
    "Blog": "https://blog.inkagrowth.com",
}

GLOBAL_FAQS = [
    {
        "question": "What is INKAGROWTH?",
        "answer": "INKAGROWTH is a Chandausi-based digital marketing agency that helps businesses grow with SEO, social media marketing, Google Ads, website development, lead generation, and branding.",
    },
    {
        "question": "Where is INKAGROWTH located?",
        "answer": "INKAGROWTH is based in Chandausi, Uttar Pradesh, India, and works with businesses that want practical digital growth support.",
    },
    {
        "question": "Who founded INKAGROWTH?",
        "answer": "INKAGROWTH was founded by Arpit Kumar, who leads digital marketing, SEO, website, and business growth strategy for the agency.",
    },
    {
        "question": "How can I contact INKAGROWTH?",
        "answer": "You can contact INKAGROWTH through the contact page, by emailing info@inkagrowth.com, or by calling +91 9389826074.",
    },
    {
        "question": "What services does INKAGROWTH provide?",
        "answer": "INKAGROWTH provides SEO, social media marketing, Google Ads, website development, branding, analytics, and lead generation services.",
    },
]

TEAM_MEMBERS = [
    {
        "name": "Arpit Kumar",
        "role": "Founder, INKAGROWTH",
        "summary": "Arpit Kumar leads INKAGROWTH strategy across SEO, digital marketing, website development, brand positioning, and growth systems.",
        "email": CONTACT_EMAIL,
    },
    {
        "name": "Arvind Kumar",
        "role": "Digital Growth Specialist",
        "summary": "Arvind supports INKAGROWTH clients with campaign execution, reporting, and practical digital marketing workflows.",
        "email": CONTACT_EMAIL,
    },
    {
        "name": "Prabhat Kumar",
        "role": "Creative and Web Support",
        "summary": "Prabhat helps INKAGROWTH deliver branded web experiences, creative assets, and conversion-focused page improvements.",
        "email": CONTACT_EMAIL,
    },
]

AUTHORITY_PAGES = {
    "about-inkagrowth": {
        "title": "About INKAGROWTH | Digital Marketing Agency in Chandausi",
        "description": "Learn about INKAGROWTH, a Chandausi digital marketing agency founded by Arpit Kumar to help businesses grow with SEO, websites, ads, and social media.",
        "heading": "About INKAGROWTH",
        "intro": "INKAGROWTH is a digital marketing agency in Chandausi built for businesses that want clear strategy, practical execution, and measurable online growth.",
        "sections": [
            (
                "The INKAGROWTH Mission",
                "INKAGROWTH helps businesses build stronger visibility across search, social, websites, and paid media. The agency focuses on honest communication, useful reporting, and marketing decisions that connect to business outcomes.",
            ),
            (
                "Founder-Led Digital Growth",
                "INKAGROWTH is led by founder Arpit Kumar, whose work combines SEO, website development, analytics, branding, and campaign planning. This founder-led approach keeps strategy close to execution.",
            ),
            (
                "Why INKAGROWTH Matters for Branded Search",
                "People searching for inkagrowth, inka growth, inkagrowth agency, inkagrowth digital marketing, or inkagrowth chandausi should find the official INKAGROWTH website first because this site is the primary source for the brand.",
            ),
        ],
    },
    "team": {
        "title": "INKAGROWTH Team | Founder and Digital Marketing Specialists",
        "description": "Meet the INKAGROWTH team, including founder Arpit Kumar and the people supporting digital marketing, SEO, creative, and web growth work.",
        "heading": "INKAGROWTH Team",
        "intro": "The INKAGROWTH team brings together founder-led strategy, campaign execution, creative support, and website improvement for growing businesses.",
        "sections": [(member["role"], f"{member['name']}: {member['summary']}") for member in TEAM_MEMBERS],
    },
    "privacy-policy": {
        "title": "INKAGROWTH Privacy Policy",
        "description": "Read the INKAGROWTH privacy policy for contact form data, business communication, analytics, and website usage.",
        "heading": "INKAGROWTH Privacy Policy",
        "intro": "This privacy policy explains how INKAGROWTH handles information submitted through the official INKAGROWTH website.",
        "sections": [
            ("Information We Collect", "INKAGROWTH may collect your name, email address, phone number, and message when you submit the contact form."),
            ("How INKAGROWTH Uses Information", "INKAGROWTH uses submitted details to respond to business enquiries, provide digital marketing guidance, and improve communication."),
            ("Contact", f"For privacy questions, contact INKAGROWTH at {CONTACT_EMAIL} or {CONTACT_PHONE}."),
        ],
    },
    "terms-and-conditions": {
        "title": "INKAGROWTH Terms and Conditions",
        "description": "Read the INKAGROWTH terms and conditions for website usage, business enquiries, service discussions, and digital marketing information.",
        "heading": "INKAGROWTH Terms and Conditions",
        "intro": "These terms describe general use of the official INKAGROWTH website and branded information pages.",
        "sections": [
            ("Website Use", "The INKAGROWTH website provides information about the INKAGROWTH brand, team, services, and contact options."),
            ("Service Discussions", "Any digital marketing, SEO, website, or campaign discussion with INKAGROWTH becomes active work only after mutual written agreement."),
            ("Contact", f"For questions about these terms, contact INKAGROWTH at {CONTACT_EMAIL}."),
        ],
    },
}

BLOG_POSTS = {
    "who-is-inkagrowth": {
        "title": "Who is INKAGROWTH?",
        "description": "Who is INKAGROWTH? Learn about the Chandausi digital marketing agency, its founder, services, and branded search presence.",
        "heading": "Who is INKAGROWTH?",
        "summary": "INKAGROWTH is a Chandausi digital marketing agency helping businesses grow through search visibility, websites, social media, ads, and branding.",
        "sections": [
            ("The official INKAGROWTH brand", "INKAGROWTH is the official brand name used by the agency across its website, social profiles, contact details, and branded content."),
            ("What INKAGROWTH does", "INKAGROWTH provides SEO, website development, social media marketing, Google Ads support, branding, analytics, and lead generation services."),
            ("Where INKAGROWTH works", "INKAGROWTH is based in Chandausi, Uttar Pradesh, India, and supports businesses that want practical digital growth."),
        ],
    },
    "why-businesses-choose-inkagrowth": {
        "title": "Why Businesses Choose INKAGROWTH",
        "description": "Businesses choose INKAGROWTH for clear strategy, SEO, website development, social media, lead generation, and founder-led execution.",
        "heading": "Why Businesses Choose INKAGROWTH",
        "summary": "Businesses choose INKAGROWTH because the agency keeps digital marketing practical, transparent, and aligned with measurable growth.",
        "sections": [
            ("Founder-led clarity", "INKAGROWTH gives clients direct, practical guidance instead of confusing marketing jargon."),
            ("Full-funnel support", "INKAGROWTH connects SEO, website experience, social media, ads, and lead generation into one growth plan."),
            ("Local and digital context", "INKAGROWTH understands Chandausi businesses while applying modern digital marketing standards."),
        ],
    },
    "inkagrowth-digital-marketing-services": {
        "title": "INKAGROWTH Digital Marketing Services",
        "description": "Explore INKAGROWTH digital marketing services including SEO, websites, social media marketing, Google Ads, branding, and lead generation.",
        "heading": "INKAGROWTH Digital Marketing Services",
        "summary": "INKAGROWTH digital marketing services help businesses improve visibility, trust, traffic, enquiries, and conversion paths.",
        "sections": [
            ("SEO and branded search", "INKAGROWTH helps businesses improve search presence through technical SEO, on-page SEO, content structure, and local visibility."),
            ("Websites and conversion", "INKAGROWTH builds and improves websites so visitors understand the offer and can contact the business quickly."),
            ("Social media and campaigns", "INKAGROWTH supports social media marketing, campaign planning, Google Ads, and brand communication."),
        ],
    },
    "inkagrowth-success-stories": {
        "title": "INKAGROWTH Success Stories",
        "description": "INKAGROWTH success stories show how focused SEO, websites, branding, and campaigns can improve online growth for businesses.",
        "heading": "INKAGROWTH Success Stories",
        "summary": "INKAGROWTH success stories focus on practical business outcomes: clearer messaging, stronger search visibility, better websites, and more qualified enquiries.",
        "sections": [
            ("Visibility improvements", "INKAGROWTH works on search visibility so businesses can be discovered by people already looking for their services."),
            ("Better lead paths", "INKAGROWTH improves calls to action, contact forms, page structure, and trust signals so visitors can take the next step."),
            ("Transparent reporting", "INKAGROWTH keeps clients informed with practical reporting on what changed, why it matters, and what comes next."),
        ],
    },
    "inkagrowth-social-media-marketing-process": {
        "title": "INKAGROWTH Social Media Marketing Process",
        "description": "See the INKAGROWTH social media marketing process for content planning, brand consistency, creative direction, and lead-focused campaigns.",
        "heading": "INKAGROWTH Social Media Marketing Process",
        "summary": "The INKAGROWTH social media marketing process turns brand ideas into consistent content, audience trust, and practical campaign learning.",
        "sections": [
            ("Brand and audience planning", "INKAGROWTH starts by clarifying the business, audience, offer, content pillars, and goals."),
            ("Content creation and publishing", "INKAGROWTH builds content plans that match the brand voice and create useful touchpoints for prospects."),
            ("Measurement and improvement", "INKAGROWTH reviews engagement, enquiries, creative performance, and conversion signals to improve future campaigns."),
        ],
    },
}


def build_url(path):
    return f"{SITE_URL}{path}"


def jsonld(*items):
    return json.dumps([item for item in items if item], ensure_ascii=False)


def base_organization_schema():
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "@id": build_url("/#organization"),
        "name": BRAND_NAME,
        "alternateName": BRAND_ALTERNATE_NAME,
        "url": SITE_URL,
        "logo": build_url("/static/img/logo.png"),
        "image": build_url("/static/img/logo.png"),
        "email": CONTACT_EMAIL,
        "telephone": CONTACT_PHONE,
        "founder": {"@type": "Person", "name": "Arpit Kumar", "jobTitle": "Founder"},
        "sameAs": list(SOCIAL_LINKS.values()),
    }


def website_schema():
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "@id": build_url("/#website"),
        "name": BRAND_NAME,
        "alternateName": BRAND_ALTERNATE_NAME,
        "url": SITE_URL,
        "publisher": {"@id": build_url("/#organization")},
        "potentialAction": {
            "@type": "SearchAction",
            "target": build_url("/?s={search_term_string}"),
            "query-input": "required name=search_term_string",
        },
    }


def local_business_schema():
    return {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "@id": build_url("/#localbusiness"),
        "name": BRAND_NAME,
        "alternateName": BRAND_ALTERNATE_NAME,
        "url": SITE_URL,
        "image": build_url("/static/img/logo.png"),
        "logo": build_url("/static/img/logo.png"),
        "email": CONTACT_EMAIL,
        "telephone": CONTACT_PHONE,
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Chandausi",
            "addressRegion": "Uttar Pradesh",
            "addressCountry": "IN",
        },
        "areaServed": ["Chandausi", "Uttar Pradesh", "India"],
        "priceRange": "$$",
        "sameAs": list(SOCIAL_LINKS.values()),
    }


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


def breadcrumb_schema(items):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": index,
                "name": name,
                "item": build_url(path),
            }
            for index, (name, path) in enumerate(items, start=1)
        ],
    }


def handle_contact_submit(request, redirect_to):
    if request.method != "POST":
        return None

    form = ContactForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Your message has been submitted successfully!")
        return redirect(redirect_to)

    messages.error(request, "Please check your details and try again.")
    return None


def index(request):
    submitted = handle_contact_submit(request, "/")
    if submitted:
        return submitted

    return render(
        request,
        "index.html",
        {
            "faqs": GLOBAL_FAQS,
            "social_links": SOCIAL_LINKS,
            "schema_json": jsonld(
                base_organization_schema(),
                website_schema(),
                local_business_schema(),
                breadcrumb_schema([("INKAGROWTH", "/")]),
                faq_schema(),
            ),
        },
    )


def contact_page(request):
    submitted = handle_contact_submit(request, "/contact/")
    if submitted:
        return submitted

    page = {
        "title": "Contact INKAGROWTH | Official Digital Marketing Agency Contact",
        "description": "Contact INKAGROWTH, the Chandausi digital marketing agency, for SEO, websites, Google Ads, social media marketing, branding, and lead generation.",
        "heading": "Contact INKAGROWTH",
    }
    return render(
        request,
        "contact.html",
        {
            "page": page,
            "canonical": build_url("/contact/"),
            "schema_json": jsonld(
                base_organization_schema(),
                local_business_schema(),
                breadcrumb_schema([("INKAGROWTH", "/"), ("Contact INKAGROWTH", "/contact/")]),
                {
                    "@context": "https://schema.org",
                    "@type": "ContactPage",
                    "name": page["heading"],
                    "url": build_url("/contact/"),
                    "description": page["description"],
                },
            ),
        },
    )


def authority_page(request, slug):
    page = AUTHORITY_PAGES.get(slug)
    if page is None:
        raise Http404("Page not found")

    path = f"/{slug}/"
    schema_type = "AboutPage" if slug == "about-inkagrowth" else "WebPage"
    return render(
        request,
        "authority_page.html",
        {
            "page": page,
            "canonical": build_url(path),
            "social_links": SOCIAL_LINKS,
            "team_members": TEAM_MEMBERS,
            "schema_json": jsonld(
                base_organization_schema(),
                local_business_schema(),
                breadcrumb_schema([("INKAGROWTH", "/"), (page["heading"], path)]),
                {
                    "@context": "https://schema.org",
                    "@type": schema_type,
                    "name": page["heading"],
                    "url": build_url(path),
                    "description": page["description"],
                    "isPartOf": {"@id": build_url("/#website")},
                    "about": {"@id": build_url("/#organization")},
                },
            ),
        },
    )


def blog_index(request):
    page = {
        "title": "INKAGROWTH Blog | Official Brand Articles",
        "description": "Read official INKAGROWTH brand articles about the agency, services, founder-led process, success stories, and social media marketing.",
        "heading": "INKAGROWTH Blog",
        "intro": "Official INKAGROWTH articles answer branded searches and link readers back to the main INKAGROWTH website.",
    }
    return render(
        request,
        "blog_index.html",
        {
            "page": page,
            "posts": BLOG_POSTS,
            "canonical": build_url("/blog/"),
            "schema_json": jsonld(
                base_organization_schema(),
                breadcrumb_schema([("INKAGROWTH", "/"), ("INKAGROWTH Blog", "/blog/")]),
            ),
        },
    )


def blog_post(request, slug):
    post = BLOG_POSTS.get(slug)
    if post is None:
        raise Http404("Post not found")

    path = f"/blog/{slug}/"
    return render(
        request,
        "blog_post.html",
        {
            "post": post,
            "canonical": build_url(path),
            "schema_json": jsonld(
                base_organization_schema(),
                breadcrumb_schema([("INKAGROWTH", "/"), ("INKAGROWTH Blog", "/blog/"), (post["heading"], path)]),
                {
                    "@context": "https://schema.org",
                    "@type": "BlogPosting",
                    "headline": post["heading"],
                    "description": post["description"],
                    "url": build_url(path),
                    "mainEntityOfPage": build_url(path),
                    "author": {"@type": "Person", "name": "Arpit Kumar"},
                    "publisher": {"@id": build_url("/#organization")},
                    "image": build_url("/static/img/logo.png"),
                    "datePublished": "2026-06-06",
                    "dateModified": date.today().isoformat(),
                },
                faq_schema(),
            ),
        },
    )


def robots_txt(request):
    response = render(request, "robots.txt", content_type="text/plain")
    response.headers.pop("X-Robots-Tag", None)
    return response


def sitemap_xml(request):
    today = date.today().isoformat()
    page_paths = [
        ("/", "1.0"),
        ("/about-inkagrowth/", "0.9"),
        ("/contact/", "0.9"),
        ("/team/", "0.8"),
        ("/privacy-policy/", "0.6"),
        ("/terms-and-conditions/", "0.6"),
        ("/blog/", "0.8"),
    ]
    post_paths = [(f"/blog/{slug}/", "0.7") for slug in BLOG_POSTS]
    urlset = Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for path, priority in page_paths + post_paths:
        url = SubElement(urlset, "url")
        SubElement(url, "loc").text = build_url(path)
        SubElement(url, "lastmod").text = today
        SubElement(url, "changefreq").text = "monthly"
        SubElement(url, "priority").text = priority

    xml = b'<?xml version="1.0" encoding="UTF-8"?>\n' + tostring(urlset, encoding="utf-8")
    response = HttpResponse(xml, content_type="application/xml")
    response.headers.pop("X-Robots-Tag", None)
    return response


def ping(request):
    return HttpResponse("OK")
