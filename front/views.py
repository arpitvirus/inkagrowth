import json
from datetime import date

from django.contrib import messages
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ContactForm
from .models import PortfolioProject


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
        "role": "Founder & CEO",
        "summary": "Arpit Kumar leads INKAGROWTH strategy across SEO, digital marketing, website development, brand positioning, and growth systems.",
        "email": CONTACT_EMAIL,
    },
    {
        "name": "Arvind Pal",
        "role": "Sales Manager",
        "summary": "Arvind helps businesses understand the right growth plan and keeps client communication clear from enquiry to onboarding.",
        "email": CONTACT_EMAIL,
    },
    {
        "name": "Prabhat Kumar",
        "role": "Product & Digital Marketing Manager",
        "summary": "Prabhat manages digital marketing execution, product thinking, creative direction, and conversion-focused website improvements.",
        "email": CONTACT_EMAIL,
    },
]

SERVICES = [
    {
        "title": "Digital Marketing",
        "slug": "digital-marketing",
        "path": "/digital-marketing-services/",
        "icon": "fa-chart-line",
        "summary": "Full-funnel strategy that connects visibility, content, campaigns, leads, and reporting into one practical growth system.",
    },
    {
        "title": "SEO Services",
        "slug": "seo",
        "path": "/seo-services/",
        "icon": "fa-magnifying-glass-chart",
        "summary": "Technical SEO, on-page optimization, local SEO, content structure, and search visibility improvements for long-term traffic.",
    },
    {
        "title": "Social Media Marketing",
        "slug": "social-media",
        "path": "/social-media-marketing/",
        "icon": "fa-share-nodes",
        "summary": "Content planning, creative direction, publishing, campaign ideas, and audience engagement across priority social platforms.",
    },
    {
        "title": "Website Development",
        "slug": "website-development",
        "path": "/website-development/",
        "icon": "fa-laptop-code",
        "summary": "Fast, mobile-friendly websites and landing pages designed for trust, clear messaging, enquiries, and measurable action.",
    },
    {
        "title": "Lead Generation",
        "slug": "lead-generation",
        "path": "/lead-generation-services/",
        "icon": "fa-filter-circle-dollar",
        "summary": "Landing pages, forms, ad funnels, audience targeting, and follow-up paths built to turn attention into qualified enquiries.",
    },
    {
        "title": "Branding",
        "slug": "branding",
        "path": "/branding-services/",
        "icon": "fa-pen-nib",
        "summary": "Positioning, brand messaging, visual direction, and digital identity systems that help customers remember and trust you.",
    },
    {
        "title": "Performance Marketing",
        "slug": "performance-marketing",
        "path": "/performance-marketing-services/",
        "icon": "fa-bullseye",
        "summary": "Campaign planning, paid media testing, conversion tracking, and optimization focused on leads, sales, and return on spend.",
    },
]

