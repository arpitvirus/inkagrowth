import json
from datetime import date
from xml.etree.ElementTree import Element, SubElement, tostring

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import ContactForm


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
        "question": "How can I start working with InkaGROWTH?",
        "answer": "Send a message through the contact page or call +91 9389826074. We will review your goals and recommend the right growth plan.",
    },
]


def build_url(path):
    return f"{SITE_URL}{path}"


def jsonld(*items):
    return json.dumps([item for item in items if item], ensure_ascii=False)


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
            "https://blog.inkagrowth.com",
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
    website_schema = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": BRAND_NAME,
        "url": SITE_URL,
    }

    return render(
        request,
        "index.html",
        {
            "faqs": GLOBAL_FAQS,
            "schema_json": jsonld(
                organization_schema,
                local_business_schema,
                website_schema,
                faq_schema(),
            ),
        },
    )


def contact_page(request):
    submitted = handle_contact_submit(request, "/contact/")
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


def robots_txt(request):
    response = render(request, "robots.txt", content_type="text/plain")
    response.headers.pop("X-Robots-Tag", None)
    return response


def sitemap_xml(request):
    today = date.today().isoformat()
    urlset = Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for path, priority in (("/", "1.0"), ("/contact/", "0.8")):
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
