import json
from datetime import date
from xml.etree.ElementTree import Element, SubElement, tostring

from django.contrib import messages
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import SEOPage, contact


SITE_URL = "https://www.inkagrowth.com"
BRAND_NAME = "InkaGROWTH"
CONTACT_EMAIL = "info@inkagrowth.com"
CONTACT_PHONE = "+91 9389826074"

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


def build_url(path):
    return f"{SITE_URL}{path}"


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

def robots_txt(request):
    response = render(request, "robots.txt", content_type="text/plain")
    response.headers.pop("X-Robots-Tag", None)
    return response


def sitemap_xml(request):
    urlset = Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    today = date.today().isoformat()

    static_paths = [
        ("/", "daily", "1.0"),
        ("/seo-services/", "weekly", "0.9"),
        ("/social-media-marketing/", "weekly", "0.9"),
        ("/google-ads-services/", "weekly", "0.9"),
        ("/website-development/", "weekly", "0.9"),
        ("/digital-marketing-services/", "weekly", "0.9"),
        ("/contact/", "monthly", "0.8"),
        ("/privacy-policy/", "yearly", "0.6"),
        ("/terms-and-conditions/", "yearly", "0.6"),
        ("/disclaimer/", "yearly", "0.5"),
        ("/cookie-policy/", "yearly", "0.5"),
    ]

    for path, changefreq, priority in static_paths:
        url = SubElement(urlset, "url")
        SubElement(url, "loc").text = build_url(path)
        SubElement(url, "lastmod").text = today
        SubElement(url, "changefreq").text = changefreq
        SubElement(url, "priority").text = priority

    for page in SEOPage.objects.all().order_by("slug"):
        url = SubElement(urlset, "url")
        SubElement(url, "loc").text = build_url(f"/{page.slug}/")
        SubElement(url, "lastmod").text = today
        SubElement(url, "changefreq").text = "weekly"
        SubElement(url, "priority").text = "0.7"

    xml = b'<?xml version="1.0" encoding="UTF-8"?>\n' + tostring(urlset, encoding="utf-8")
    response = HttpResponse(xml, content_type="application/xml")
    response.headers.pop("X-Robots-Tag", None)
    return response


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


# DYNAMIC SEO PAGE
def dynamic_page(request, slug):

    page = get_object_or_404(
        SEOPage,
        slug=slug
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

    state = "Uttar Pradesh"

    context = {

        'service': page.service,

        'city': page.city,

        'image_url': image_url,

        'state': state,

        'meta_title': page.meta_title,

        'meta_description': page.meta_description,

        'content': page.content,

        'slug': page.slug,

        'canonical': build_url(f"/{page.slug}/"),

        'schema_json': jsonld(
            {
                "@context": "https://schema.org",
                "@type": "Service",
                "name": page.service,
                "serviceType": page.service,
                "provider": {"@type": "Organization", "name": BRAND_NAME, "url": SITE_URL},
                "areaServed": {"@type": "City", "name": page.city},
                "url": build_url(f"/{page.slug}/"),
                "description": page.meta_description,
            },
            faq_schema(),
        ),
    }

    return render(
        request,
        'seo_page.html',
        context
    )