SERVICE_LANDING_PAGES = {
    "digital-marketing-services": {
        "title": "Digital Marketing Services in Chandausi | INKAGROWTH",
        "description": "Digital marketing services in Chandausi from INKAGROWTH: SEO, websites, social media, Google Ads, branding, lead generation, and reporting.",
        "heading": "Digital Marketing Services in Chandausi",
        "eyebrow": "Digital Marketing",
        "path": "/digital-marketing-services/",
        "summary": "INKAGROWTH builds practical digital marketing plans for businesses that need search visibility, sharper websites, stronger social content, and better lead flow.",
        "sections": [
            ("Search and discovery", "We improve how customers find your business through technical SEO, keyword-focused pages, local search signals, and useful content structure."),
            ("Website and conversion", "We make sure traffic has a clear path to trust, enquiry, calls, forms, and next-step actions across mobile and desktop experiences."),
            ("Campaign learning", "We connect organic work, paid campaigns, analytics, and monthly reporting so every channel teaches the next decision."),
        ],
    },
    "seo-services": {
        "title": "SEO Services in Chandausi | INKAGROWTH",
        "description": "SEO services in Chandausi for technical SEO, on-page optimization, local SEO, content structure, and search visibility from INKAGROWTH.",
        "heading": "SEO Services in Chandausi",
        "eyebrow": "SEO",
        "path": "/seo-services/",
        "summary": "INKAGROWTH helps businesses earn more qualified organic visibility with technical fixes, local search improvements, service-page optimization, and content planning.",
        "sections": [
            ("Technical SEO foundations", "We review crawlability, page structure, internal links, speed basics, metadata, canonical tags, and indexability signals."),
            ("Local and service keywords", "We map high-intent local searches to clear pages so customers understand your offer and can contact you quickly."),
            ("Content that answers demand", "We build content around real customer questions, service proof, location context, and conversion intent."),
        ],
    },
    "social-media-marketing": {
        "title": "Social Media Marketing in Chandausi | INKAGROWTH",
        "description": "Social media marketing in Chandausi for content planning, creative direction, publishing, campaigns, and audience engagement by INKAGROWTH.",
        "heading": "Social Media Marketing in Chandausi",
        "eyebrow": "Social Media",
        "path": "/social-media-marketing/",
        "summary": "INKAGROWTH turns social media into a consistent brand presence with content pillars, campaign ideas, creative direction, and lead-focused messaging.",
        "sections": [
            ("Content planning", "We define topics, offers, proof points, and publishing rhythms that match your audience and business goals."),
            ("Creative execution", "We shape posts, reels, captions, and campaign assets so the brand looks consistent and easy to understand."),
            ("Audience and lead flow", "We connect engagement to enquiry paths, landing pages, WhatsApp, calls, and follow-up systems."),
        ],
    },
    "website-development": {
        "title": "Website Development in Chandausi | INKAGROWTH",
        "description": "Website development in Chandausi for fast, mobile-friendly, SEO-ready, conversion-focused business websites by INKAGROWTH.",
        "heading": "Website Development in Chandausi",
        "eyebrow": "Website Development",
        "path": "/website-development/",
        "summary": "INKAGROWTH builds and improves websites that explain the offer clearly, load well on mobile, support SEO, and make enquiries easier.",
        "sections": [
            ("Clear page structure", "We organize homepage, service, about, proof, and contact sections so visitors can scan and decide faster."),
            ("SEO-ready build", "We include titles, descriptions, headings, internal links, schema basics, canonical tags, and crawlable public pages."),
            ("Conversion paths", "We design calls, forms, WhatsApp actions, trust sections, and lead capture points around real customer behavior."),
        ],
    },
    "google-ads-services": {
        "title": "Google Ads Services in Chandausi | INKAGROWTH",
        "description": "Google Ads services in Chandausi for search campaigns, landing pages, conversion tracking, and lead generation from INKAGROWTH.",
        "heading": "Google Ads Services in Chandausi",
        "eyebrow": "Google Ads",
        "path": "/google-ads-services/",
        "summary": "INKAGROWTH plans Google Ads around useful landing pages, clear offers, search intent, conversion tracking, and practical budget learning.",
        "sections": [
            ("Search intent campaigns", "We group keywords by customer intent so ad copy and landing pages match what people are actively looking for."),
            ("Lead-focused landing pages", "We connect campaigns to clear pages with contact actions, trust signals, and service-specific messaging."),
            ("Measurement and optimization", "We review enquiries, cost, terms, landing-page behavior, and campaign quality before scaling spend."),
        ],
    },
    "lead-generation-services": {
        "title": "Lead Generation Services in Chandausi | INKAGROWTH",
        "description": "Lead generation services in Chandausi for landing pages, forms, campaigns, tracking, and follow-up systems by INKAGROWTH.",
        "heading": "Lead Generation Services in Chandausi",
        "eyebrow": "Lead Generation",
        "path": "/lead-generation-services/",
        "summary": "INKAGROWTH helps businesses turn traffic and campaign attention into qualified enquiries with clearer offers, landing pages, forms, and follow-up paths.",
        "sections": [
            ("Offer clarity", "We define what customers get, why it matters, and what action they should take next."),
            ("Landing page flow", "We build pages with proof, FAQs, calls to action, contact forms, and mobile-friendly sections."),
            ("Follow-up readiness", "We connect enquiries to CRM thinking, WhatsApp, email, and team workflows so leads do not disappear after submission."),
        ],
    },
    "branding-services": {
        "title": "Branding Services in Chandausi | INKAGROWTH",
        "description": "Branding services in Chandausi for positioning, messaging, visual direction, and digital identity systems from INKAGROWTH.",
        "heading": "Branding Services in Chandausi",
        "eyebrow": "Branding",
        "path": "/branding-services/",
        "summary": "INKAGROWTH helps businesses look clearer and more trustworthy with practical positioning, messaging, visual direction, and digital brand consistency.",
        "sections": [
            ("Positioning", "We clarify who the business serves, what makes it useful, and why customers should trust it."),
            ("Messaging", "We shape headlines, service explanations, proof points, and calls to action for websites and campaigns."),
            ("Digital consistency", "We align website, social, search snippets, business profiles, and campaign creative around one recognizable identity."),
        ],
    },
    "performance-marketing-services": {
        "title": "Performance Marketing Services in Chandausi | INKAGROWTH",
        "description": "Performance marketing services in Chandausi for paid campaigns, conversion tracking, landing pages, and optimization by INKAGROWTH.",
        "heading": "Performance Marketing Services in Chandausi",
        "eyebrow": "Performance Marketing",
        "path": "/performance-marketing-services/",
        "summary": "INKAGROWTH uses campaign testing, landing-page improvements, conversion tracking, and reporting to help businesses learn what creates measurable enquiries.",
        "sections": [
            ("Channel planning", "We choose search, social, retargeting, or landing-page improvements based on the offer and customer intent."),
            ("Tracking and reporting", "We set up practical measurement around leads, calls, forms, campaign performance, and page behavior."),
            ("Optimization cycles", "We improve audiences, copy, creative, budgets, and landing pages based on what the data shows."),
        ],
    },
}

PUBLIC_PAGES = {
    "services": {
        "title": "Digital Marketing Services in Chandausi | INKAGROWTH",
        "description": "Explore INKAGROWTH services including digital marketing, SEO, social media marketing, website development, lead generation, branding, and performance marketing.",
        "heading": "Digital Marketing Services Built for Measurable Growth",
        "path": "/services/",
        "schema_type": "Service",
    },
    "results": {
        "title": "Marketing Results and Growth Case Studies | INKAGROWTH",
        "description": "See INKAGROWTH growth results, case-study style examples, metrics, and before-after improvements from SEO, websites, branding, and performance marketing.",
        "heading": "Results That Connect Marketing Work to Business Growth",
        "path": "/results/",
        "schema_type": "CollectionPage",
    },
    "about": {
        "title": "About INKAGROWTH | Digital Marketing Agency in Chandausi",
        "description": "Learn about INKAGROWTH, our mission, vision, process, team, and founder-led digital marketing approach from Chandausi, Uttar Pradesh.",
        "heading": "About INKAGROWTH",
        "path": "/about/",
        "schema_type": "AboutPage",
    },
    "clients": {
        "title": "INKAGROWTH Clients | Industries, Testimonials and Trust",
        "description": "Discover the industries INKAGROWTH serves, local business focus, client trust signals, and testimonials for digital marketing growth.",
        "heading": "Clients Grow With Clear Strategy and Consistent Execution",
        "path": "/clients/",
        "schema_type": "CollectionPage",
    },
}

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


def page_schema(page):
    schema_type = page.get("schema_type", "WebPage")
    schema = {
        "@context": "https://schema.org",
        "@type": schema_type,
        "name": page["heading"],
        "url": build_url(page["path"]),
        "description": page["description"],
        "isPartOf": {"@id": build_url("/#website")},
        "publisher": {"@id": build_url("/#organization")},
        "about": {"@id": build_url("/#organization")},
    }
    if schema_type == "Service":
        schema["provider"] = {"@id": build_url("/#organization")}
        schema["serviceType"] = [service["title"] for service in SERVICES]
        schema["areaServed"] = ["Chandausi", "Uttar Pradesh", "India"]
    return schema


def service_landing_schema(page):
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": page["heading"],
        "url": build_url(page["path"]),
        "description": page["description"],
        "provider": {"@id": build_url("/#organization")},
        "areaServed": ["Chandausi", "Uttar Pradesh", "India"],
        "isPartOf": {"@id": build_url("/#website")},
    }


def portfolio_listing_schema(page):
    return {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": page["heading"],
        "url": build_url("/portfolio/"),
        "description": page["description"],
        "isPartOf": {"@id": build_url("/#website")},
        "publisher": {"@id": build_url("/#organization")},
        "about": {"@id": build_url("/#organization")},
    }


def portfolio_case_study_schema(project, canonical, description, image_url):
    return {
        "@context": "https://schema.org",
        "@type": "CreativeWork",
        "headline": project.business_name,
        "name": project.seo_title,
        "description": description,
        "image": image_url,
        "author": {"@type": "Organization", "name": BRAND_NAME, "url": SITE_URL},
        "publisher": {"@id": build_url("/#organization")},
        "datePublished": project.created_at.date().isoformat(),
        "dateModified": project.updated_at.date().isoformat(),
        "url": canonical,
        "about": {
            "@type": "LocalBusiness",
            "name": project.business_name,
            "description": project.short_description,
            "address": {
                "@type": "PostalAddress",
                "addressLocality": project.location,
                "addressCountry": "IN",
            },
        },
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


def absolute_media_url(field):
    if not field:
        return build_url("/static/img/logo.png")
    return build_url(field.url)


def portfolio_services(project):
    services = [
        service.strip()
        for service in project.services_provided.split(",")
        if service.strip()
    ]
    return services or [project.get_service_type_display()]


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


def render_public_page(request, page_key, template_name):
    page = PUBLIC_PAGES[page_key]
    return render(
        request,
        template_name,
        {
            "page": page,
            "canonical": build_url(page["path"]),
            "services": SERVICES,
            "team_members": TEAM_MEMBERS,
            "social_links": SOCIAL_LINKS,
            "schema_json": jsonld(
                base_organization_schema(),
                website_schema(),
                local_business_schema(),
                breadcrumb_schema([("INKAGROWTH", "/"), (page["heading"], page["path"])]),
                page_schema(page),
            ),
        },
    )


def services_page(request):
    return render_public_page(request, "services", "services.html")


def results_page(request):
    return render_public_page(request, "results", "results.html")


def about_page(request):
    return render_public_page(request, "about", "about.html")


def clients_page(request):
    return render_public_page(request, "clients", "clients.html")


def portfolio_page(request):
    service = request.GET.get("service", "")
    projects = PortfolioProject.live()
    if service in dict(PortfolioProject.SERVICE_TYPE_CHOICES):
        projects = projects.filter(service_type=service)

    featured_projects = PortfolioProject.live().filter(is_featured=True)[:3]
    testimonials = PortfolioProject.live().exclude(testimonial_text="")[:6]
    page = {
        "title": "Portfolio | Digital Marketing Case Studies | Inkagrowth",
        "description": "Explore Inkagrowth portfolio and case studies of local businesses growing through Google Maps SEO, Meta Ads, social media management, website development, and branding.",
        "heading": "Our Portfolio",
        "subheading": "Real work. Real local businesses. Real digital growth.",
    }
    return render(
        request,
        "portfolio.html",
        {
            "page": page,
            "canonical": build_url("/portfolio/"),
            "projects": projects,
            "featured_projects": featured_projects,
            "testimonials": testimonials,
            "service_choices": PortfolioProject.SERVICE_TYPE_CHOICES,
            "active_service": service,
            "schema_json": jsonld(
                base_organization_schema(),
                website_schema(),
                local_business_schema(),
                breadcrumb_schema([("INKAGROWTH", "/"), ("Portfolio", "/portfolio/")]),
                portfolio_listing_schema(page),
            ),
        },
    )


def portfolio_detail(request, slug):
    project = get_object_or_404(PortfolioProject.live(), slug=slug)
    canonical = build_url(project.get_absolute_url())
    description = project.seo_description
    og_image_url = absolute_media_url(project.og_image or project.cover_image)
    services = portfolio_services(project)
    metrics = [
        ("Keywords Targeted", project.keywords_targeted_count),
        ("Search Visibility", project.search_visibility),
        ("Profile Views", project.profile_views),
        ("Direction Requests", project.direction_requests),
        ("Calls Received", project.calls_received),
        ("Leads Generated", project.leads_generated),
        ("Campaigns Run", project.campaigns_run),
    ]
    metrics = [(label, value) for label, value in metrics if value not in (None, "")]
    external_links = [
        ("Website", project.website_url),
        ("Instagram", project.instagram_url),
        ("Facebook", project.facebook_url),
        ("Google Maps", project.google_maps_url),
    ]
    external_links = [(label, url) for label, url in external_links if url]
    return render(
        request,
        "portfolio_detail.html",
        {
            "project": project,
            "canonical": canonical,
            "meta_title": project.seo_title,
            "meta_description": description,
            "og_title": project.og_title or project.seo_title,
            "og_description": project.og_description or description,
            "og_image": og_image_url,
            "services": services,
            "metrics": metrics,
            "external_links": external_links,
            "schema_json": jsonld(
                base_organization_schema(),
                local_business_schema(),
                breadcrumb_schema([
                    ("INKAGROWTH", "/"),
                    ("Portfolio", "/portfolio/"),
                    (project.business_name, project.get_absolute_url()),
                ]),
                portfolio_case_study_schema(project, canonical, description, og_image_url),
            ),
        },
    )


def service_landing_page(request, slug):
    page = SERVICE_LANDING_PAGES.get(slug)
    if page is None:
        raise Http404("Page not found")

    related_pages = [
        related_page
        for related_slug, related_page in SERVICE_LANDING_PAGES.items()
        if related_slug != slug
    ][:4]
    return render(
        request,
        "service_landing.html",
        {
            "page": page,
            "canonical": build_url(page["path"]),
            "related_pages": related_pages,
            "schema_json": jsonld(
                base_organization_schema(),
                website_schema(),
                local_business_schema(),
                breadcrumb_schema([("INKAGROWTH", "/"), ("Services", "/services/"), (page["heading"], page["path"])]),
                service_landing_schema(page),
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


def ping(request):
    return HttpResponse("OK")
